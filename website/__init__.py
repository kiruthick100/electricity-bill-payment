from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
db =SQLAlchemy()
DB_NAME ="database.db"
def create_app():
    app =Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] ='kiruthick'
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .models import User,Data
    create_database(app)

    return app
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)