from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, Regexp

from settings import CUSTOM_LENGTH_REGEX


class URLForm(FlaskForm):
    original_link = URLField(
        'Изначальный URL', validators=[
            DataRequired(message='Обязательное поле'),
        ]
    )
    custom_id = StringField(
        'Короткий ID из 16 знаков', validators=[
            Regexp(CUSTOM_LENGTH_REGEX), Optional(),
        ]
    )
    submit = SubmitField('Запилить')
