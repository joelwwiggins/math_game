import unittest
import sqlite3
from app import app, get_db, init_db, close_db

class MathGameTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            init_db()

    def tearDown(self):
        """Tear down test environment."""
        with app.app_context():
            close_db()

    def test_index_page(self):
        """Test the index page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Math Game', response.data)

    def test_game_page(self):
        """Test the game page."""
        response = self.app.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Start Game', response.data)

    def test_results_page(self):
        """Test the results page."""
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Game Results', response.data)

if __name__ == '__main__':
    unittest.main()