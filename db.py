import sqlite3
import logging

database = sqlite3.connect("db.db")
cursor = database.cursor()

try:
    cursor.execute('''CREATE TABLE games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_set INTEGER
    )''')
except Exception as ex:
    logging.error(f'Games table already exists. {ex}')

try:
    cursor.execute('''CREATE TABLE score (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team1 INTEGER,
        team2 INTEGER
    )''')
except Exception as ex:
    logging.error(f'Score table already exists. {ex}')


try:
    cursor.execute('''CREATE TABLE tournaments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tournament TEXT,
        status BOOLEAN DEFAULT FALSE
    )''')
except Exception as ex:
    logging.error(f'Tournaments table already exists. {ex}')

try:
    cursor.execute('''CREATE TABLE sets (
        game_set INTEGER PRIMARY KEY,
        status BOOLEAN
    )''')
except Exception as ex:
    logging.error(f'Sets table already exists. {ex}')


# cursor.execute("DELETE FROM referrals WHERE id<>1000")
# database.commit()
