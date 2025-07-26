"code to do date math with the todo and holiday stuff"
import datetime
from typing import List

from dateutil.relativedelta import relativedelta

from constants import DAYS, MONTHS, ONE_DAY
def get_week_info(date):
    """get the components for what goes into the week/quarter stamp at the bottom of pages"""
    # Get the week number of the year
    week_of_year = date.isocalendar()[1]

    # Determine the quarter
    quarter = (date.month - 1) // 3 + 1

    # Get the first day of the quarter
    first_day_of_quarter = datetime.datetime(date.year, (quarter - 1) * 3 + 1, 1).date()

    # Get the week number within the quarter
    week_of_quarter = (date - first_day_of_quarter).days // 7 + 1

    return {
        "week_of_year": week_of_year,
        "quarter": quarter,
        "week_of_quarter": week_of_quarter,
    }


def add_todos(t: List[str], v: List[str]) -> List[str]:
    """Add todos from v to t and return a new t"""
    t = t[:]
    for i in v:
        if "" in t:
            ind = t.index("")
            t[ind] = i
        else:
            t.append(i)
    return t


def get_day_todos(todos: dict, date: datetime.date) -> list[str]:
    """Get todos for a specific date from yearly todo configurations.

    Args:
        todos: Dictionary of todo configurations
        date: Date to get todos for

    Returns:
        List of todo strings for the given date
    """
    result = []

    if not todos:
        return result

    for pattern, tasks in todos.items():
        if not tasks:  # Skip empty tasks
            continue

        if pattern[0].isdigit():
            result.extend(get_recurring_todos(pattern, tasks, date))
        else:
            result.extend(get_pattern_todos(pattern, tasks, date))

    return result


def get_recurring_todos(
    pattern: str, tasks: list[str] | str, date: datetime.date
) -> list[str]:
    """Handle recurring interval patterns like '2024-01-01,week,2'"""
    start_date_str, unit, interval = pattern.split(",")
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    interval = int(interval)

    days_since_start = (date - start_date).days
    if days_since_start < 0:
        return []

    if unit == "week" and days_since_start % (7 * interval) == 0:
        return _normalize_tasks(tasks)
    if unit == "day" and days_since_start % interval == 0:
        return _normalize_tasks(tasks)

    return []


def get_pattern_todos(
    pattern: str, tasks: list[str] | str, date: datetime.date
) -> list[str]:
    """Handle patterns like 'January,Monday,1' or 'Monday,1'"""
    parts = pattern.split(",")

    # Handle abbreviated patterns (e.g. "Monday,1")
    if len(parts) == 2:
        parts = ["*", parts[0], parts[1]]  # Prepend "*" for any month

    month_pattern, day_type, occurrence = parts

    # Check if month matches
    if not _is_matching_month(month_pattern, date):
        return []

    if day_type == "Day":
        if _is_matching_day(int(occurrence), date):
            return _normalize_tasks(tasks)
    elif day_type in DAYS:
        if _is_matching_weekday(day_type, occurrence, date):
            return _normalize_tasks(tasks)
    elif day_type == "*" and occurrence == "*":
        return _normalize_tasks(tasks)

    return []


def _normalize_tasks(tasks: list[str] | str) -> list[str]:
    """Convert tasks to list format and filter empty strings"""
    if isinstance(tasks, list):
        return [t for t in tasks if t]
    return [tasks] if tasks else []


def _is_matching_month(month_pattern: str, date: datetime.date) -> bool:
    """Check if date's month matches the pattern"""
    return month_pattern in ("*", MONTHS[date.month])


def _is_matching_day(target_day: int, date: datetime.date) -> bool:
    """Check if date matches the target day of month"""
    if target_day < 0:  # Handle negative day numbers (counting from end)
        next_month = date + relativedelta(months=1, day=1)
        last_day = (next_month - ONE_DAY).day
        return date.day == (last_day + target_day + 1)
    return date.day == target_day


def _is_matching_weekday(day_type: str, occurrence: str, date: datetime.date) -> bool:
    """Check if a date matches a weekday pattern like 'Monday,2' (2nd Monday)
    or 'Friday,-1' (last Friday).

    Args:
        day_type: Name of weekday (e.g., "Monday", "Tuesday")
        occurrence: Which occurrence to match ("*" for any, or number like "2" or "-1")
        date: The date to check
    """
    # First check if it's the right day of the week
    if date.strftime("%A") != day_type:
        return False

    # "*" means match any occurrence of this weekday
    if occurrence == "*":
        return True

    # Find the date of the first occurrence of this weekday in the month
    first_of_month = date.replace(day=1)
    days_to_first = (DAYS.index(day_type) - first_of_month.weekday()) % 7
    first_occurrence_date = days_to_first + 1

    # Find which occurrence number this date represents (1st, 2nd, 3rd, etc.)
    if date.day < first_occurrence_date:
        return False
    this_occurrence = ((date.day - first_occurrence_date) // 7) + 1

    # For negative occurrences (like -1 for last), we need total occurrences in month
    target = int(occurrence)
    if target > 0:
        return this_occurrence == target

    # Calculate how many times this weekday occurs in the month
    last_of_month = (first_of_month + relativedelta(months=1, days=-1)).day
    total_occurrences = (last_of_month - first_occurrence_date + 7) // 7

    # Convert negative occurrence (-1 means last, -2 means second-to-last, etc.)
    target_from_end = total_occurrences + target + 1
    return this_occurrence == target_from_end


def is_recurring_interval(pattern: str) -> bool:
    """Check if pattern is a recurring interval (e.g. '2025-01-01,week,3')"""
    return pattern.split(",")[0][0] in "0123456789"


def should_add_recurring_todo(pattern: str, d_obj: datetime.date) -> bool:
    """Check if recurring todo should be added for given date"""
    date, unit, interval = pattern.split(",")
    start_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    numdays = {"week": 7, "day": 1}[unit]

    datediff_days = (d_obj - start_date.date()).days
    return datediff_days % (int(interval) * numdays) == 0
