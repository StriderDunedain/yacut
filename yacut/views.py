from random import randint
from string import ascii_letters, digits

from flask import flash, redirect, render_template

from settings import BASE_ROUTE, DEFAULT_LENGTH

from . import app, db
from .forms import URLForm
from .models import URLMap

CHARS = ascii_letters + digits
CHAR_LEN = len(CHARS)


@app.route('/', methods=['GET', 'POST', ])
def main_page():
    """Главная страница проекта с формой для ссылок."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

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

    new_form = URLForm()
    new_short = BASE_ROUTE + url_map.short

    return render_template('index.html', short=new_short, form=new_form)


@app.route('/url/<string:short>/', methods=['GET', 'POST', ])
def final_view(short):
    """Вью главной страницы уже с новоиспченной ссылкой."""
    short_url = BASE_ROUTE + short
    form = URLForm()
    return render_template('index.html', short=short_url, form=form)


@app.route('/<string:short>', methods=['GET', ])
def redirect_view(short):
    """Переходит на страницу основного URL."""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)


def get_unique_short_id():
    """Создает ID для короткой ссылки."""
    short_url = ''
    for _ in range(DEFAULT_LENGTH):
        short_url += CHARS[randint(0, CHAR_LEN - 1)]
    return short_url
