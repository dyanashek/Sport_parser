import telebot
import threading

import config
import keyboards
import utils
import functions


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


threading.Thread(daemon=True, target=functions.parse_table_tennis_score).start()


@bot.message_handler(commands=['start'])
def start_message(message):
    '''Handles start command.'''

    bot.send_message(chat_id=message.chat.id,
                         text='Пришлю уведомления',
                         )


@bot.message_handler(commands=['score'])
def start_message(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
        score_1, score_2 = utils.validate_score(message.text.split(' ')[1])

        if isinstance(score_1, int) and isinstance(score_2, int):
            functions.update_score(score_1, score_2)
            functions.drop_games()
            bot.send_message(chat_id=message.chat.id,
                         text=f'Отслеживаются матчи со счетом *{score_1}:{score_2}*',
                         parse_mode='Markdown',
                         )
            
        else:
            bot.send_message(chat_id=message.chat.id,
                         text='Введены некорректные данные',
                         )
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Недостаточно прав.',
                         )
        

@bot.message_handler(commands=['status'])
def start_message(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
        score_1, score_2 = functions.get_score()

        status = 'приостановлены'
        if config.NOTIFY:
            status = 'активны'

        active_sets = str(functions.select_active_sets()).replace('[', '').replace(']', '')

        bot.send_message(chat_id=message.chat.id,
                         text=f'Отслеживаются матчи со счетом *{score_1}:{score_2}*\n*Уведомления:* {status}\n*Отслеживаемые сеты:* {active_sets}',
                         parse_mode='Markdown',
                         )
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Недостаточно прав.',
                         )


@bot.message_handler(commands=['deactivate'])
def start_message(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
        config.NOTIFY = False

        bot.send_message(chat_id=message.chat.id,
                         text=f'Уведомления приостановлены.',
                         )
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Недостаточно прав.',
                         )


@bot.message_handler(commands=['activate'])
def start_message(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
        config.NOTIFY = True

        bot.send_message(chat_id=message.chat.id,
                         text=f'Уведомления активированы.',
                         )
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Недостаточно прав.',
                         )


@bot.message_handler(commands=['tournaments'])
def tournaments_message(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Выберите турниры, по которым присылать уведомления:',
                         reply_markup=keyboards.tournaments_keyboard(functions.get_tournaments(), 1),
                         )
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Недостаточно прав.',
                         )


@bot.message_handler(commands=['sets'])
def game_sets(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
        bot.send_message(chat_id=message.chat.id,
                         text=f'Выберите сеты, по которым присылать уведомления:',
                         reply_markup=keyboards.sets_keyboard(functions.get_sets()),
                         )
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Недостаточно прав.',
                         )


@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id = call.message.chat.id

    call_data = call.data.split('_')
    query = call_data[0]

    if query == 'tournament':
        status = int(call_data[1])
        tournament = int(call_data[2])
        page = int(call_data[3])

        if status:
            status = False
        else:
            status = True

        functions.update_tournament(tournament, status)

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.tournaments_keyboard(functions.get_tournaments(), page),
                                      )
    
    elif query == 'page':
        page = int(call_data[1])

        bot.edit_message_reply_markup(chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=keyboards.tournaments_keyboard(functions.get_tournaments(), page),
                                    )

    elif query == 'set':
        status = int(call_data[1])
        game_set = int(call_data[2])

        if status:
            status = False
        else:
            status = True

        functions.update_set(game_set, status)

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.sets_keyboard(functions.get_sets()),
                                      )

    elif query == 'done':
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text='Изменения применены.',
                              )


if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass