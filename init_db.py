"""this is to initialize the database and create the tables for the math game"""
import sqlite3
import logging
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_db_connection(retries=5, delay=1):
    """Get a connection to the SQLite database with retry logic."""
    db_path = '/mnt/db/math_game.db'
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL")  # Enable Write-Ahead Logging
            logger.info("Connected to the SQLite database successfully.")
            return conn
        except sqlite3.OperationalError as error:
            if "database is locked" in str(error):
                logger.warning("Database is locked, retrying in %s seconds...", delay)
                time.sleep(delay)
            else:
                logger.error("Error connecting to SQLite database: %s", error)
                raise
    logger.error("Failed to connect to SQLite database after %s retries.", retries)
    raise sqlite3.OperationalError("database is locked")


def init_db():
    """Initialize the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        logger.debug("Creating tables...")
        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """
        )
        logger.info("Table 'players' created successfully.")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                score INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """
        )
        logger.info("Table 'games' created successfully.")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                answer_time REAL NOT NULL,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
        """
        )
        logger.info("Table 'attempts' created successfully.")

        conn.commit()
        logger.debug("Changes committed to the database.")
        cursor.close()
        conn.close()
        logger.info("Database connection closed successfully.")
        return True
    except sqlite3.Error as error:
        logger.error("SQLite error occurred: %s", error)
        return False
    except Exception as error:
        logger.error("An unexpected error occurred: %s", error)
        return False


if __name__ == "__main__":
    logger.info("Starting database initialization script")
    if init_db():
        logger.info("Database initialized successfully.")
    else:
        logger.error("Failed to initialize database. Check the logs for details.")
    logger.info("Database initialization script completed")
