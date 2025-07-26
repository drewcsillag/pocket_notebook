"""Tests for yaml_loading"""

import unittest
import io

from yaml_load import parse_preserving_duplicates

class TestAddingTodos(unittest.TestCase):  # pylint: disable=too-many-public-methods
    "Tests"

    def test_load(self):
        """test that loading without a top level heading loads the way we want"""
        y = io.StringIO("""
February,*,*: Read

#### DAILY
"*,*": 3 grateful
"*,*": 10m stop 
"*,*": walk
""")
        d = parse_preserving_duplicates(y)
        self.assertEqual(d['February,*,*'], ['Read'])
        res = d['*,*']
        res.sort()
        self.assertEqual(res, ['10m stop', '3 grateful', 'walk'])
