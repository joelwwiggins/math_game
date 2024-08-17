"testing file"

import logging
import random
import sqlite3
import time
import os

from flask import Flask, render_template, request, redirect, url_for, session, g
from init_db import init_db as initialize_database

# Configure logging to a file
LOG_DIR = '/mnt/logs'
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # to also log to console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['DATABASE'] = '/mnt/db/math_game.db'

def get_db():
    """Get or create a database connection."""
    if 'db' not in g:
        # pylint: disable=assigning-non-slot
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    """Close the database connection."""
    database = g.pop('db', None)
    if database is not None:
        database.close()

def init_db():
    """Initialize the database."""
    db_path = app.config['DATABASE']
    initialize_database()  # Removed the argument
    logger.info("Database initialized at '%s'", db_path)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle the index route."""
    if request.method == 'POST':
        player_name = request.form['player_name']
        session['player_name'] = player_name
        create_player(player_name)
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    """Handle the game route."""
    if 'player_name' not in session:
        return redirect(url_for('index'))

    if 'game_id' not in session:
        session['game_id'] = create_game(session['player_name'])
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
    """Get all attempts for a given game."""
    database = get_db()
    attempts = database.execute('SELECT answer_time FROM attempts WHERE game_id = ? ORDER BY id',
                                (game_id,)).fetchall()
    return [attempt['answer_time'] for attempt in attempts]

def create_player(name):
    """Create a new player in the database."""
    try:
        database = get_db()
        database.execute('INSERT OR IGNORE INTO players (name) VALUES (?)', (name,))
        database.commit()
        logger.info("Player '%s' created successfully.", name)
    except sqlite3.Error as error:
        logger.error("Error creating player '%s': %s", name, error)

def create_game(player_name):
    """Create a new game in the database."""
    try:
        database = get_db()
        player_id = database.execute('SELECT id FROM players WHERE name = ?',
                                     (player_name,)).fetchone()['id']
        cursor = database.execute('INSERT INTO games (player_id, score) VALUES (?, 0)',
                                  (player_id,))
        game_id = cursor.lastrowid
        database.commit()
        logger.info("Game created successfully for player '%s' with game_id '%s'.",
                    player_name, game_id)
        return game_id
    except sqlite3.Error as error:
        logger.error("Error creating game for player '%s': %s", player_name, error)
        return None

def update_score(game_id, score):
    """Update the score for a given game."""
    try:
        database = get_db()
        database.execute('UPDATE games SET score = ? WHERE id = ?', (score, game_id))
        database.commit()
        logger.info("Score updated to '%s' for game_id '%s'.", score, game_id)
    except sqlite3.Error as error:
        logger.error("Error updating score for game_id '%s': %s", game_id, error)

def record_attempt(game_id, answer_time):
    """Record an attempt for a given game."""
    try:
        database = get_db()
        database.execute(
            'INSERT INTO attempts (game_id, answer_time) VALUES (?, ?)',
                        (game_id, answer_time))
        database.commit()
        logger.info("Attempt recorded for game_id '%s' with answer_time '%s'.",
                    game_id, answer_time)
    except sqlite3.Error as error:
        logger.error("Error recording attempt for game_id '%s': %s", game_id, error)

@app.teardown_appcontext
def teardown_db(_exception):
    """Teardown the database connection."""
    close_db()

if __name__ == '__main__':
    init_db()
    
