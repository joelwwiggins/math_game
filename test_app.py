import unittest
from app import app, init_db
import tempfile
import os

class MathGameTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Math Adventure!', response.data)

    def test_game_page(self):
        self.client.post('/', data=dict(player_name='TestPlayer'))
        response = self.client.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, TestPlayer!', response.data)

    def test_correct_answer(self):
        self.client.post('/', data=dict(player_name='TestPlayer'))
        with self.client.session_transaction() as sess:
            sess['num1'] = 5
            sess['num2'] = 3
        response = self.client.post('/game', data=dict(answer='8'))
        self.assertIn(b'Current Score: 1', response.data)

if __name__ == '__main__':
    unittest.main()