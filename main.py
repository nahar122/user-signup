from flask import Flask, request, redirect
import os
import jinja2
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

@app.route('/')
def index():
    template = jinja_env.get_template('form.html')
    return template.render()

@app.route('/signup',methods=['POST'])
def signup():
    user_error = ''
    pass_error = ''
    conf_error = ''
    email_error = ''
    username = request.form['username']
    password = request.form['password']
    confirm_pass = request.form['confirm-pass']
    email = request.form['email']
    template = jinja_env.get_template('signup.html')
    if username == '' or password == '' or confirm_pass == '':
        user_error = 'Username or password cannot be empty!'
        pass_error = 'Username or password cannot be empty!'
    if len(username) < 3 or len(username) > 20 or ' ' in username:
        user_error = 'Invalid username'
    if len(password) < 3 or len(password) > 20 or ' ' in password:
        pass_error = 'Invalid password'
    if password != confirm_pass:
        conf_error = 'Your passwords do not match!'
    if len(email) > 0:
        period_count = email.count('.')
        at_count = email.count('@')
        if period_count != 1 or at_count != 1 or len(email) < 3 or len(email) > 20:
            email_error = 'Invalid email'
    if not user_error and not pass_error and not conf_error and not email_error:
        return template.render(user=username)
    else:
        error_template = jinja_env.get_template('form.html')
        return error_template.render(user_error=user_error,pass_error=pass_error,conf_error=conf_error,email_error=email_error,username=username,email=email)

app.run()