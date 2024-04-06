from flask import Flask, render_template, request, redirect, url_for
from dataclasses import dataclass, field
import random
import time
import json

app = Flask(__name__)

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
        return render_template('home.html')

    @app.route('/game', methods=['GET', 'POST'])
    def game():
        if request.method == 'POST':
            player_name = request.form['player_name']
            session = GameSession(player_name=player_name)
            return redirect(url_for('play', session=session))
        return render_template('game.html')

    @app.route('/play/<player_name>', methods=['GET', 'POST'])
    def play(player_name):
        # Note: For simplicity, a new session is created for each request.
        # In a real application, consider using Flask's session management to persist state.
        session = GameSession(player_name=player_name)

        if request.method == 'POST':
            user_answer = int(request.form['answer'])
            if user_answer == session.answer:
                # Correct answer, generate new question
                return render_template('play.html', session=session, message="Correct! Try another one.")
            else:
                # Wrong answer, update leaderboard
                leaderboard = load_leaderboard()
                end_time = time.time()
                time_taken = round(end_time - session.start_time, 2)
                leaderboard = update_leaderboard(leaderboard, player_name, time_taken)
                save_leaderboard(leaderboard)
                return redirect(url_for('leaderboard'))

        # Starting or continuing a game
        return render_template('play.html', session=session, message="")

    @app.route('/leaderboard')
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