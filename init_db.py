import psycopg2
import logging
import time
import os
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get a connection to the database."""
    # Use SQLite for testing
    if os.environ.get('TESTING') == 'True':
        logger.info("Using SQLite for testing")
        conn = sqlite3.connect(os.environ.get('TEST_DB_PATH', ':memory:'))
        conn.row_factory = sqlite3.Row
        return conn
    
    # Use PostgreSQL for production
    max_retries = 10
    retry_delay = 5  # seconds

    logger.info(f"Attempting to connect to database at {os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}")
    logger.info(f"Using database: {os.getenv('POSTGRES_DB')}, user: {os.getenv('POSTGRES_USER')}")
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB', 'math_game'),
                user=os.getenv('POSTGRES_USER', 'user'),
                password=os.getenv('POSTGRES_PASSWORD', 'password'),
                host=os.getenv('POSTGRES_HOST', 'db'),
                port=os.getenv('POSTGRES_PORT', '5432')
            )
            logger.info(f"Successfully connected to the database on attempt {attempt + 1}")
            return conn
        except psycopg2.OperationalError as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.warning(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to the database after {max_retries} attempts")
                logger.error(f"Last error: {str(e)}")
                raise

def init_db():
    """Initialize the database."""
    conn = get_db_connection()
    
    try:
        # For SQLite (testing)
        if os.environ.get('TESTING') == 'True':
            cursor = conn.cursor()
            # SQLite schema
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                score INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                answer_time REAL NOT NULL,
                FOREIGN KEY (game_id) REFERENCES games(id)
            )""")
        else:
            # PostgreSQL schema (unchanged)
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS games (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts (
                id SERIAL PRIMARY KEY,
                game_id INTEGER REFERENCES games(id),
                answer_time FLOAT NOT NULL
            );
            """)
        
        conn.commit()
        logger.info("Tables created successfully")
        return True
    except Exception as e:
        logger.error(f"An error occurred while creating tables: {e}")
        conn.rollback()
        return False
    finally:
        if hasattr(cursor, 'close'):
            cursor.close()
        conn.close()

if __name__ == "__main__":
    logger.info("Starting database initialization script")
    if init_db():
        logger.info("Database initialized successfully.")
    else:
        logger.error("Failed to initialize database. Check the logs for details.")