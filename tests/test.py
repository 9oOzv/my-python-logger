import json
from log import log
from logging import (
    INFO,
    DEBUG,
)
from tests.utils import (
    assert_timestamp,
    assert_data,
)
from io import StringIO
import unittest
from pathlib import Path
import inspect
from typing import Any


data_dir = Path('tests/data')


class TestLog(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = log

    def test_meta(self):
        stream = StringIO()
        self.log.handlers[0].setStream(stream)
        log.info('Hello world!')
        line_number = inspect.currentframe().f_lineno
        logged = json.loads(stream.getvalue())
        assert_timestamp(logged['timestamp'])
        self.assertEqual(logged['level'], 'INFO')
        self.assertEqual(logged['funcName'], 'test_meta')
        self.assertEqual(logged['lineno'], line_number - 1)
        self.assertEqual(logged['pathname'], __file__)
        self.assertEqual(logged['module'], __name__)

    def _capture_log_message(
        self,
        message: Any,
        level: str = INFO
    ) -> dict:
        stream = StringIO()
        self.log.handlers[0].setStream(stream)
        log.log(level, message)
        v = stream.getvalue()
        if not v:
            return None
        else:
            return json.loads(stream.getvalue())

    def test_info(self):
        logged = self._capture_log_message('This is an info message.')
        self.assertEqual(logged['message'], 'This is an info message.')
        self.assertEqual(logged['level'], 'INFO')

    def test_debug_off(self):
        self.log.setLevel(INFO)
        logged = self._capture_log_message('This is a debug message.', DEBUG)
        self.assertIsNone(logged)

    def test_debug_on(self):
        self.log.setLevel(DEBUG)
        logged = self._capture_log_message('This is a debug message.', DEBUG)
        self.assertEqual(logged['message'], 'This is a debug message.')
        self.assertEqual(logged['level'], 'DEBUG')

    def test_one(self):
        data = json.loads((data_dir / 'one.json').read_text())
        logged = self._capture_log_message(data)
        assert_data(logged['message'], data)

    def test_two(self):
        data = json.loads((data_dir / 'two.json').read_text())
        logged = self._capture_log_message(data)
        assert_data(logged['message'], data)

    def test_too_deep(self):
        data = json.loads((data_dir / 'too_deep.json').read_text())
        truncated = json.loads(
            (data_dir / 'too_deep_truncated.json').read_text()
        )
        logged = self._capture_log_message(data)
        assert_data(logged['message'], truncated)

    def test_long_string(self):
        data = json.loads((data_dir / 'long_string.json').read_text())
        truncated = json.loads(
            (data_dir / 'long_string_truncated.json').read_text()
        )
        logged = self._capture_log_message(data)
        assert_data(logged['message'], truncated)

    def test_too_many_dict_items(self):
        data = json.loads((data_dir / 'too_many_dict_items.json').read_text())
        logged = self._capture_log_message(data)
        self.assertEqual(len(logged['message']), 64)
        for k, v in logged['message'].items():
            if k == '...':
                self.assertEqual(v, '...')
            else:
                self.assertEqual(v, data[k])

    def test_too_many_list_items(self):
        data = json.loads((data_dir / 'too_many_list_items.json').read_text())
        logged = self._capture_log_message(data)
        self.assertEqual(len(logged['message']), 64)
        for i, v in enumerate(logged['message']):
            if i == 63:
                self.assertEqual(v, '...')
            else:
                self.assertEqual(v, data[i])


if __name__ == '__main__':
    unittest.main()
