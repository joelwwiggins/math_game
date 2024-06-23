import sqlite3

def init_db():
    conn = sqlite3.connect('math_game.db')
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            score INTEGER NOT NULL
        )
    ''')

    # Insert initial score if not exists
    c.execute('INSERT OR IGNORE INTO scores (id, score) VALUES (1, 0)')

    conn.commit()
    conn.close()

    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()