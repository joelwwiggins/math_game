""" This script initializes the database for the math game. """

import sqlite3


def init_db(db_path='/mnt/mathgamefilesharemount/mathgamedirectory/math_game.db'):
    """Initialize the database."""
    conn = sqlite3.connect(db_path)
    car = conn.cursor()

    # Create tables
    car.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    car.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            score INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')

    car.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            answer_time FLOAT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
