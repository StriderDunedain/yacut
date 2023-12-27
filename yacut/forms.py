from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URL_Form(FlaskForm):
    original_url = URLField(
        'Изначальный URL', validators=[
            DataRequired(message='Обязательное поле'),
        ]
    )
    custom_id = StringField(
        'Короткий ID из 6 знаков', validators=[
            DataRequired(message='Обязательное поле'),
            Length(16), Optional(),
        ]
    )
    submit = SubmitField('Запилить')
