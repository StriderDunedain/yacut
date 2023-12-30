from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


from . import api_views, views, models, forms
