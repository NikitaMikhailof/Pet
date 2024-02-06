from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/login/')
def login():
    return render_template('login.html') 


@app.route('/registration/')
def registration():
    return render_template('registration.html') 


@app.route('/password_recovery/')
def password_recovery():
    return render_template('password_recovery.html')


@app.route('/send_password_email/')
def send_password_email():
    return render_template('send_password_email.html')


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('404.html')


@app.errorhandler(500)
def pageNotFount(error):
    return render_template('500.html')


if __name__ == '__main__':
    app.run(debug=True)