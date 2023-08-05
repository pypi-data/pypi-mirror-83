"""
Test some config parsing.
"""
import pathlib
from unittest import TestCase

from lib.config import parse_config


class Test(TestCase):
    def test_parse_config(self):
        config = parse_config("{'test':'test'}")
        self.assertEqual(config['test'], 'test')

    def test_parse_from_file(self):
        config = parse_config(pathlib.Path('./test/config/test.conf').read_text())
        self.assertEqual(config['Test'], 'T')
