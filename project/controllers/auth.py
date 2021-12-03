from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from project import db 
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import time

auth = Blueprint('auth', __name__)
api = TwitterAPI('U6M1BkpdScCQwvGe0rXQ2kfW1', 'g7dhETjYejLMHNHYcXhvz3nw3ZauKAOHZq1ULoYNx8MJClF6j2', '1370127146421780481-mdjuxIlcHpOK7lDsXmMzAYbGU3SZkt', 'vfKtYgNRK878A4mgT3RgVOPZZ9P4TsPq2b5FxMfhT8X1i', api_version='2')
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email    = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('perfil.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

# @auth.route('/signup', methods=['POST'])
# def signup_post():

#     email    = request.form.get('email')
#     name     = request.form.get('name')
#     password = request.form.get('password')
#     twitter_username = request.form.get('twitter_username')
#     twitter_id = api.request(f'users/by/username/:{twitter_username}')
#     twitter_id = twitter_id.json()['data']['id']
#     user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again
#         flash('Email address already exists')
#         return redirect(url_for('auth.signup'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(email=email, 
#                     name=name, 
#                     password=generate_password_hash(password, method='sha256'), 
#                     twitter_id=twitter_id,
#                     twitter_username=twitter_username
#                     )

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))

# @auth.route('/ajax_signup', methods=['POST'])
# def ajax_signup_post():
#     _json = request.json
#     responseMessage = {'message' : 'The account has been created'}
#     responseStatusCode = 200
#     time.sleep(5)
	
#     email    = _json['email']
#     name     = _json['name']
#     password = _json['password']
#     twitter_username = request.form.get('twitter_username')
#     twitter_id = api.request(f'users/by/username/:{twitter_username}')
#     twitter_id = twitter_id.json()['data']['id']
    

#     user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again
#         responseMessage = {'message' : 'Email address already exists'}
#         responseStatusCode = 400
#     else:
#         # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#         new_user = User(email=email, 
#                         name=name, 
#                         password=generate_password_hash(password, method='sha256'), 
#                         twitter_id=twitter_id,
#                         twitter_username=twitter_username
#                         )

#         # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
    
#     response = jsonify(responseMessage)
#     response.status_code = responseStatusCode

#     return response

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))