from random import randint


# Логика игры
def game_logic(game_data):
    '''
    Логика игры
    :param game_data: Список переменных о состоянии игры и решениях игрока
        game_data = [score, position, jump_direction, jump_height, jump_distance, shelf_x, shelf_y, step]
    :return: Список переменных с состояниями игры
        game_state = [score, position, step, game_message_id, shelf_x, shelf_y]
    '''
    print(f'processing game logic...')
    # достаем переменные из списка
    score = int(game_data[0])
    position = game_data[1]
    jump_direction = game_data[2]
    jump_height = game_data[3]
    jump_distance = game_data[4]
    shelf_x = game_data[5]
    shelf_y = game_data[6]
    step = game_data[7]

    # вычисление положения игрока после прыжка
    check_x = direction_detect(position, jump_direction, jump_distance)
    print(f'check_x: {check_x}')
    check_y = shelf_y - jump_height

    # определяем исходящие данные на основе правильности попадания
    if check_x > 2 or check_x < 0:  # Прыгнул в стену
        game_message_id = 0  # f'Вы прыгнули в стену и кислота догнала вас'
        step, position = 0, 0  # Игра окончена, обнуляем статы
    elif check_x != shelf_x:  # не попал по х
        game_message_id = 1  # f'Вы не попали на полку и упали в кислоту'
        step, position = 0, 0  # Игра окончена, обнуляем статы
    elif check_y != 0:  # не попал по y
        game_message_id = 4  # f'Вы не правильно расчитали высоту и упали в кислоту'
        step, position = 0, 0  # Игра окончена, обнуляем статы
    else:
        win_lose = 1  # Игра продолжается
        step += 1
        position = check_x
        shelf_x = 0  # Обнуляем положение полок
        shelf_y = 0
        if step % 3 == 0: # Если шаг делится на 3 без остатка - у нас новый этаж
            game_message_id = 2  # f'Вы перепрыгнули на следующую полку и достигли нового этажа'
            score += 300
        else:
            game_message_id = 3  # f'Вы перепрыгнули на следующую полку'
            score += 100
    print(f'score after step in game.py: {score}')  # temp
    game_state = [score, position, step, game_message_id, shelf_x, shelf_y]
    return game_state


# расшифровщик сообщений (чтобы не отображать сообщения в URL)
def game_messages(game_message_id):
    game_message = ''
    print(f' game message id: {game_message_id}')
    game_message_id = int(game_message_id)
    if game_message_id == 0:
        game_message = f'Вы прыгнули в стену и кислота догнала вас'
    elif game_message_id == 1:
        game_message = f'Вы не попали на полку и упали в кислоту'
    elif game_message_id == 2:
        game_message = f'Вы перепрыгнули на следующую полку и достигли нового этажа'
    elif game_message_id == 3:
        game_message = f'Вы перепрыгнули на следующую полку'
    elif game_message_id == 4:
        game_message = f'Вы неправильно расчитали высоту и упали в кислоту'
    return game_message


# определяем направление прыжка
def direction_detect(position, jump_direction, jump_distance):
    if jump_direction == 0:  # лево
        check_x = position - jump_distance
    else:  # право
        check_x = position + jump_distance
    return check_x


# определение позиции следующей полки
def next_shelf():
    '''
    Функция определяет позицию следующей полки
    Возвращает положение позиции по x и y, а так же сообщение для пользователя
    :return: shelf_x, shelf_y, shelf_message
    '''
    shelf_x = randint(0, 2)
    print(f'shelf_x: {shelf_x}')
    shelf_y = randint(1, 3)
    msg_x = shelf_x_msg(shelf_x)  # Переводим id позиции в сообщение
    msg_y = shelf_y_msg(shelf_y)  # Переводим id позиции в сообщение

    shelf_message = f'Следующая полка находится {msg_x} и {msg_y}'
    return shelf_x, shelf_y, shelf_message


def shelf_x_msg(shelf_x):
    '''
    Переводим id позиции в сообщение
    :param shelf_x: id позиции
    :return: msg_x: сообщение
    '''
    if shelf_x == 0:
        msg_x = '[В левой части башни]'
    elif shelf_x == 1:
        msg_x = '[По центру башни]'
    elif shelf_x == 2:
        msg_x = '[В правой части башни]'
    return msg_x


def shelf_y_msg(shelf_y):
    '''
    Переводим id позиции в сообщение
    :param shelf_y: id позиции
    :return: msg_y: сообщение
    '''
    if shelf_y == 1:
        msg_y = '[Довольно низко]'
    elif shelf_y == 2:
        msg_y = '[Довольно высоко]'
    elif shelf_y == 3:
        msg_y = '[Очень высоко]'
    return  msg_y


def current_shelf(shelf_x):
    '''
    Переводим текущее положение игрока в сообщение
    :param shelf_x:
    :return: current_shelf_msg: текущее положение игрока с прошлого хода
    '''
    msg_x = shelf_x_msg(shelf_x)  # Переводим id позиции в сообщение
    current_shelf_msg = f'Ваше текущее положение: {msg_x}'
    return current_shelf_msg