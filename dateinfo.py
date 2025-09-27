# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "python-dateutil",
#     "pyyaml",
# ]
# ///
"""test to load ing todos and holidays and do what's what"""
import sys
import datetime

from notepaper import parse_preserving_duplicates
from constants import ONE_DAY, DAYS
from svg_gen import get_day_todos


if __name__ == "__main__":
    with open("todo_holidays/todos.yaml", encoding="utf-8") as file:
        todos = parse_preserving_duplicates(file)
    with open("todo_holidays/holidays.yaml", encoding="utf-8") as file:
        holidays = parse_preserving_duplicates(file)
    cur = datetime.date.fromisoformat(sys.argv[1])
    numdays = int(sys.argv[2])

    for i in range(numdays):
        print("--------")
        print(cur, DAYS[cur.weekday()])
        t = get_day_todos(todos, cur)
        h = get_day_todos(holidays, cur)
        if t:
            print("TODOS:")
            print(t)
        if h:
            print("HOLIDAY:")
            print(h)
        cur += ONE_DAY
