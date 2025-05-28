import unittest
from unittest.mock import patch, MagicMock
import os

# It's often better to import the module under test once, if possible,
# but here reload is used, so patching 'dotenv.load_dotenv' which is used by app.config
# is more direct.

class TestConfig(unittest.TestCase):

    @patch('dotenv.load_dotenv') # Corrected patch target
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_db_url(self, mock_dotenv_load_dotenv: MagicMock):
        with self.assertRaisesRegex(RuntimeError, "DB_URL environment variable not set."):
            # Temporarily remove other required vars to isolate the test
            with patch.dict(os.environ, {"OPENAI_API_KEY": "test", "SUBMISSION_DEADLINE": "test"}):
                import importlib
                import app.config # app.config will use the mocked dotenv.load_dotenv
                importlib.reload(app.config)

    @patch('dotenv.load_dotenv') # Corrected patch target
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_openai_api_key(self, mock_dotenv_load_dotenv: MagicMock):
        with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY environment variable not set."):
            with patch.dict(os.environ, {"DB_URL": "test", "SUBMISSION_DEADLINE": "test"}):
                import importlib
                import app.config
                importlib.reload(app.config)

    @patch('dotenv.load_dotenv') # Corrected patch target
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_submission_deadline(self, mock_dotenv_load_dotenv: MagicMock):
        with self.assertRaisesRegex(RuntimeError, "SUBMISSION_DEADLINE environment variable not set."):
            with patch.dict(os.environ, {"DB_URL": "test", "OPENAI_API_KEY": "test"}):
                import importlib
                import app.config
                importlib.reload(app.config)

    @patch('dotenv.load_dotenv') # Corrected patch target
    @patch.dict(os.environ, {
        "DB_URL": "sqlite:///./test.db",
        "OPENAI_API_KEY": "fake_key",
        "SUBMISSION_DEADLINE": "2024-12-31T23:59:59Z"
    })
    def test_all_variables_present(self, mock_dotenv_load_dotenv: MagicMock):
        try:
            import importlib
            import app.config
            importlib.reload(app.config) # This will call the mocked dotenv.load_dotenv
            self.assertEqual(app.config.DB_URL, "sqlite:///./test.db")
            self.assertEqual(app.config.OPENAI_API_KEY, "fake_key")
            self.assertEqual(app.config.SUBMISSION_DEADLINE, "2024-12-31T23:59:59Z")
        except RuntimeError:
            self.fail("RuntimeError raised unexpectedly when all env vars are present.")

if __name__ == '__main__':
    unittest.main()
