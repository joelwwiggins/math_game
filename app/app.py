from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize SQLite database
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE scores (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER)")

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/scores', methods=['GET'])
def get_scores():
    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()
    return jsonify(scores=[{"name": row[0], "score": row[1]} for row in rows])

@app.route('/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (data['name'], data['score']))
    conn.commit()
    return jsonify(id=cursor.lastrowid)

if __name__ == '__main__':
    app.run(port=3000)
