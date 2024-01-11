from http import HTTPStatus

from flask import render_template

from yacut import app


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND
