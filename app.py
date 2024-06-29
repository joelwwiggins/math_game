from flask import Flask, render_template, request, redirect, url_for, session, g
import random
import sqlite3
from init_db import init_db as initialize_database
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key
app.config['DATABASE'] = 'math_game.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        initialize_database(app.config['DATABASE'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name = request.form['player_name']
        session['player_name'] = player_name
        create_player(player_name)
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
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
    db = get_db()
    attempts = db.execute('SELECT answer_time FROM attempts WHERE game_id = ? ORDER BY id',
                           (game_id,)).fetchall()
    return [attempt['answer_time'] for attempt in attempts]

def create_player(name):
    db = get_db()
    db.execute('INSERT OR IGNORE INTO players (name) VALUES (?)', (name,))
    db.commit()

def create_game(player_name):
    db = get_db()
    player_id = db.execute('SELECT id FROM players WHERE name = ?', (player_name,)).fetchone()['id']
    cursor = db.execute('INSERT INTO games (player_id, score) VALUES (?, 0)', (player_id,))
    game_id = cursor.lastrowid
    db.commit()
    return game_id

def update_score(game_id, score):
    db = get_db()
    db.execute('UPDATE games SET score = ? WHERE id = ?', (score, game_id))
    db.commit()

def record_attempt(game_id, answer_time):
    db = get_db()
    db.execute('INSERT INTO attempts (game_id, answer_time) VALUES (?, ?)', (game_id, answer_time))
    db.commit()

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
