import math

from telebot import types

import config

def tournaments_keyboard(tournaments_info, page):
    """Generates keyboards with categories."""

    keyboard = types.InlineKeyboardMarkup(row_width=5)

    pages = math.ceil(len(tournaments_info) / config.ON_PAGE)

    for num, tournament in enumerate(tournaments_info[config.ON_PAGE*page-config.ON_PAGE:config.ON_PAGE*page]):
        if tournament[2]:
            keyboard.add(types.InlineKeyboardButton(f'✅ {num + 1 + config.ON_PAGE * (page - 1)}. {tournament[1]}', callback_data = f'tournament_1_{tournament[0]}_{page}'))
        else:
            keyboard.add(types.InlineKeyboardButton(f'{num + 1 + config.ON_PAGE * (page - 1)}. {tournament[1]}', callback_data = f'tournament_0_{tournament[0]}_{page}'))

    begin_callback = f'page_1'
    back_callback = f'page_{page - 1}'
    forward_callback = f'page_{page + 1}'
    end_callback = f'page_{pages}'

    if page == 1:
        begin_callback = 'not_available'
        back_callback = 'not_available'
    elif page == pages:
        forward_callback = 'not_available'
        end_callback = 'not_available'
    
    if len(tournaments_info) > config.ON_PAGE:
        begin = types.InlineKeyboardButton('<<<', callback_data = begin_callback)
        back = types.InlineKeyboardButton('<-', callback_data = back_callback)
        page = types.InlineKeyboardButton(f'{page}/{pages}', callback_data = 'not_available')
        forward = types.InlineKeyboardButton('->', callback_data = forward_callback)
        end = types.InlineKeyboardButton('>>>', callback_data = end_callback)
        keyboard.add(begin, back, page, forward, end)
    
    keyboard.add(types.InlineKeyboardButton('👍 Готово', callback_data = f'done'))
    
    return keyboard


def sets_keyboard(sets_info):
    """Generates keyboards with categories."""

    keyboard = types.InlineKeyboardMarkup(row_width=4)

    buttons = []

    for game_set in sets_info:
        if game_set[1]:
            buttons.append(types.InlineKeyboardButton(f'✅ {game_set[0]}', callback_data = f'set_1_{game_set[0]}'))
        else:
            buttons.append(types.InlineKeyboardButton(f'{game_set[0]}', callback_data = f'set_0_{game_set[0]}'))

    keyboard.add(buttons[0], buttons[1], buttons[2], buttons[3])
    keyboard.add( buttons[4], buttons[5], buttons[6])
    keyboard.add(types.InlineKeyboardButton('👍 Готово', callback_data = f'done'))
    
    return keyboard