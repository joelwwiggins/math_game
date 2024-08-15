import sqlite3
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ensure_directory_exists(path):
    """Ensure that the specified directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
        logger.debug(f"Ensured directory exists: {path}")
    except OSError as error:
        logger.error(f"Error creating directory {path}: {error}")
        raise

def init_db(db_path=None):
    """Initialize the database."""
    if db_path is None:
        # Use a default path in the current working directory
        db_path = os.path.join(os.getcwd(), 'math_game.db')
    
    logger.info(f"Attempting to initialize database at: {db_path}")
    
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    ensure_directory_exists(db_dir)

    try:
        logger.debug(f"Attempting to connect to SQLite database at {db_path}")
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to the database at '{db_path}' successfully.")
        cursor = conn.cursor()

        logger.debug("Creating tables...")
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
        logger.debug("Changes committed to the database.")
        conn.close()
        logger.info("Database connection closed successfully.")
        return True
    except sqlite3.Error as error:
        logger.error(f"SQLite error occurred: {error}")
        return False
    except Exception as error:
        logger.error(f"An unexpected error occurred: {error}")
        return False

if __name__ == '__main__':
    logger.info("Starting database initialization script")
    if init_db():
        logger.info("Database initialized successfully.")
    else:
        logger.error("Failed to initialize database. Check the logs for details.")
    logger.info("Database initialization script completed")