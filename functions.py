import sqlite3
import telebot
import requests
import time
import itertools

import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


# проверка отправлялось ли уведомление по игре
def is_in_database(game_id, game_set):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        games = cursor.execute(f'''SELECT COUNT(id) 
                                FROM games 
                                WHERE game_id=? and game_set=?
                                ''', (game_id, game_set,)).fetchall()[0][0]
        
        cursor.close()
        database.close()

        return games
    except:
        pass


# проверка наличия турнира в БД
def is_tournament_in_database(tournament):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        tournaments = cursor.execute(f'''SELECT COUNT(id) 
                                FROM tournaments 
                                WHERE tournament=?
                                ''', (tournament,)).fetchall()[0][0]
        
        cursor.close()
        database.close()

        return tournaments

    except:
        pass


# добавление игры в бд (значит по ней на конкретном сете отправлялось уведомление)
def add_game(game_id, game_set):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            INSERT INTO games (game_id, game_set)
            VALUES (?, ?)
            ''', (game_id, game_set,))
            
        database.commit()
        cursor.close()
        database.close()
    except:
        pass


# добавление турнира в БД
def add_tournament(tournament):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            INSERT INTO tournaments (tournament)
            VALUES (?)
            ''', (tournament,))
            
        database.commit()
        cursor.close()
        database.close()
    except:
        pass


# проверка статуса турнира (присылать ли по нему уведомление)
def check_tournament(tournament):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        status = cursor.execute(f'''SELECT status 
                                FROM tournaments 
                                WHERE tournament=?
                                ''', (tournament,)).fetchall()[0][0]
        
        cursor.close()
        database.close()

        return status
    except:
        pass


# получить информацию о турнирах
def get_tournaments():
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        tournaments_info = cursor.execute('SELECT * FROM tournaments').fetchall()
        
        cursor.close()
        database.close()

        return tournaments_info
    except:
        pass


# обновить статус турнира
def update_tournament(tournament, status):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE tournaments
                        SET status=?
                        WHERE id=?
                        ''', (status, tournament,))

        database.commit()
        cursor.close()
        database.close()
    except:
        pass

# обновить статус сета (отслеживается или нет)
def update_set(game_set, status):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE sets
                        SET status=?
                        WHERE game_set=?
                        ''', (status, game_set,))

        database.commit()
        cursor.close()
        database.close()
    except:
        pass

# выбрать отслеживаемые сеты
def select_active_sets():
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        sets = cursor.execute('SELECT game_set FROM sets WHERE status=?', (True,)).fetchall()
        
        cursor.close()
        database.close()

        if sets:
            sets = list(itertools.chain.from_iterable(sets))
        
        return sets
    
    except:
        pass

# извлечь информацию по всем сетам
def get_sets():
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        sets_info = cursor.execute('SELECT * FROM sets').fetchall()
        
        cursor.close()
        database.close()

        return sets_info
    except:
        pass


# извлечение целевого счета
def get_score():
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        score = cursor.execute(f'''SELECT team1, team2 
                                FROM score 
                                WHERE id=?
                                ''', (1,)).fetchall()[0]
        
        cursor.close()
        database.close()

        return score[0], score[1]
    except:
        pass


# изменение целевого счета
def update_score(score_1, score_2):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE score
                        SET team1=?, team2=?
                        WHERE id=?
                        ''', (score_1, score_2, 1,))

        database.commit()
        cursor.close()
        database.close()
    except:
        pass


# сброс информации об присланных уведомлениях
def drop_games():
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute('DELETE FROM games')

        database.commit()
        cursor.close()
        database.close()
    except:
        pass


# парсер
def parse_table_tennis_score():
    # бесконечный цикл
    while True:
        # если включены уведомления
        if config.NOTIFY:
            # запрос к url
            try:
                response = requests.get(config.TABLE_TENNIS_URL)
            except:
                pass
            
            # извлечение результата
            try:
                result = response.json().get('Value')
            except:
                result = None

            # если результат получен
            if result:
                # получаем целевой счет
                score_1, score_2 = get_score()

                matches_to_notify = []
                
                # цикл по матчам в выдаче
                for match in result:
                    tournament = match.get('L')

                    # добавляем турнир в БД, если его там не было
                    if not is_tournament_in_database(tournament):
                        try:
                            add_tournament(tournament)
                        except:
                            pass

                    else:
                        # если был - проверяем нужно ли присылать по нему уведомления
                        if check_tournament(tournament):
                            # анализируем счет в сетах 
                            for num, score in enumerate(match.get('SC').get('PS')):
                                game_set = num + 1
                                score1 = score.get('Value').get('S1')
                                score2 = score.get('Value').get('S2')

                                if score1 is None:
                                    score1 = 0
                                
                                if score2 is None:
                                    score2 = 0

                                # если номер сета в отслеживаемых
                                
                                if game_set in select_active_sets():
                                # если встретился целевой счет

                                    if (score1 == score_1 and score2 == score_2) or (score1 == score_2 and score2 == score_1):
                                    
                                        game_id = match.get('I')
                                        # и уведомление по этой игре и сету еще не присылалось - добавляем в список для уведомлений
                                        if not is_in_database(game_id, game_set):
                                            matches_to_notify.append(match)
                                            # добавляем игру и сет в бд, по которым прислано уведомление
                                            add_game(game_id, game_set)

                                        break
                
                replies = []
                reply = f'Счет *{score_1}:{score_2}* встретился в следующих матчах *(настольный теннис)*:\n\n'

                # формируем текст уведомления, предусматриваем вариант, если текст слишком длинный для одного сообщения
                for num, match in enumerate(matches_to_notify):
                    team1 = match.get('O1')
                    team2 = match.get('O2')
                    game_id = match.get('I')

                    lig_num = match.get('LI')
                    lig = match.get('LE').replace(' ', '-')
                    name1 = match.get('O1E').replace(' ', '-')
                    name2 = match.get('O2E').replace(' ', '-')

                    tournament = match.get('L')

                    url = f'{config.LIVE_TABLE_TENNIS}{lig_num}-{lig}/{game_id}-{name1}-{name2}'.lower()

                    reply += f'[{team1} - {team2}]({url}) ({tournament})\n'
                    
                    if (num + 1) % 25 == 0 or num == len(matches_to_notify) - 1:
                        replies.append(reply)
                        reply = ''
                
                # отправляем уведомления
                for reply in replies:
                    try:
                        bot.send_message(chat_id=config.USER_ID,
                                        text=reply,
                                        parse_mode='Markdown',
                                        )
                    except:
                        pass
                
                time.sleep(5)
