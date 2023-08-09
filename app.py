from flask import Flask, render_template, session

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

# Backend logic for login
@app.route('/login_request', methods=['GET', 'POST'])
def loginRequest():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        session['username'] = username
        return render_template('main_menu.html')
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/update_code')
def update_code():
    return render_template('update_code.html')

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/highscores')
def highscores():
    return render_template('highscores.html')

@app.route('/replays')
def replays():
    return render_template('replays.html')

if __name__ == '__main__':
    app.run()
