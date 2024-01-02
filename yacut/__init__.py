import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from settings import Config

app = Flask(__name__)
# app.config.from_object(Config)
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


from . import api_views, forms, models, views
