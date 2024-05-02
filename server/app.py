from flask import Flask, render_template, session, jsonify, request, send_file
import database.db_access as db
import json
import os
from server.global_consts import *
import atexit
from log import setup_logger


@atexit.register
def clean_up():
    global handlers
    for handler in handlers:
        handler.close()

logger, handlers = setup_logger("web_app", "logs/web_app")

"""
Flask: Framework for the web application
render_template: Renders a template from the templates folder (html file)
session: A dictionary that stores data for the user
jsonify: Converts a dictionary to a JSON object, which can be used in JavaScript
request: Used to get data from the client
send_file: Used to send a file to the client
"""

app = Flask(__name__)
app.logger = logger
app.secret_key = 'key' # This serves as a secret key for the session, which is used to encrypt the cookie
logger.info("Web app started")

"""
DATABASE FETCH FUNCTIONS: Check username, check login, create user, get user id, upload and download config, upload and download code, download user info, download error log
----------------------------------------------------------------------------------------------------------
"""
def check_username(username):
    try:
        return db.exists_user(username) # True: user exists, False: user does not exist
    except:
        logger.exception(f"Error checking user {username} in database")
        return False

def check_login(username, password):
    try:
        return db.check_user_credentials(username, password) # True: login correct, False: login incorrect
    except:
        logger.exception(f"Error checking login for user {username} in database")
        return False

def createUser(username, password):
    try:
        db.insert_user(username, password)
        return True
    except:
        logger.exception(f"Error creating user {username} in database")
        return False

def IdFromUser(username):
    try:
        return db.get_user_id(username)
    except:
        logger.exception(f"Error getting user id for user {username} in database")
        return False

def uploadConfig(id, health, shield, attack):
    try:
        config = {"health": health, "shield": shield, "attack": attack}
        db.save_config(id, json.dumps(config))
        return True
    except:
        logger.exception(f"Error uploading config for user with id {id} in database")
        return False

def downloadConfig(id):
    try:
        return db.get_config(id) # JSON: {health, shield, attack}
    except:
        logger.exception(f"Error downloading config for user with id {id} in database")
        return False

def uploadCode(id, code):
    try:
        db.save_code(id, code)
        return True
    except:
        logger.exception(f"Error uploading code for user with id {id} in database")
        return False

def downloadCode(id):
    try:
        return db.get_code(id)
    except:
        logger.exception(f"Error downloading code for user with id {id} in database")
        return False

def downloadInfo(id):
    try:
        return db.get_info(id) # JSON: {last_position, last_game}
    except:
        logger.exception(f"Error downloading info for user with id {id} in database")
        return False

def downloadError(id):
    try:
        return db.get_exec_output(id)
    except:
        logger.exception(f"Error downloading error for user with id {id} in database")
        return False


"""
SERVER DATA UPLOAD AND DOWNLOAD FUNCTIONS: Get session data, upload and download config, upload and download code, download user info, download error log, download simulation info
----------------------------------------------------------------------------------------------------------
"""
@app.route('/get_session_data', methods=['GET'])
def get_session_data():
    session_data = {
        'username': session.get('username'),
        'theme': session.get('theme'),
        'loggedIn': session.get('loggedIn')
    }
    return jsonify(session_data)

@app.route('/upload_config', methods=['POST'])
def upload_config():
    # Get the data from the request
    data = request.get_json()
    health = data['health']
    shield = data['shield']
    attack = data['attack']

    # Check that the data is clean (300 points)
    if (health + shield + attack != 300 or health < 50 or shield < 50 or attack < 50 or health > 150 or shield > 150 or attack > 150 or not isinstance(health, int) or not isinstance(shield, int) or not isinstance(attack, int)):
        return '', 400 # Bad request
    
    id = IdFromUser(session['username'])

    uploadConfig(id, health, shield, attack)
    logger.debug("User " + session['username'] + " has updated their bot configuration.")
    return '', 200 # a-ok

@app.route('/download_config', methods=['GET'])
def download_config():
    if session['newUser']:
        return jsonify({"health": "100", "shield": "100", "attack": "100"}), 201
    id = IdFromUser(session['username'])
    data = downloadConfig(id)
    if not data: 
        return '', 400 # Bad request
    logger.debug("Bot configuration succesfully loaded for user " + session['username'] + ": " + data + ".")
    return data, 200

@app.route('/upload_code', methods=['POST'])
def upload_code():

    # Get the data from the request
    code = request.get_json()['code']

    # Check that the code is valid
    is_valid, error_details = check_syntax(code)

    if is_valid:
        user = session['username']
        id = IdFromUser(user)
        uploadCode(id, code)
        logger.debug("User " + session['username'] + " has updated their code.")
        return jsonify({"ok":True}), 200 # a-ok
    else:
        return jsonify({"ok":False, "error":str(error_details)}), 400 # Bad request
    
@app.route('/download_code', methods=['GET'])
def download_code():
    if session['newUser']:
        return jsonify({"code": ""}), 200
    id = IdFromUser(session['username'])
    code = downloadCode(id)
    logger.debug("Code succesfully loaded for user " + session['username'] + ".")
    return jsonify({"code": code}), 200

