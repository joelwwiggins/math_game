"main application file"

import logging
import os
import random
import sqlite3
import time

import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, render_template, request, redirect, url_for, session
from init_db import init_db as initialize_database

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_key_for_testing')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['DATABASE'] = {
    'dbname': os.getenv('POSTGRES_DB', 'math_game'),
    'user': os.getenv('POSTGRES_USER', 'user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

def get_db():
    """Get or create a database connection."""
    # Use SQLite for testing
    if os.environ.get('TESTING') == 'True':
        if 'database_connection' not in app.extensions:
            app.extensions['database_connection'] = sqlite3.connect(
                os.environ.get('TEST_DB_PATH', ':memory:'),
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            app.extensions['database_connection'].row_factory = sqlite3.Row
        return app.extensions['database_connection']
    # Use PostgreSQL for production
    if 'database_connection' not in app.extensions:
        app.extensions['database_connection'] = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'math_game'),
            user=os.getenv('POSTGRES_USER', 'user'),
            password=os.getenv('POSTGRES_PASSWORD', 'password'),
            host=os.getenv('POSTGRES_HOST', 'db'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            cursor_factory=DictCursor
        )
    return app.extensions['database_connection']

def close_db(_error=None):
    """Close the database connection."""
    if 'database_connection' in app.extensions:
        app.extensions['database_connection'].close()
        del app.extensions['database_connection']

def init_db():
    """Initialize the database."""
    initialize_database()
    logger.info("Database initialized.")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle the index route."""
    if request.method == 'POST':
        player_name = request.form['player_name']
        session['player_name'] = player_name
        player_id = create_player(player_name)
        if player_id:
            session['player_id'] = player_id
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    """Handle the game route."""
    if 'player_name' not in session or 'player_id' not in session:
        return redirect(url_for('index'))

    if 'game_id' not in session:
        session['game_id'] = create_game(session['player_id'])
        session['score'] = 0

    if 'start_time' not in session:
        session['start_time'] = time.time()

    if request.method == 'POST':
        user_answer = int(request.form['answer'])
        correct_answer = session['num1'] + session['num2']
        answer_time = time.time() - session['start_time']

        if user_answer == correct_answer:
            session['score'] += 1
            update_score(session['game_id'], session['score'])

        record_attempt(session['game_id'], answer_time)
        session['start_time'] = time.time()

        return redirect(url_for('game'))

    session['num1'] = random.randint(0, 10)
    session['num2'] = random.randint(0, 10)

    return render_template('game.html', num1=session['num1'], num2=session['num2'],
                           score=session['score'], player_name=session['player_name'])

@app.route('/results')
def results():
    """Handle the results route."""
    if 'player_name' not in session or 'game_id' not in session:
        return redirect(url_for('index'))

    game_id = session['game_id']
    player_name = session['player_name']
    score = session['score']
    attempts = get_attempts(game_id)

    # Clear the session data after getting results
    session.pop('game_id', None)
    session.pop('score', None)

    return render_template('results.html', attempts=attempts,
                           player_name=player_name, score=score)

def get_attempts(game_id):
    """Get all attempts for a game."""
    try:
        database_conn = get_db()
        cursor = database_conn.cursor()
        
        # For SQLite (testing)
        if os.environ.get('TESTING') == 'True':
            cursor.execute("SELECT answer_time FROM attempts WHERE game_id = ? ORDER BY id",
                           (game_id,))
            return [dict(row) for row in cursor.fetchall()]
        
        # For PostgreSQL
        cursor.execute("SELECT answer_time FROM attempts WHERE game_id = %s ORDER BY id",
                      (game_id,))
        return cursor.fetchall()
    except (psycopg2.Error, sqlite3.Error) as error:
        logger.error("Error getting attempts for game_id '%s': %s", game_id, str(error))
        return []

def create_player(name):
    """Create a new player and return the player ID."""
    try:
        database_conn = get_db()
        cursor = database_conn.cursor()
        
        # For SQLite (testing)
        if os.environ.get('TESTING') == 'True':
            cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
            player_id = cursor.lastrowid
        else:
            # For PostgreSQL
            cursor.execute("INSERT INTO players (name) VALUES (%s) RETURNING id", (name,))
            player_id = cursor.fetchone()[0]
        
        database_conn.commit()
        return player_id
    except (psycopg2.Error, sqlite3.Error) as error:
        logger.error("Error creating player '%s': %s", name, str(error))
        database_conn.rollback()
        return None

def create_game(player_id):
    """Create a new game for a player and return the game ID."""
    try:
        database_conn = get_db()
        cursor = database_conn.cursor()
        
        # For SQLite (testing)
        if os.environ.get('TESTING') == 'True':
            cursor.execute("INSERT INTO games (player_id, score) VALUES (?, 0)",
                          (player_id,))
            game_id = cursor.lastrowid
        else:
            # For PostgreSQL
            cursor.execute(
                "INSERT INTO games (player_id, score) VALUES (%s, 0) RETURNING id",
                (player_id,)
            )
            game_id = cursor.fetchone()[0]
        
        database_conn.commit()
        return game_id
    except (psycopg2.Error, sqlite3.Error) as error:
        if player_id:
            logger.error("Error creating game for player '%s': %s", player_id, str(error))
        else:
            logger.error("Error creating game, no player_id provided: %s", str(error))
        database_conn.rollback()
        return None

def update_score(game_id, score):
    """Update the score for a game."""
    try:
        database_conn = get_db()
        cursor = database_conn.cursor()
        
        # Same for both SQLite and PostgreSQL
        if os.environ.get('TESTING') == 'True':
            cursor.execute("UPDATE games SET score = ? WHERE id = ?", (score, game_id))
        else:
            cursor.execute("UPDATE games SET score = %s WHERE id = %s", (score, game_id))
        
        database_conn.commit()
        return True
    except (psycopg2.Error, sqlite3.Error) as error:
        logger.error("Error updating score for game_id '%s': %s", game_id, str(error))
        database_conn.rollback()
        return False

def record_attempt(game_id, answer_time):
    """Record an attempt for a game."""
    try:
        database_conn = get_db()
        cursor = database_conn.cursor()
        
        # For SQLite (testing)
        if os.environ.get('TESTING') == 'True':
            cursor.execute("INSERT INTO attempts (game_id, answer_time) VALUES (?, ?)",
                          (game_id, answer_time))
        else:
            # For PostgreSQL
            cursor.execute("INSERT INTO attempts (game_id, answer_time) VALUES (%s, %s)",
                          (game_id, answer_time))
        
        database_conn.commit()
        return True
    except (psycopg2.Error, sqlite3.Error) as error:
        logger.error("Error recording attempt for game_id '%s': %s", game_id, str(error))
        database_conn.rollback()
        return False

@app.teardown_appcontext
def teardown_db(_exception):
    """Teardown the database connection."""
    close_db()

@app.route('/health', methods=['GET'])
def health():
    """Return a simple health check response."""
    return "OK", 200

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=8080)
