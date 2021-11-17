from flask import Blueprint, render_template , request, jsonify
from flask_login import login_required, current_user
from ..models.comment import Comment
from project import db 
import time

perfil = Blueprint('perfil', __name__)

@perfil.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user_name=current_user.email)

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

