from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    Migrate(app,db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
   
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for non-auth parts of app
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # blueprint for non-auth parts of app
    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint)

    return app