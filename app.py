from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

def get_db_connection():
    conn = sqlite3.connect('math_game.db')
    conn.row_factory = sqlite3.Row
    return conn

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

    return render_template('game.html', num1=session['num1'], num2=session['num2'], score=session['score'], player_name=session['player_name'])

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

    return render_template('results.html', attempts=attempts, player_name=player_name, score=score)

def get_attempts(game_id):
    conn = get_db_connection()
    attempts = conn.execute('SELECT answer_time FROM attempts WHERE game_id = ? ORDER BY id', (game_id,)).fetchall()
    conn.close()
    return [attempt['answer_time'] for attempt in attempts]

def create_player(name):
    conn = get_db_connection()
    conn.execute('INSERT OR IGNORE INTO players (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def create_game(player_name):
    conn = get_db_connection()
    player_id = conn.execute('SELECT id FROM players WHERE name = ?', (player_name,)).fetchone()['id']
    cursor = conn.execute('INSERT INTO games (player_id, score) VALUES (?, 0)', (player_id,))
    game_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return game_id

def update_score(game_id, score):
    conn = get_db_connection()
    conn.execute('UPDATE games SET score = ? WHERE id = ?', (score, game_id))
    conn.commit()
    conn.close()

def record_attempt(game_id, answer_time):
    conn = get_db_connection()
    conn.execute('INSERT INTO attempts (game_id, answer_time) VALUES (?, ?)', (game_id, answer_time))
    conn.commit()
    conn.close()



if __name__ == '__main__':
    app.run(debug=True)