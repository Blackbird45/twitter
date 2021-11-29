from flask import Blueprint, render_template , request, jsonify
from flask_login import login_required, current_user
from ..models.comment import Comment
from project import db 
import time
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError

perfil = Blueprint('perfil', __name__)

@perfil.route('/profile')
@login_required
def profile():
   # USER_ID = '1370127146421780481'
    USER_ID = current_user.twitter_id

    try:
        api = TwitterAPI('U6M1BkpdScCQwvGe0rXQ2kfW1', 'g7dhETjYejLMHNHYcXhvz3nw3ZauKAOHZq1ULoYNx8MJClF6j2', '1370127146421780481-mdjuxIlcHpOK7lDsXmMzAYbGU3SZkt', 'vfKtYgNRK878A4mgT3RgVOPZZ9P4TsPq2b5FxMfhT8X1i', api_version='2')
        
        params = {'max_results':5}
        user_tweets = api.request(f'users/:{USER_ID}/tweets',params)
        user_tweets = user_tweets.json()['data']
    
    except TwitterRequestError as e:
        print('Request error')
        print(e.status_code)
        for msg in iter(e):
            print(msg)

    except TwitterConnectionError as e:
        print('Connection error')
        print(e)

    except Exception as e:
        print('Exception')
        print(e)
    return render_template('profile.html', user_name=current_user.email, tweets=user_tweets)

@perfil.route('/ajax_new_comment', methods=['POST'])
@login_required
def ajax_new_comment_post():
    _json = request.json
    responseMessage = {'message' : 'The comment has been created'}
    responseStatusCode = 200

    time.sleep(2)
	
    newComment    = _json['newComment']

    if not current_user: # if a user is found, we want to redirect back to signup page so user can try again
        responseMessage = {'message' : 'User in session not exists'}
        responseStatusCode = 400
    else:
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_comment = Comment(comment=newComment, user_id=current_user.id)

        # add the new user to the database
        db.session.add(new_comment)
        db.session.commit()
    
    response = jsonify(responseMessage)
    response.status_code = responseStatusCode

    return response

