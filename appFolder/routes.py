from appFolder import app

from flask import render_template, flash, redirect,\
     url_for

from appFolder.forms import LoginForm

PROJECT_NAME = 'Hubble-Berry'



@app.route('/')
@app.route('/index')
def index():
    user = {'username': ''}
    return render_template('index.html', title=PROJECT_NAME, user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)