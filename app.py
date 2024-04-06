import random
import time
import json
from dataclasses import dataclass, asdict
from flask import Flask, render_template, request, redirect, url_for
import random
import time
import json
from dataclasses import dataclass, asdict


app = Flask(__name__)

@dataclass

class PlayerScore:
    player: str
    score: int

    def to_dict(self):
        return asdict(self)

 

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = []
    return leaderboard

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

 
def update_leaderboard(leaderboard, player, score):
    player_score = PlayerScore(player, score)
    leaderboard.append(player_score.to_dict())
    leaderboard.sort(key=lambda x: x["score"])
    leaderboard = leaderboard[:3]
    return leaderboard


def math_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    answer = num1 + num2
    question = f"{num1} + {num2} = ?"
    return num1, num2, answer


def main():
    leaderboard = load_leaderboard()
    name = input("What is your name? ")
    correct = True
    start_time = time.time()
    while correct:
        num1, num2, correct_answer = math_question()
        print(f"Hello {name}! Let's play a math game! what is {num1} + {num2}?")
        user_answer = int(input("Your answer: "))
        if user_answer == correct_answer:
            print(f"Correct!")
        else:
            correct = False
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print(f"Wrong! The correct answer is {correct_answer}. It took you {time_taken} seconds.")
            leaderboard = update_leaderboard(leaderboard, name, time_taken)
 
    save_leaderboard(leaderboard)
    print("\nAll time best scores:")
    for player_score in leaderboard:
        player = player_score['player']
        score = player_score['score']
        print(f"{player}: {score}")
 
if __name__ == "__main__":
    main()