from notepaper import parse_preserving_duplicates, get_day_todos, ONE_DAY, DAYS
import sys
import datetime


if __name__ == "__main__":
    todos = parse_preserving_duplicates(open("todo_holidays/todos.yaml"))
    holidays = parse_preserving_duplicates(open("todo_holidays/holidays.yaml"))
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