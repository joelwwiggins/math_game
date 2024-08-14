"""Unit tests for the Math Adventure game application."""

import os
import tempfile
import time
import unittest

from app import app, init_db, get_db


class MathGameTestCase(unittest.TestCase):
    """Test case for the Math Adventure game application."""

    def setUp(self):
        """Set up the test environment before each test."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        """Clean up the test environment after each test."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_index_page(self):
        """Test the index page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Math Adventure!', response.data)

    def test_game_page(self):
        """Test the game page."""
        response = self.client.post('/', data={'player_name': 'TestPlayer'},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, TestPlayer!', response.data)

    def test_correct_answer(self):
        """Test submitting a correct answer."""
        with self.client.session_transaction() as sess:
            sess['player_name'] = 'TestPlayer'
            sess['game_id'] = 1
            sess['score'] = 0
            sess['start_time'] = time.time()
            sess['num1'] = 5
            sess['num2'] = 3

        response = self.client.post('/game', data={'answer': '8'},
                                    follow_redirects=True)
        self.assertIn(b'Score: 1', response.data)

    def test_incorrect_answer(self):
        """Test submitting an incorrect answer."""
        with self.client.session_transaction() as sess:
            sess['player_name'] = 'TestPlayer'
            sess['game_id'] = 1
            sess['score'] = 0
            sess['start_time'] = time.time()
            sess['num1'] = 5
            sess['num2'] = 3

        response = self.client.post('/game', data={'answer': '7'},
                                    follow_redirects=True)
        self.assertIn(b'Score: 0', response.data)

    def test_results_page(self):
        """Test the results page."""
        with self.client.session_transaction() as sess:
            sess['player_name'] = 'TestPlayer'
            sess['game_id'] = 1
            sess['score'] = 5

        response = self.client.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Adventure Results for TestPlayer', response.data)
        self.assertIn(b'Final Score: 5', response.data)

    def test_create_player(self):
        """Test player creation in the database."""
        with app.app_context():
            db = get_db()
            db.execute('INSERT INTO players (name) VALUES (?)', ('TestPlayer',))
            db.commit()

            player = db.execute('SELECT * FROM players WHERE name = ?', ('TestPlayer',)).fetchone()
            self.assertIsNotNone(player)
            self.assertEqual(player['name'], 'TestPlayer')

    def test_create_game(self):
        """Test game creation in the database."""
        with app.app_context():
            db = get_db()
            db.execute('INSERT INTO players (name) VALUES (?)', ('TestPlayer',))
            db.commit()

            player_id = db.execute('SELECT id FROM players WHERE name = ?', ('TestPlayer',)).fetchone()['id']
            db.execute('INSERT INTO games (player_id, score) VALUES (?, 0)', (player_id,))
            db.commit()

            game = db.execute('SELECT * FROM games WHERE player_id = ?', (player_id,)).fetchone()
            self.assertIsNotNone(game)
            self.assertEqual(game['player_id'], player_id)
            self.assertEqual(game['score'], 0)

    def test_update_score(self):
        """Test updating the score in the database."""
        with app.app_context():
            db = get_db()
            db.execute('INSERT INTO players (name) VALUES (?)', ('TestPlayer',))
            db.commit()

            player_id = db.execute('SELECT id FROM players WHERE name = ?', ('TestPlayer',)).fetchone()['id']
            db.execute('INSERT INTO games (player_id, score) VALUES (?, 0)', (player_id,))
            db.commit()

            game_id = db.execute('SELECT id FROM games WHERE player_id = ?', (player_id,)).fetchone()['id']
            db.execute('UPDATE games SET score = ? WHERE id = ?', (10, game_id))
            db.commit()

            game = db.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
            self.assertEqual(game['score'], 10)

if __name__ == '__main__':
    unittest.main()
