from string import ascii_letters, digits
from random import random

from flask import flash, redirect, render_template
from .forms import URL_Form
from .models import URLMap
from . import app, db

CHARS = ascii_letters + digits
CHAR_LEN = len(CHARS)


@app.route('/', methods=['GET',])
def main_page():
    form = URL_Form()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short is None:
            short = get_unique_short_id()

        if URLMap.query.filter_by(short=short).first():
            flash('Такой вариат короткой ссылки уже есть!')
            return render_template('index.html', form=form)

        url_map = URLMap(
            original=form.original_url.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return redirect('index.html', custom_id=short)

    return render_template('index.html', form=form)


def get_unique_short_id():
    short_url = ''
    for _ in range(6 + 1):
        short_url += CHARS[random(CHAR_LEN)]
    return short_url
