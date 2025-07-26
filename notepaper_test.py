"""Tests for svg generation -- sorta, but not really. More for the "math" of it."""

import unittest
import datetime

from todo_date_math import get_day_todos, get_week_info, add_todos
from constants import ONE_DAY


class TestAddingTodos(unittest.TestCase):  # pylint: disable=too-many-public-methods
    "Tests"

    def test_add_todos(self) -> None:
        "Test that adding todos works"
        orig = ["1", "2"]
        v = ["3", "4"]
        r = add_todos(orig, v)
        self.assertEqual(["1", "2", "3", "4"], r)

        orig = ["1", "", "2"]
        v = ["3"]
        r = add_todos(orig, v)
        self.assertEqual(["1", "3", "2"], r)
        # ensure that orig doesn't change
        self.assertEqual(["1", "", "2"], orig)

    def test_yearly_first_monday(self) -> None:
        "test that we can select the first Monday of a month"
        todos = {"March,Monday,1": "t"}

        # monday in other month
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 3)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 4)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 5)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 11)))

    def test_yearly_last_weekday(self) -> None:
        "test that we can find the last Monday of a month"
        todos = {"March,Monday,-1": "t"}

        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 18)))

    def test_yearly_any_monday(self) -> None:
        "TEest that we can find any Monday in march 2024"
        todos = {"March,Monday,*": "t"}

        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 18)))

    def test_yearly_specific_date(self) -> None:
        "test that we can find March 15th"
        todos = {"March,Day,15": "t"}

        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 15)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 14)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 15)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 16)))

    def test_alternate_monthly_any_monday(self) -> None:
        "test that we can find any Monday"
        todos = {"*,Monday,*": "t"}

        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 3, 18)))

    def test_alternate_monthly_last_monday(self) -> None:
        "test that we can find the last monday of any Month"
        todos = {"*,Monday,-1": "t"}
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 22)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 30)))

    def test_alternate_monthly_first_monday(self) -> None:
        "test that we can find first monday of any month"
        todos = {"*,Monday,1": "t"}
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2023, 12, 31)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 8)))

    def test_abbreviate_month_first_monday(self) -> None:
        "test that we can use the abbreviated form to find the first monday of any month"
        todos = {"Monday,1": "t"}
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2023, 12, 31)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 8)))

    def test_every_day_in_month(self) -> None:
        "test that we can select every day in February"
        todos = {"February,*,*": "t"}
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 8)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 3, 8)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 2, 8)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 2, 14)))

    def test_mixing(self) -> None:
        "test a bugfix where if we have two items with a similar selector that we find both"
        todos = {"*,Saturday,*": ["Chess"], "March,Saturday,*": ["Check MCTP F28R32"]}
        self.assertEqual(
            ["Chess", "Check MCTP F28R32"],
            get_day_todos(todos, datetime.date(2024, 3, 2)),
        )

    def test_dont_mess_the_orgiginals(self):
        """I don't remember why this was necessary, but probably was because of an
        aliasing/sharing bug"""
        todos = {
            "February,Saturday,4": ["u"],  # ac
            "Saturday,4": ["w"],  # endo
        }
        cur = datetime.date(2025, 2, 1)
        for _ in range(28):
            get_day_todos(todos, cur)
            cur += ONE_DAY
        self.assertEqual(["u"], todos["February,Saturday,4"])

    def test_interval(self) -> None:
        "Test for recurring items that are based on a date interval"
        # Every two weeks starting on 2025-01-01
        todos = {"2024-01-01,week,2": "t"}
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 8)))
        self.assertEqual(["t"], get_day_todos(todos, datetime.date(2024, 1, 15)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 2, 8)))
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 2, 14)))

    def test_get_day_todos_recurring_weekly(self) -> None:
        "test specific cases of fortnightly meeting"
        todos = {"2024-01-01,week,2": ["Biweekly meeting"]}

        # Should occur on start date
        self.assertEqual(
            ["Biweekly meeting"], get_day_todos(todos, datetime.date(2024, 1, 1))
        )
        # Should not occur one week later
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 8)))
        # Should occur two weeks later
        self.assertEqual(
            ["Biweekly meeting"], get_day_todos(todos, datetime.date(2024, 1, 15))
        )

    def test_get_day_todos_recurring_daily(self) -> None:
        "test that a recurrence based on days works"
        todos = {"2024-01-01,day,3": ["Every 3 days"]}

        self.assertEqual(
            ["Every 3 days"], get_day_todos(todos, datetime.date(2024, 1, 1))
        )
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual(
            ["Every 3 days"], get_day_todos(todos, datetime.date(2024, 1, 4))
        )

    def test_get_todos_last_day_of_month(self) -> None:
        "test selecting the last day of the month for all months"
        todos = {"Day,-1": ["Last day of month"]}
        self.assertEqual(
            ["Last day of month"], get_day_todos(todos, datetime.date(2024, 1, 31))
        )
        self.assertEqual([], get_day_todos(todos, datetime.date(2024, 1, 30)))

    def test_saturday_of_month(self) -> None:
        "test picking saturdays of any month"
        todos = {"Saturday,2": ["Second Saturday of month"]}
        self.assertEqual(
            ["Second Saturday of month"],
            get_day_todos(todos, datetime.date(2024, 2, 10)),
        )
        todos = {"Saturday,3": ["Third Saturday of month"]}
        self.assertEqual(
            ["Third Saturday of month"],
            get_day_todos(todos, datetime.date(2024, 2, 17)),
        )

    def test_get_day_todos_empty_slots(self) -> None:
        "test handling empty messages"
        todos = {"March,Monday,1": ["First", "", "Third"]}

        result = get_day_todos(todos, datetime.date(2024, 3, 4))
        self.assertEqual(["First", "Third"], result)

    def test_get_day_todos_month_weekday_star(self) -> None:
        "test handling * in the last item where month and dow are spec'd"
        todos = {"March,Saturday,*": ["Weekend in March"]}

        # Should not occur in February
        self.assertEqual(
            [],
            get_day_todos(todos, datetime.date(2024, 2, 3)),  # A Saturday in February
        )

        # Should occur on all Saturdays in March
        self.assertEqual(
            ["Weekend in March"],
            get_day_todos(todos, datetime.date(2024, 3, 2)),  # First Saturday in March
        )
        self.assertEqual(
            ["Weekend in March"],
            get_day_todos(todos, datetime.date(2024, 3, 9)),  # Second Saturday in March
        )

        # Should not occur in April
        self.assertEqual(
            [], get_day_todos(todos, datetime.date(2024, 4, 6))  # A Saturday in April
        )

    ##### Week, quarter, week in quarter tests

    def test_start_of_year(self):
        "test the bottom of page markers for quarter, week, and week of quarter"
        date = datetime.date(2024, 1, 1)
        result = get_week_info(date)
        self.assertEqual(result["week_of_year"], 1)
        self.assertEqual(result["quarter"], 1)
        self.assertEqual(result["week_of_quarter"], 1)

    def test_middle_of_year(self):
        "test quarter for not quite 3rd quarter"
        date = datetime.date(2024, 6, 15)
        result = get_week_info(date)
        self.assertEqual(result["quarter"], 2)

    def test_end_of_year(self):
        "test quarter info for end of year"
        date = datetime.date(2024, 12, 31)
        result = get_week_info(date)
        self.assertEqual(result["quarter"], 4)

    def test_week_in_quarter(self):
        "test week in quarter"
        date = datetime.date(2024, 4, 10)
        result = get_week_info(date)
        self.assertEqual(result["week_of_quarter"], 2)