@app.route('/download_user_info', methods=['GET'])
def download_user_info():
    id = IdFromUser(session['username'])
    user_info = downloadInfo(id)
    if not user_info:
        return '', 400
    logger.debug("User info succesfully loaded for user " + session['username'] + ".")
    
    return jsonify({"position": user_info[0], "date": user_info[1]}), 200

@app.route('/download_error_log', methods=['GET'])
def download_error_log():
    id = IdFromUser(session['username'])
    error_log = downloadError(id)
    if not error_log:
        return '', 400
    logger.debug("Error log succesfully loaded for user " + session['username'] + ".")
    
    return jsonify({"error_log": error_log}), 200

@app.route('/download_simulation_info', methods=['GET'])
def download_simulation_info():
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(path, "replays/simulation_info.txt")
    # format: "Last simulation: 22/08/2023 14:17:25 Duration: 0:00:25.311462 Winner: emmagil Score: 20 Number of simulations: 1"
    with open(file_path, "r") as file:
    # Read the content of the file
        text = file.read()
        day = "".join(text.split(" ")[2])
        hour = "".join(text.split(" ")[3])
        date = day + " " + hour
        duration = "".join(text.split(" ")[5])
        winner = "".join(text.split(" ")[7])
        score = "".join(text.split(" ")[9])
        number = "".join(text.split(" ")[13]) #Number of simulations

    logger.debug("Simulation info succesfully loaded for user " + session['username'] + ".")
    return jsonify({"time": date, "duration": duration, "winner": winner, "score": score, "number": number}), 200

"""
OTHER SERVER FETCH FUNCTIONS: User exists, login function, create user
----------------------------------------------------------------------------------------------------------
"""
@app.route('/user_exists', methods=['POST'])
def user_exists():
    # Get the data from the request
    username = request.get_json()['username']

    # Check that the data is clean
    if (not username.isalnum() or len(username) == 0 or len(username) > 20):
        return '', 400 # Bad request
    
    # Check that the user exists
    user_exists = check_username(username)
    return jsonify({'user_exists': user_exists}), 200 # a-ok

@app.route('/login_function', methods=['POST'])
def login_function():
    # Get the data from the request
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check that the data is clean
    if (not username.isalnum() or not password.isalnum() or len(username) == 0 or len(password) == 0 or len(username) > 20 or len(password) > 20):
        return '', 400 # Bad request

    # Check that the user exists
    userExists = check_username(username)

    if userExists:
        # Check that the login is correct
        loginOk = check_login(username, password)

        # LOGIN
        if loginOk:
            session['newUser'] = False
            session['loggedIn'] = True
            session['username'] = username
            logger.debug('User ' + username + ' logged in.')
            return '', 200 # a-ok
        
        return '', 401 # Unauthorized
    return '', 404 # Not found

@app.route('/create_user', methods=['POST'])
def create_user():
    # Get the data from the request
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check that the data is clean
    if (not username.isalnum() or not password.isalnum() or len(username) == 0 or len(password) == 0 or len(username) > 20 or len(password) > 20):
        return '', 400 # Bad request
    
    # It has been previously checked that the user does not exist already
    newUserId = createUser(username, password)
    session['newUser'] = True
    session['loggedIn'] = True
    session['username'] = username
    logger.debug("User created: " + username + ".")
    return '', 200 # a-ok


"""
SERVER INSIDE FUNCTIONS: Check syntax, validate login
----------------------------------------------------------------------------------------------------------
"""
# Syntax checking for users code
def check_syntax(code):
    try:
        compile(code, '<string>', 'exec') # Code to be compiled, filename name, mode
        return True, None  # Syntax is valid
    except SyntaxError as e:
        return False, e  # Syntax error details

# Prevents user from accessing pages without logging in
def validate_login(route): 
    if session['loggedIn'] == True:
        return route
    else:
        return login()


""" HTML pages and routes: Login, main menu, upload code, bot config, player info, replays, highscores, help, logout
----------------------------------------------------------------------------------------------------------
"""
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/main_menu')
def main_menu():
    return validate_login(render_template('main_menu.html'))

@app.route('/upload_code')
def update_code():
    return validate_login(render_template('upload_code.html'))

@app.route('/bot_config')
def bot_config():
    return validate_login(render_template('bot_config.html'))

@app.route('/player_info')
def options():
    return validate_login(render_template('player_info.html'))

@app.route('/replays')
def replays():
    return validate_login(render_template('replays.html'))

@app.route('/highscores')
def highscores():
    return validate_login(render_template('highscores.html'))

@app.route('/help')
def help():
    return validate_login(render_template('help.html'))

@app.route('/logout')
def logout():
    logger.debug("User " + session['username'] + " has logged off.")
    session.clear()
    return login()

""" MEDIA: Simulation video, help icon
----------------------------------------------------------------------------------------------------------
"""

@app.route('/simulation_video')
def video():
    return validate_login(send_file('replays/simulation.mp4'))

@app.route('/help_icon')
def help_icon():
    return send_file('static/question_icon.png')


""" RUN APP 
----------------------------------------------------------------------------------------------------------
"""
if __name__ == '__main__':
    app.run()

