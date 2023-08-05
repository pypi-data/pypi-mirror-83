from unittest import TestCase

from lib.compress import compress_sql


class Test(TestCase):
    def test_compress_sql(self):
        self.assertEqual('I T t v', compress_sql({'Test': 'T', 'table': 't', 'value': 'v'},
                                                 "INSERT INTO `Test` (`table`) VALUES ('value');"))
