from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = 'key' # This serves as a secret key for the session, which is used to encrypt the cookie

@app.route('/')
def login():
    # Configure session
    session['theme'] = 'light'
    session['username'] = 'Guest'

    return render_template('login.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/update_code')
def update_code():
    return render_template('update_code.html')

@app.route('/options')
def options():
    return render_template('options.html', theme=session['theme'])

@app.route('/highscores')
def highscores():
    return render_template('highscores.html')

@app.route('/replays')
def replays():
    return render_template('replays.html')

#logic
@app.route('/toggle-theme')
def toggle_theme():
    if session['theme'] == 'dark':
        session['theme'] = 'light'
    elif session['theme'] == 'light':
        session['theme'] = 'dark'
    return options()

if __name__ == '__main__':
    app.run()
