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
        todos = {"Day,-1": "t"}

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 1, 30), todos, []))

        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 31), todos, [])
        )

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 2, 1), todos, []))

    def testAddMonthlyRelativeDayPositive(self):
        todos = {"Day,1": "t"}

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 1, 31), todos, []))
        self.assertEqual(["t"], p.addMonthlyTodos(datetime.date(2024, 2, 1), todos, []))
        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 2, 2), todos, []))

    def testAddMonthlyFirstMonday(self):
        todos = {"Monday,1": "t"}

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2023, 12, 31), todos, []))
        self.assertEqual(["t"], p.addMonthlyTodos(datetime.date(2024, 1, 1), todos, []))
        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 1, 2), todos, []))

    def testAddMonthlyLastMonday(self):
        todos = {"Monday,-1": "t"}

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2023, 1, 22), todos, []))
        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 29), todos, [])
        )

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 1, 30), todos, []))

    def testAddMonthlyAnyMonday(self):
        todos = {"Monday,*": "t"}

        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 1, 21), todos, []))
        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 22), todos, [])
        )
        self.assertEqual(
            ["t"], p.addMonthlyTodos(datetime.date(2024, 1, 29), todos, [])
        )
        self.assertEqual([], p.addMonthlyTodos(datetime.date(2024, 1, 30), todos, []))

    def testYearlyFirstWeekday(self):
        todos = {"yearly": [{"March,Monday,1": "t"}], "monthly": [{}]}

        # monday in other month
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 3)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 4)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 5)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 11)))

    def testYearlyLastWeekday(self):
        todos = {"yearly": [{"March,Monday,-1": "t"}], "monthly": [{}]}

        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 18)))

    def testYearlyAnyMonday(self):
        todos = {"yearly": [{"March,Monday,*": "t"}], "monthly": [{}]}

        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 18)))

    def testYearlySpecificDate(self):
        todos = {"yearly": [{"March,Day,15": "t"}], "monthly": [{}]}

        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 15)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 14)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 15)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 16)))

    def testAlternateMonthlyAnyMonday(self):
        todos = {"yearly": [{"*,Monday,*": "t"}], "monthly": [{}]}

        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 3, 18)))

    def testAlternateMonthlyLastMonday(self):
        todos = {"yearly": [{"*,Monday,-1": "t"}], "monthly": [{}]}
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 22)))
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 30)))

    def testAlternateMonthlyFirstMonday(self):
        todos = {"yearly": [{"*,Monday,1": "t"}], "monthly": [{}]}
        self.assertEqual(["t"], p.getDayTodos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2023, 12, 31)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual([], p.getDayTodos(todos, datetime.date(2024, 1, 8)))
