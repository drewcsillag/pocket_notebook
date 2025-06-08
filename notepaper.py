"""Driver program for page generation"""

import sys
from typing import TextIO, Dict, Any
import datetime
from collections import defaultdict
import yaml

from utils import create_output_file
from constants import RIGHT_PAGES, LEFT_PAGES, DAYS, MONTHS, ONE_DAY
from svg_gen import (
    make_date_page,
    make_monthly_pages,
    make_dated_monthly_pages_p1,
    make_dated_monthly_pages_p2,
    make_dated_monthly_pages_p3,
    make_dated_monthly_pages_p4,
    make_blank_pages,
    make_front_page,
)


def parse_preserving_duplicates(src: TextIO) -> Dict:
    """Parse yaml, but handle duplicate keys by having the values be lists instead
    of whatever they would be"""

    # We deliberately define a fresh class inside the function,
    # because add_constructor is a class method and we don't want to
    # mutate pyyaml classes.
    class PreserveDuplicatesLoader(yaml.loader.Loader): # pylint: disable=too-many-ancestors
        """Loader that preserves duplicate key values"""

    def map_constructor(loader: Any, node: Any, deep: Any = False) -> Any:
        """Walk the mapping, recording any duplicate keys."""

        mapping = defaultdict(list)
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            value = loader.construct_object(value_node, deep=deep)

            mapping[key].append(value)

        # print("RESULT MAPPING", mapping)
        return mapping

    PreserveDuplicatesLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, map_constructor
    )  # type: ignore
    return yaml.load(src, PreserveDuplicatesLoader)


def main():
    """The kickoff"""
    todos_file = "todo_holidays/todos.yaml"
    holidays_file = "todo_holidays/holidays.yaml"
    if len(sys.argv) == 5:
        todos_file, holidays_file = sys.argv[-2:]
    with open(todos_file, encoding="utf-8") as file:
        todos = parse_preserving_duplicates(file)
    with open(holidays_file, encoding="utf-8") as file:
        holidays = parse_preserving_duplicates(file)
    cur = datetime.date.fromisoformat(sys.argv[1])
    orig_year = cur.year
    numdays = int(sys.argv[2])
    numsplits = numdays / 2
    if numsplits != int(numsplits):
        print("must specify an even number of days {numsplits} {numsplits:i}")
        sys.exit(1)
    numsplits = int(numsplits)

    year = generate_dated_pages(todos, holidays, cur, numsplits)

    sys.stdout = create_output_file("monthly1.svg")
    make_monthly_pages()
    sys.stdout = create_output_file("monthly2.svg")
    make_monthly_pages()

    sys.stdout = create_output_file("monthly_dated1.svg")
    make_dated_monthly_pages_p1(orig_year)
    sys.stdout = create_output_file("monthly_dated2.svg")
    make_dated_monthly_pages_p2(orig_year)
    sys.stdout = create_output_file("monthly_dated3.svg")
    make_dated_monthly_pages_p3(orig_year)
    sys.stdout = create_output_file("monthly_dated4.svg")
    make_dated_monthly_pages_p4(orig_year)

    sys.stdout = create_output_file("blank1.svg")
    make_blank_pages(False, year=year)
    sys.stdout = create_output_file("blank2.svg")
    make_blank_pages(True, year=year)

    sys.stdout = create_output_file("header_r.svg")
    make_front_page(year=year, left=True)
    sys.stdout = create_output_file("header_l.svg")

    make_front_page(year=year, left=False)


def generate_dated_pages(
    todos: dict, holidays: dict, cur: datetime.date, numsplits: int
):
    """Generate dated page svgs"""
    minipageno = 0
    p1 = []
    p2 = []
    for _ in range(numsplits):
        p1.append(
            (
                RIGHT_PAGES[minipageno],
                DAYS[cur.weekday()],
                cur.day,
                MONTHS[cur.month],
                cur.year,
                cur,
            )
        )
        cur += ONE_DAY

        p2.append(
            (
                LEFT_PAGES[minipageno],
                DAYS[cur.weekday()],
                cur.day,
                MONTHS[cur.month],
                cur.year,
                cur,
            )
        )
        cur += ONE_DAY

        minipageno += 1
        if minipageno == 4:
            minipageno = 0

        # used way below
        year = cur.year

    num_sheets = int(len(p1) / 4)
    if len(p1) % 4:
        num_sheets += 1

    for p in range(num_sheets):
        make_date_page(left=False, p=p, px=p1[:4], todos=todos, holidays=holidays)
        make_date_page(left=True, p=p, px=p2[:4], todos=todos, holidays=holidays)

        p1 = p1[4:]
        p2 = p2[4:]
    return year


if __name__ == "__main__":
    main()
