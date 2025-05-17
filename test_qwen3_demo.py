import unittest
from unittest import mock
import sys

# Provide a dummy gradio module so qwen3_demo can be imported without the real
# dependency installed during tests.
sys.modules.setdefault("gradio", mock.MagicMock())

import qwen3_demo


class TestRunOllama(unittest.TestCase):
    def test_missing_command(self):
        with mock.patch.object(qwen3_demo, 'OLLAMA_CMD', None), \
             mock.patch('shutil.which', return_value=None):
            result = qwen3_demo._run_ollama('hi')
        self.assertIn('ollama command not found', result.lower())

    def test_success(self):
        with mock.patch.object(qwen3_demo, 'OLLAMA_CMD', None) as _cmd, \
             mock.patch('shutil.which', return_value='/usr/bin/ollama'):
            fake_proc = mock.Mock(stdout='ok')
            with mock.patch('subprocess.run', return_value=fake_proc):
                out = qwen3_demo._run_ollama('prompt')
                # OLLAMA_CMD should be cached after successful execution
                self.assertEqual(qwen3_demo.OLLAMA_CMD, '/usr/bin/ollama')
                self.assertEqual(out, 'ok')


if __name__ == '__main__':
    unittest.main()
