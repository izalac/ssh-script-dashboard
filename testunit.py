import unittest
import os
import json
import app as main_app
import envexecute as ex
from unittest.mock import patch, MagicMock

class TestSSHScriptDashboard(unittest.TestCase):
    def setUp(self):
        # Create a test app
        self.app = main_app.create_app({
            'TESTING': True,
            'COMMANDS': {
                'test-command': 'echo "hello world"',
                'error-command': 'exit 1'
            }
        })
        self.client = self.app.test_client()

    def test_index_page(self):
        """Test the main landing page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SSH Script Dashboard', response.data)
        self.assertIn(b'test-command', response.data)

    def test_run_script_success(self):
        """Test running a script successfully."""
        with patch('envexecute.local_execute') as mocked_exec:
            mocked_exec.return_value = "hello world<br />"
            response = self.client.get('/scripts/test-command')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'hello world', response.data)

    def test_run_script_not_found(self):
        """Test running a non-existent script."""
        response = self.client.get('/scripts/non-existent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)

    def test_local_execute(self):
        """Test the local_execute function directly."""
        result = ex.local_execute('echo "test output"')
        self.assertIn('test output', result)
        self.assertIn('<br />', result)

    def test_default_execute_fallback(self):
        """Test default_execute fallback to local."""
        with patch.dict(os.environ, {'EXECUTE_MODEL': 'unknown'}):
            result = ex.default_execute('echo "fallback"')
            self.assertIn('fallback', result)

    @patch('fabric.Connection')
    def test_remote_connection_error(self, mock_conn):
        """Test remote connection failure."""
        mock_conn.side_effect = Exception("Connection failed")
        with patch.dict(os.environ, {
            'EXECUTE_MODEL': 'remote',
            'REMOTESERVER': 'test-server',
            'REMOTEUSER': 'test-user',
            'REMOTECERT': 'test-cert'
        }):
            # Clear previous connection if any
            ex._server_connection = None
            with self.assertRaises(Exception) as cm:
                ex.get_server_connection()
            self.assertIn("Remote connection to test-server failed", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
