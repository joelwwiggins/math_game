"""This script initializes the database for the math game."""

import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db_path='/mnt/db/math_game.db'):
    """Initialize the database."""
    try:
        conn = sqlite3.connect(db_path)
        logger.info("Connected to the database at '%s' successfully.", db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        logger.info("Table 'players' created successfully.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                score INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        ''')
        logger.info("Table 'games' created successfully.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                answer_time FLOAT NOT NULL,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
        ''')
        logger.info("Table 'attempts' created successfully.")

        conn.commit()
        conn.close()
        logger.info("Database initialized and connection closed successfully.")
    except sqlite3.Error as error:
        logger.error("Error initializing database at '%s': %s", db_path, error)

if __name__ == '__main__':
    init_db()