from unittest import TestCase

from lib.expand import expand_sql


class Test(TestCase):
    def test_expand_sql(self):
        self.assertEqual("INSERT INTO `Test` (`table`) VALUES ('value');",
                         expand_sql({'Test': 'T', 'table': 't', 'value': 'v'},
                                    'I T t v'))
