from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required


from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User

from datetime import datetime
from werkzeug.urls import url_parse


# before_request decorator is called before a view function is called,
# can be used for multiple purposes
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # db.session.add(current_user)  - this is not necessary
        db.session.commit()

# route decorators - map the URLs given in the two routes below to the function below them
@app.route('/')
@app.route('/index')
# View function associated with the above two routes
@login_required
def index():
    posts = [
        {
            'author':{'username':'John'},
            'body':'Beautiful day here'
        },
        {
            'author':{'username':'Guy1'},
            'body':'Hello there'
        },
        {
            'author':{'username':'Guy2'},
            'body':'hey there'
        }
    ]
    # Process of converting a template to a complete HTML page is called rendering.
    # The source code of the HTML page(in browser) wil be different from the template
    return render_template('index.html', title='Home', posts=posts)

# LOGIN VIEW FUNCTION
# login() - The view function that accepts and validates data from the user
# create an object of class LoginForm and send the object to the template and the form
# fields will get rendered, method argument tells the kind of requests that are accepted by this function
# flash shows a message to the user, provided a template renders it
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # query the database to find a user by name form.username and pick the first() result
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or Password!')
            return redirect(url_for('login'))
        # flash-login method login_user will register the user as logged in
        # and the future pages will have current_user set to user
        login_user(user, remember=form.remember_me.data)
        # next_page is set to a relative URL. Absolute URL indicates malicious activity
        # in which case the user is redirected to the index and not the absolute URl
        # netloc does that
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # ??
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are not a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
                {
                    'author': user,
                    'body': 'Test post 1'
                },
                {
                    'author': user,
                    'body': 'Test post 2'
                }]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # copy form values to user object
        # if validate_on_submit is false, it is because it was get request or
        # post with some data invalid
        current_user.username=form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        # pre-populate the input fields with values from the database
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!', format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

