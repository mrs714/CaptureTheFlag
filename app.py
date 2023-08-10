from flask import Flask, render_template, session, jsonify
"""
Flask: Framework for the web application
render_template: Renders a template from the templates folder (html file)
session: A dictionary that stores data for the user
jsonify: Converts a dictionary to a JSON object, which can be used in JavaScript
"""

app = Flask(__name__)
app.secret_key = 'key' # This serves as a secret key for the session, which is used to encrypt the cookie

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
    return check_login(render_template('main_menu.html'))

@app.route('/update_code')
def update_code():
    return check_login(render_template('update_code.html'))

@app.route('/player_info')
def options():
    return check_login(render_template('player_info.html'))

@app.route('/bot_config')
def bot_config():
    return check_login(render_template('bot_config.html'))

@app.route('/highscores')
def highscores():
    return check_login(render_template('highscores.html'))

@app.route('/replays')
def replays():
    return check_login(render_template('replays.html'))

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

@app.route('/user_exists', methods=['GET'])
def user_exists():
    # Get the data from the request
    username = request.get_json()['username']

    # Check that the data is clean
    if (not username.isalnum() or len(username) == 0 or len(username) > 20):
        return '', 400 # Bad request
    
    # Check that the user exists
    userExists = check_username(username)
    return jsonify({'userExists': userExists}), 200 # a-ok
    
    
# Logic and functions ---------------------------------------------------------
# Change the theme of the website (dark/light)
@app.route('/toggle_theme')
def toggle_theme():
    if session['theme'] == 'dark':
        session['theme'] = 'light'
    else:
        session['theme'] = 'dark'
    return '', 200 # a-ok

# Prevents user from accessing pages without logging in
def check_login(route): 
    if session['loggedIn'] == True:
        return route
    else:
        return login()

#aplication ---------------------------------------------------------
if __name__ == '__main__':
    app.run()
