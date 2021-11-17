from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'

    db.init_app(app)

    # controllers module register
    from .controllers import controllers as controllers_blueprint
    app.register_blueprint(controllers_blueprint)

    # models module register
    from .models import models as models_blueprint
    app.register_blueprint(models_blueprint)
    
    
    # blueprint for auth routes in our app
    from .controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .controllers.perfil import perfil as perfil_blueprint
    app.register_blueprint(perfil_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.comment import Comment
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app