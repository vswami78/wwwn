import unittest
# If app.py is in the app directory and you run tests from the root:
from app.app import ping # Corrected import path

class TestApp(unittest.TestCase):

    def test_ping(self):
        self.assertEqual(ping(), "OK", "ping() function should return 'OK'")

if __name__ == '__main__':
    unittest.main()
