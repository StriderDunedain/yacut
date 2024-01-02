from random import randint
from string import ascii_letters, digits

from flask import abort, flash, redirect, render_template

from settings import BASE_ROUTE

from . import app, db
from .forms import URL_Form
from .models import URLMap

CHARS = ascii_letters + digits
CHAR_LEN = len(CHARS)


@app.route('/', methods=['GET', 'POST', ])
def main_page():
    """Главная страница проекта с формой для ссылок."""
    form = URL_Form()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data

        if short == '' or short is None:
            short = get_unique_short_id()

        if URLMap.query.filter_by(original=original).count():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()

        new_form = URL_Form()
        new_short = BASE_ROUTE + url_map.short

        return render_template('index.html', short=new_short, form=new_form)

    return render_template('index.html', form=form)


@app.route('/url/<string:short>/', methods=['GET', 'POST', ])
def final_view(short):
    """Вью главной страницы уже с новоиспченной ссылкой."""
    short_url = BASE_ROUTE + short
    form = URL_Form()
    return render_template('index.html', short=short_url, form=form)


@app.route('/<string:short>', methods=['GET', ])
def redirect_view(short):
    """Переходит на страницу основного URL."""
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is not None:
        return redirect(url_map.original)
    abort(404)


def get_unique_short_id():
    """Создает ID для короткой ссылки."""
    short_url = ''
    for _ in range(6):
        short_url += CHARS[randint(0, CHAR_LEN - 1)]
    return short_url
