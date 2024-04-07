from flask import Flask, render_template, request, redirect, url_for, session
from dataclasses import dataclass, field
import random
import time
import json
from flask_session import Session  # You might need to install this with pip

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to a random secret key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@dataclass
class GameSession:
    player_name: str
    start_time: float = field(default_factory=time.time)
    num1: int = field(default_factory=lambda: random.randint(1, 10))
    num2: int = field(default_factory=lambda: random.randint(1, 10))
    answer: int = field(init=False)

    def __post_init__(self):
        self.answer = self.num1 + self.num2

    def question(self):
        return f"{self.num1} + {self.num2} = ?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        player_name = request.form['player_name']
        game_session = GameSession(player_name=player_name)
        session['game_session'] = game_session.__dict__
        return redirect(url_for('play'))
    return render_template('game.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    # Ensure that a game session exists in the session. If not, redirect to start a new game.
    if 'game_session' not in session or 'player_name' not in session:
        # Optionally, show an error message or redirect to '/game' to start a new game
        return redirect(url_for('game'))
    
    # If the method is POST, process the submitted answer
    if request.method == 'POST':
        user_answer = request.form.get('answer', type=int, default=None)
        game_session = GameSession(**session['game_session'])
        
        if user_answer is not None and user_answer == game_session.answer:
            # Answer is correct; create a new question and update session
            message = "Correct! Try another one."
            new_session = GameSession(player_name=game_session.player_name)
            session['game_session'] = new_session.__dict__
        else:
            # Answer is incorrect or not provided; retain the current question
            message = f"Wrong! The correct answer was {game_session.answer}." if user_answer is not None else ""
        
        return render_template('play.html', session=session['game_session'], message=message)
    
    # GET request: simply display the current question
    return render_template('play.html', session=session['game_session'], message="")

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    leaderboard = load_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard)

def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as file:
            leaderboard = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}
    return leaderboard

def save_leaderboard(leaderboard):
    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file)

def update_leaderboard(leaderboard, player_name, time_taken):
    if player_name not in leaderboard or time_taken < leaderboard[player_name]:
        leaderboard[player_name] = time_taken
    return leaderboard

if __name__ == '__main__':
    app.run(debug=True)
