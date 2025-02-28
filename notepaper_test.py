import unittest
import notepaper as p
import datetime


class TestAddingTodos(unittest.TestCase):
    def test_add_todos(self) -> None:
        orig = ["1", "2"]
        v = ["3", "4"]
        r = p.add_todos(orig, v)
        self.assertEqual(["1", "2", "3", "4"], r)

        orig = ["1", "", "2"]
        v = ["3"]
        r = p.add_todos(orig, v)
        self.assertEqual(["1", "3", "2"], r)
        # ensure that orig doesn't change
        self.assertEqual(["1", "", "2"], orig)

    def test_yearly_first_monday(self) -> None:
        todos = {"yearly": [{"March,Monday,1": "t"}]}

        # monday in other month
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 3)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 4)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 5)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 11)))

    def test_yearly_last_weekday(self) -> None:
        todos = {"yearly": [{"March,Monday,-1": "t"}]}

        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 18)))

    def test_yearly_any_monday(self) -> None:
        todos = {"yearly": [{"March,Monday,*": "t"}]}

        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 18)))

    def test_yearly_specific_date(self) -> None:
        todos = {"yearly": [{"March,Day,15": "t"}]}

        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 15)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 14)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 15)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 16)))

    def test_alternate_monthly_any_monday(self) -> None:
        todos = {"yearly": [{"*,Monday,*": "t"}]}

        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 24)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 25)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 26)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 3, 18)))

    def test_alternate_monthly_last_monday(self) -> None:
        todos = {"yearly": [{"*,Monday,-1": "t"}]}
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 22)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 1, 29)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 30)))

    def test_alternate_monthly_first_monday(self) -> None:
        todos = {"yearly": [{"*,Monday,1": "t"}]}
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2023, 12, 31)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 8)))

    def test_abbreviate_month_first_monday(self) -> None:
        todos = {"yearly": [{"Monday,1": "t"}]}
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2023, 12, 31)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 8)))

    def test_every_day_in_month(self) -> None:
        todos = {"yearly": [{"February,*,*": "t"}]}
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 8)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 3, 8)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 2, 8)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 2, 14)))

    def test_mixing(self) -> None:
        todos = {
            "yearly": [
                {"*,Saturday,*": ["Chess"], "March,Saturday,*": ["Check MCTP F28R32"]}
            ]
        }
        self.assertEqual(
            ["Chess", "Check MCTP F28R32"],
            p.get_day_todos(todos, datetime.date(2024, 3, 2)),
        )

    def test_dont_mess_the_orgiginals(self):
        todos = {
            "yearly": [
                {
                    "February,Saturday,4": ["u"],  # ac
                    "Saturday,4": ["w"],  # endo
                }
            ]
        }
        cur = datetime.date(2025, 2, 1)
        for i in range(28):
            p.get_day_todos(todos, cur)
            cur += p.ONE_DAY
        self.assertEqual(["u"], todos["yearly"][0]["February,Saturday,4"])

    def test_interval(self) -> None:
        # Every two weeks starting on 2025-01-01
        todos = {"yearly": [{"2024-01-01,week,2": "t"}]}
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 1, 1)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 8)))
        self.assertEqual(["t"], p.get_day_todos(todos, datetime.date(2024, 1, 15)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 2, 8)))
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 2, 14)))

    ### NEW
    def test_get_day_todos_recurring_weekly(self) -> None:
        todos = {"yearly": [{"2024-01-01,week,2": ["Biweekly meeting"]}]}

        # Should occur on start date
        self.assertEqual(
            ["Biweekly meeting"], p.get_day_todos(todos, datetime.date(2024, 1, 1))
        )
        # Should not occur one week later
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 8)))
        # Should occur two weeks later
        self.assertEqual(
            ["Biweekly meeting"], p.get_day_todos(todos, datetime.date(2024, 1, 15))
        )

    def test_get_day_todos_recurring_daily(self) -> None:
        todos = {"yearly": [{"2024-01-01,day,3": ["Every 3 days"]}]}

        self.assertEqual(
            ["Every 3 days"], p.get_day_todos(todos, datetime.date(2024, 1, 1))
        )
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 2)))
        self.assertEqual(
            ["Every 3 days"], p.get_day_todos(todos, datetime.date(2024, 1, 4))
        )

    def test_get_todos_last_day_of_month(self) -> None:
        todos = {"yearly": [{"Day,-1": ["Last day of month"]}]}
        self.assertEqual(
            ["Last day of month"], p.get_day_todos(todos, datetime.date(2024, 1, 31))
        )
        self.assertEqual([], p.get_day_todos(todos, datetime.date(2024, 1, 30)))

    def test_saturday_of_month(self) -> None:
        todos = {"yearly": [{"Saturday,2": ["Second Saturday of month"]}]}
        self.assertEqual(
            ["Second Saturday of month"],
            p.get_day_todos(todos, datetime.date(2024, 2, 10)),
        )
        todos = {"yearly": [{"Saturday,3": ["Third Saturday of month"]}]}
        self.assertEqual(
            ["Third Saturday of month"],
            p.get_day_todos(todos, datetime.date(2024, 2, 17)),
        )

    def test_get_day_todos_empty_slots(self) -> None:
        todos = {"yearly": [{"March,Monday,1": ["First", "", "Third"]}]}

        result = p.get_day_todos(todos, datetime.date(2024, 3, 4))
        self.assertEqual(["First", "Third"], result)

    def test_get_day_todos_month_weekday_star(self) -> None:
        todos = {"yearly": [{"March,Saturday,*": ["Weekend in March"]}]}

        # Should not occur in February
        self.assertEqual(
            [],
            p.get_day_todos(todos, datetime.date(2024, 2, 3)),  # A Saturday in February
        )

        # Should occur on all Saturdays in March
        self.assertEqual(
            ["Weekend in March"],
            p.get_day_todos(
                todos, datetime.date(2024, 3, 2)
            ),  # First Saturday in March
        )
        self.assertEqual(
            ["Weekend in March"],
            p.get_day_todos(
                todos, datetime.date(2024, 3, 9)
            ),  # Second Saturday in March
        )

        # Should not occur in April
        self.assertEqual(
            [], p.get_day_todos(todos, datetime.date(2024, 4, 6))  # A Saturday in April
        )

    def test_start_of_year(self):
        date = datetime.datetime(2024, 1, 1)
        result = p.get_week_info(date)
        self.assertEqual(result["week_of_year"], 1)
        self.assertEqual(result["quarter"], 1)
        self.assertEqual(result["week_of_quarter"], 1)

    def test_middle_of_year(self):
        date = datetime.datetime(2024, 6, 15)
        result = p.get_week_info(date)
        self.assertEqual(result["quarter"], 2)

    def test_end_of_year(self):
        date = datetime.datetime(2024, 12, 31)
        result = p.get_week_info(date)
        self.assertEqual(result["quarter"], 4)

    def test_week_in_quarter(self):
        date = datetime.datetime(2024, 4, 10)
        result = p.get_week_info(date)
        self.assertEqual(result["week_of_quarter"], 2)

