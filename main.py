from flask import Flask, flash, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
from werkzeug.utils import redirect

import requests

# Для подгрузки мемов
from meme import get_meme
# Логика игры
import game
# Конфиг
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

class JumpForm(FlaskForm):

    # Направление прыжка
    jump_direction = SelectField(
        'Выберите в какую сторону направлен ваш персонаж',
        coerce=int,
        choices=[
            (0, 'Лево'),
            (1, 'Право'),
        ],
        render_kw={
            'class': 'form-control'
        }
    )
    # Высота прыжка
    jump_height = IntegerField(
        'Высота прыжка',
        validators=[
            NumberRange(min=1, max=3, message='Вы можете прыгнуть лишь от 1 до 3'),
            DataRequired(message='Укажите высоту прыжка')
        ],
    )
    # Дистанция прыжка
    jump_distance = RadioField("Дистанция прыжка", choices=[(0, '0'), (1, '1'), (2, '2')] )
    submit = SubmitField("Прыжок")


# Стартовый путь
@app.route("/", methods=['GET', 'POST'])
def index():
    jump_direction = ''
    jump_height = ''
    jump_distance = ''
    jump_distance_game = ''
    shelf_x = 1
    shelf_y = 1
    form = JumpForm()
    meme_pic = 'static/welcome.png'  # Приветственное изображение
    # TODO BUG - Сообщение ниже отображается без переносов
    game_message = ""
    score = 0
    position = 0  # Начальная позиция игрока
    step = 0
    shelf_message = 'Первая полка находится [По центру башни] и [Довольно низко]'  # Положение первой полки

    if form.validate_on_submit():
        jump_direction = form.jump_direction.data
        jump_height = form.jump_height.data
        jump_distance = int(form.jump_distance.data)

        # Передаем в логику игры список с данными игры, получаем список с состояниями игры
        game_data = [
            int(score),
            int(position),
            int(jump_direction),
            int(jump_height),
            int(jump_distance),
            int(shelf_x),
            int(shelf_y),
            int(step),
        ]
        print(game_data)  # temp
        game_state = game.game_logic(game_data)

        game_message = f'' \
                       f'{game.game_messages(game_state[3])} ' \
                       f' {game.current_shelf(int(game_state[1]))}'
        # Переводим id сообщения в текст и добавляем текущее положение для упрощенного понимания

        if game_state[2] != 0:  # Если игрок остался жив, то отправляем игрока на следующий шаг
            # рандомим позицию новой полки
            shelf_x, shelf_y, shelf_message = game.next_shelf()  # return shelf_x, shelf_y, shelf_message
            print(shelf_message)

            flash(game_message)
            flash(shelf_message)

            game_state[4] = shelf_x
            game_state[5] = shelf_y
            print(f'Высота прыжка index - game_state[5]: {game_state[5]}')  # temp
            return redirect(url_for(
                'game_index',
                score=game_state[0],
                game_state=game_state,
            ))
        else:  # Если игрок умер, то отправляем игрока на экран game_over
            flash(game_message)
            return redirect(url_for(
                'game_over',
                game_state=game_state,
            ))

    return render_template(
        "index.html",
        score=score,
        meme_pic=meme_pic,
        game_message=game_message,
        shelf_message=shelf_message,
        form=form,

    )

# Путь после начала игры
@app.route("/<score>_<game_state>", methods=['GET', 'POST'])
def game_index(score, game_state):

    # перевод строки в список с удалением квадратных скобок
    game_state = game_state[1:-1].split(', ')

    form = JumpForm()
    meme_pic = 'static/welcome.png'

    if (int(game_state[3]) % 3) != 0:
        meme_pic, subreddit = get_meme()  # забираем рандомный мем из meme.py

    if form.validate_on_submit():
        jump_direction = form.jump_direction.data
        jump_height = form.jump_height.data
        jump_distance = int(form.jump_distance.data)

        # Упаковываем данные игрока в game_data, чтобы передать в логику игры
        game_data = [
            int(score),
            int(int(game_state[1])),  # position (текущая позиция игрока)
            int(jump_direction),
            int(jump_height),
            int(jump_distance),
            int(game_state[4]),  # shelf_x
            int(game_state[5]),  # shelf_y
            int(game_state[2]),  # step
        ]
        print(f'game data before game logic : {game_data}')  # temp
        # Возвращаем состояние игры из логики
        game_state = game.game_logic(game_data)
        print(f'game_state after game logic: {game_state}')  # temp

        game_message = f'' \
                       f'{game.game_messages(game_state[3])} ' \
                       f' {game.current_shelf(int(game_state[1]))}'
                        # Переводим id сообщения в текст и добавляем текущее положение для упрощенного понимания



        if game_state[2] != 0:  # Если игрок остался жив, то отправляем игрока на следующий шаг
            # рандомим позицию новой полки
            shelf_x, shelf_y, shelf_message = game.next_shelf()  # return shelf_x, shelf_y, shelf_message
            print(shelf_message)

            flash(game_message)
            flash(shelf_message)

            game_state[4] = shelf_x
            game_state[5] = shelf_y
            print(f'Высота прыжка game_index - game_state[5]: {game_state[5]}')  # temp
            return redirect(url_for(
                'game_index',
                score=game_state[0],
                game_state=game_state,
            ))
        else:  # Если игрок умер, то отправляем игрока на экран game_over
            flash(game_message)
            return redirect(url_for(
                'game_over',
                game_state=game_state,

            ))


    return render_template(
        "index.html",
        score=score,
        meme_pic=meme_pic,
        form=form,
    )

@app.route("/game_over_<game_state>", methods=['GET', 'POST'])
def game_over(game_state):

    print(game_state)
    # перевод строки в список с удалением квадратных скобок
    game_state = game_state[1:-1].split(', ')

    # извлекаем нужные параметры
    score = game_state[0]
    print(f'game_over - game_state[0]: {game_state[0]}')
    game_message = game.game_messages(game_state[3])
    game_over_message = f'{game_message}. Ваш финальный счет: {score}'
    meme_pic = 'static/acid_fall.jpg'

    return render_template('game_over.html',
                           game_over_message=game_over_message,
                           meme_pic=meme_pic,
                           main_page=url_for('index'),
                           )




if __name__ == '__main__':
    app.run(debug=True)