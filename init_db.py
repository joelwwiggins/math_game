import psycopg2
import logging
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get a connection to the PostgreSQL database."""
    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB', 'math_game'),
                user=os.getenv('POSTGRES_USER', 'user'),
                password=os.getenv('POSTGRES_PASSWORD', 'password'),
                host=os.getenv('POSTGRES_HOST', 'db'),
                port=os.getenv('POSTGRES_PORT', '5432')
            )
            logger.info("Successfully connected to the database")
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to the database after {max_retries} attempts")
                raise

def init_db():
    """Initialize the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Create tables and initialize the database
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
        cursor.close()
        conn.close()

if __name__ == "__main__":
    logger.info("Starting database initialization script")
    if init_db():
        logger.info("Database initialized successfully.")
    else:
        logger.error("Failed to initialize database. Check the logs for details.")