import sqlite3

def init_db():
    conn = sqlite3.connect('math_game.db')
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            score INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            answer_time FLOAT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    ''')

    conn.commit()
    conn.close()

    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()