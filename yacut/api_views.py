import re
from http import HTTPStatus
from string import ascii_letters, digits

import validators
from flask import abort, jsonify, request

from settings import BASE_ROUTE, CUSTOM_LENGTH_REGEX
from yacut import app, db

from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST', ])
def get_new_short_url():
    """Создает запись в бд о новой ссылке.
       Попутно проверяя данные.
    """
    data = request.get_json()

    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), HTTPStatus.BAD_REQUEST

    original = data.get('url')
    short = data.get('custom_id')

    if original is None:
        return jsonify({'message': '"url" является обязательным полем!'}), HTTPStatus.BAD_REQUEST
    if not validators.url(original):
        abort(HTTPStatus.BAD_REQUEST)

    if short is None or short == '':
        short = get_unique_short_id()
    if not re.search(
        pattern=CUSTOM_LENGTH_REGEX,
        string=short
    ):
        return jsonify(
            {'message': 'Указано недопустимое имя для короткой ссылки'}
        ), HTTPStatus.BAD_REQUEST

    if URLMap.query.filter_by(short=short).count():
        return jsonify(
            {'message': 'Предложенный вариант короткой ссылки уже существует.'}
        ), HTTPStatus.BAD_REQUEST
    if not check_short(short):
        return jsonify(
            {'message': 'Указано недопустимое имя для короткой ссылки'}
        ), HTTPStatus.BAD_REQUEST

    new_url_map = URLMap(
        original=original,
        short=short
    )

    db.session.add(new_url_map)
    db.session.commit()

    return jsonify({
        'url': new_url_map.original,
        'short_link': BASE_ROUTE + new_url_map.short
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET', ])
def get_original(short_id):
    """Возвращает оригинальную ссылку по ID."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    return jsonify({'message': 'Указанный id не найден'}), HTTPStatus.NOT_FOUND


def check_short(short):
    """Доп. ф-ция для проверки `short`,
       Патамушта в `get_new_short_url` и так намешано :/
    """
    for char in short:
        if char not in ascii_letters and char not in digits:
            return False
    return True