from flask import Flask, render_template, session, jsonify, request
"""
Flask: Framework for the web application
render_template: Renders a template from the templates folder (html file)
session: A dictionary that stores data for the user
jsonify: Converts a dictionary to a JSON object, which can be used in JavaScript
request: Used to get data from the client
"""

app = Flask(__name__)
app.secret_key = 'key' # This serves as a secret key for the session, which is used to encrypt the cookie

# Database ---------------------------------------------------------
def check_username(username):
    # Check if the username exists in the database
    # Returns True if it does, False if it doesn't
    return False

def check_login(username, password):
    # Check if the login is correct
    # Returns True if it is, False if it isn't
    return True

def createUser(username, password):
    # Create a new user in the database
    # Returns True if it was successful, False if it wasn't
    return False

# Pages --------------------------------------------------------------------
@app.route('/')
def login():
    # Default settings, testing purposes and new users
    if 'loggedIn' not in session:
        session['theme'] = 'dark'
        session['username'] = 'Guest'
        session['loggedIn'] = False

    return render_template('login.html')

@app.route('/main_menu')
def main_menu():
    session['loggedIn'] = True #temporary for testing, should be handled by login
    return validate_login(render_template('main_menu.html'))

@app.route('/update_code')
def update_code():
    return validate_login(render_template('update_code.html'))

@app.route('/player_info')
def options():
    return validate_login(render_template('player_info.html'))

@app.route('/bot_config')
def bot_config():
    return validate_login(render_template('bot_config.html'))

@app.route('/highscores')
def highscores():
    return validate_login(render_template('highscores.html'))

@app.route('/replays')
def replays():
    return validate_login(render_template('replays.html'))

# Obtaining data from the server and server functions ---------------------------------
@app.route('/get_session_data', methods=['GET'])
def get_session_data():
    session_data = {
        'username': session.get('username'),
        'theme': session.get('theme'),
        'loggedIn': session.get('loggedIn')
    }
    return jsonify(session_data)

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
            session['loggedIn'] = True
            session['username'] = username
            return '', 200 # a-ok
        
        return '', 401 # Unauthorized
    return '', 404 # Not found

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
    session['loggedIn'] = True
    session['username'] = username
    return '', 200 # a-ok
    
@app.route('/save_config', methods=['POST'])
def save_config():
    # Get the data from the request
    data = request.get_json()
    health = data['health']
    shield = data['shield']
    attack = data['attack']

    # Check that the data is clean (300 points)
    if (health + shield + attack != 300 or health < 50 or shield < 50 or attack < 50 or health > 150 or shield > 150 or attack > 150 or not isinstance(health, int) or not isinstance(shield, int) or not isinstance(attack, int)):
        return '', 400
    
    saveConfig(health, shield, attack)

    

    


# Logic and functions ---------------------------------------------------------


# Prevents user from accessing pages without logging in
def validate_login(route): 
    if session['loggedIn'] == True:
        return route
    else:
        return login()

#aplication ---------------------------------------------------------
if __name__ == '__main__':
    app.run()

