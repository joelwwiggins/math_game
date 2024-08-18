import unittest
import sqlite3
from app import app, get_db, init_db, close_db, create_player

class MathGameTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            init_db()
            self.player_id = create_player('Test Player')

    def tearDown(self):
        """Tear down test environment."""
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM players")
            db.execute("DELETE FROM games")
            db.execute("DELETE FROM attempts")
            db.commit()
            close_db()

    def test_index_page(self):
        """Test the index page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Math Adventure!', response.data)

    def test_game_page(self):
        """Test the game page."""
        with self.app.session_transaction() as sess:
            sess['player_name'] = 'Test Player'
            sess['player_id'] = self.player_id
        response = self.app.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Test Player!', response.data)

    def test_results_page(self):
        """Test the results page."""
        with self.app.session_transaction() as sess:
            sess['player_name'] = 'Test Player'
            sess['player_id'] = self.player_id
            sess['num1'] = 20
            sess['num2'] = 22
        
        # Simulate playing a game
        self.app.post('/game', data={'answer': '42'})
        
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Adventure Results for Test Player', response.data)
        self.assertIn(b'Final Score:', response.data)
        self.assertIn(b'Your Answer Times:', response.data)

if __name__ == '__main__':
    unittest.main()
