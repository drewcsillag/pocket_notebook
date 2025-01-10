import unittest
import notepaper as p
import datetime


class TestAddingTodos(unittest.TestCase):
    def testAddTodos(self):
        orig = ["1", "2"]
        v = ["3", "4"]
        r = p.addTodos(orig, v)
        self.assertEqual(["1", "2", "3", "4"], r)

        orig = ["1", "", "2"]
        v = ["3"]
        r = p.addTodos(orig, v)
        self.assertEqual(["1", "3", "2"], r)
        # ensure that orig doesn't change
        self.assertEqual(["1", "", "2"], orig)

    def testAddMonthlyRelativeDayNegative(self):
        todo_dict = {"Day,-1": "t"}

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 1, 30), todo_dict, [])
        )

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 31), todo_dict, [])
        )

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 2, 1), todo_dict, [])
        )

    def testAddMonthlyRelativeDayPositive(self):
        todo_dict = {"Day,1": "t"}

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 1, 31), todo_dict, [])
        )

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 2, 1), todo_dict, [])
        )

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 2, 2), todo_dict, [])
        )

    def testAddMonthlyFirstMonday(self):
        todo_dict = {"Monday,1": "t"}

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2023, 12, 31), todo_dict, [])
        )

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 1), todo_dict, [])
        )

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 1, 2), todo_dict, [])
        )

    def testAddMonthlyLastMonday(self):
        todo_dict = {"Monday,-1": "t"}

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2023, 1, 22), todo_dict, [])
        )

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 29), todo_dict, [])
        )

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 1, 30), todo_dict, [])
        )

    def testAddMonthlyAnyMonday(self):
        todo_dict = {"Monday,*": "t"}

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 1, 21), todo_dict, [])
        )

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 22), todo_dict, [])
        )

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 29), todo_dict, [])
        )

        self.assertEqual(
            [], p.addMonthlyTodos(datetime.date(2024, 1, 30), todo_dict, [])
        )
