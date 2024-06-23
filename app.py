from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

def get_db_connection():
    conn = sqlite3.connect('math_game.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        session['score'] = get_score()

    if request.method == 'POST':
        user_answer = int(request.form['answer'])
        correct_answer = session['num1'] + session['num2']
        
        if user_answer == correct_answer:
            session['score'] += 1
            update_score(session['score'])
        
        return redirect(url_for('game'))

    session['num1'] = random.randint(0, 10)
    session['num2'] = random.randint(0, 10)

    return render_template('game.html', num1=session['num1'], num2=session['num2'], score=session['score'])

def get_score():
    conn = get_db_connection()
    score = conn.execute('SELECT score FROM scores WHERE id = 1').fetchone()['score']
    conn.close()
    return score

def update_score(score):
    conn = get_db_connection()
    conn.execute('UPDATE scores SET score = ? WHERE id = 1', (score,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
