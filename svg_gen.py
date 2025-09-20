"""
Generate SVG output for organizer pages
"""

import sys
from typing import List, Tuple, Optional
import datetime

from dateutil.relativedelta import relativedelta

from utils import create_output_file
from constants import (
    MONTHS,
    PITCH,
    ONE_DAY,
    LINE_THICKNESS,
    COLOR,
    DOT_COLOR,
    DOT_Y_OFFSET,
    DOT_RADIUS,
    RIGHT_PAGES,
    LEFT_PAGES,
)
from todo_date_math import get_day_todos, get_week_info


def make_monthly_sheet(org_x: int, org_y: int) -> None:
    """
    Create undated monthly calendar sheet
    """
    org_x += 2
    x = org_x + 4
    y = org_y + 16
    do_monthly_sheet(x, y)


def make_dated_monthly_sheet(org_x: int, org_y: int, m: datetime.date) -> None:
    """
    Create a dated monthly calendar sheet
    """
    org_x += 2
    x = org_x + 4
    y = org_y + 16
    do_monthly_sheet(x, y)
    month_name = MONTHS[m.month]
    do_month_year_title(org_x, org_y, month_name, str(m.year))
    org_month = m.month
    cur = m + relativedelta(day=1, days=0)
    horizontal_slot = 1
    while cur.month == org_month:
        dow = cur.weekday()  # 0 == Monday

        vertical_slot = 7 - dow
        text_y = (y - PITCH) + (vertical_slot * 18) - 1
        text_x = x + (3 * PITCH * horizontal_slot) - 7
        print(
            """<text style="font-size:4px;font-family:sans-serif;fill:#404040;"""
            """fill-opacity:1;stroke:none"
                """
            f"""x="{text_x:f}"
                y="{text_y:f}"
                transform="rotate(-90 {text_x:f} {text_y:f})"
                >{cur.day}</text>"""
        )

        if dow == 6:  ##sunday
            horizontal_slot += 1
        cur += ONE_DAY


def make_header_sheet(org_x: int, org_y: int, year: int, left: bool = False) -> None:
    """
    Create a header sheet where one side is just a regular lined sheet and the backside
    is a annual calendar thing
    """
    org_x += 2
    x = org_x + 4
    y = org_y + 16
    if not left:
        do_lined_sheet(x, y, dots=True)
    do_year_stamp(org_x, org_y, left, year)
    if left:
        do_frontpage(org_x, org_y, year, left)


def make_weekday_sheet(  # pylint: disable=too-many-positional-arguments,too-many-arguments
    rorg_x: int,
    org_y: int,
    left: bool,
    year: int,
    day: int,
    weekday: str,
    month: str,
    date: datetime.date,
    todos: List[str],
    holidays: List[str],
) -> None:
    """
    Create a dated daily weekday sheet with todos, etc.
    """
    org_x = rorg_x
    org_x += 2
    x = org_x + 4
    y = org_y + 16

    do_lined_sheet(x, y, dots=False)

    do_day_title(org_x, org_y, weekday, month, day)
    do_numbers(org_x, org_y)
    weekday_todo(org_x, org_y, todos, holidays)

    do_year_stamp(org_x, org_y, left, year)
    do_week_stamp(org_x, org_y, date)


def make_weekend_sheet(  # pylint: disable=too-many-positional-arguments,too-many-arguments
    rorg_x: int,
    org_y: int,
    left: bool,
    year: int,
    day: int,
    weekend: str,
    month: str,
    date: datetime.date,
    todos: List[str],
    holidays: List[str],
) -> None:
    """
    Create a dated daily weekend sheet -- no times listed, just a big bunch of todos
    """
    org_x = rorg_x
    org_x += 2
    x = org_x + 4
    y = org_y + 16

    do_lined_sheet(x, y, dots=False)

    do_day_title(org_x, org_y, weekend, month, day)
    weekend_todo(org_x, org_y, todos, holidays)

    do_year_stamp(org_x, org_y, left, year)
    do_week_stamp(org_x, org_y, date, is_weekend=True)


def make_lined_sheet(
    rorg_x: int,
    org_y: int,
    left: bool,
    year: int,
) -> None:
    """
    Create a plain lined sheet
    """
    org_x = rorg_x
    org_x += 2
    x = org_x + 4
    y = org_y + 16

    do_lined_sheet(x, y, dots=True)

    do_year_stamp(org_x, org_y, left, year)


def do_monthly_sheet(x: int, y: int) -> None:
    """
    Draw the grid and days for monthly sheets
    """
    y -= PITCH
    oy = y

    for i in range(8):
        lt = LINE_THICKNESS
        # thicker line between weekdays and weekend
        if i == 2:
            lt *= 3

        print(
            f"""<rect
            """
            f"""style="fill:{COLOR};fill-opacity:1;stroke:{COLOR};stroke-width:0.0688316;"""
            f"""stroke-dasharray:none;stroke-opacity:1"
            width="89.0"
            height="{lt:f}"
            x="{x:f}"
            y="{y:f}" />"""
        )

        if i < 7:
            dow = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][6 - i]
            print(
                """<text style="font-size:6px;font-family:sans-serif;fill:#404040;"""
                f"""fill-opacity:1;stroke:none"
                x="{x+4:f}"
                y="{y+17:f}"
                transform="rotate(-90 {x+4:f} {y+17:f})"
            >{dow}</text>
            """
            )
        y += 18

    for i in range(6):
        print(
            f"""<rect
            style="fill:{COLOR};fill-opacity:1;stroke:{COLOR};stroke-width:0.0688316;"""
            f"""stroke-dasharray:none;stroke-opacity:1"
            width="{LINE_THICKNESS:f}"
            height="{18*7:f}"
            x="{x+4:f}"
            y="{oy:f}" />"""
        )
        x += 3 * PITCH


def do_lined_sheet(x: int, y: int, dots: bool) -> None:
    """
    Create the dotted lines for a lined sheet
    """
    for _ in range(int(126 / PITCH)):
        print(
            f"""<rect
            style="fill:{COLOR};fill-opacity:1;stroke:{COLOR};stroke-width:0.0688316;"""
            f"""stroke-dasharray:none;stroke-opacity:1"
            width="89.0"
            height="{LINE_THICKNESS:f}"
            x="{x:f}"
            y="{y:f}" />"""
        )
        if dots:
            for c in range(int(90 / PITCH)):
                print(
                    f"""<ellipse
                style="fill:{DOT_COLOR};fill-opacity:1;stroke:{DOT_COLOR};stroke-width:0;"""
                    f"""stroke-dasharray:none;stroke-opacity:1"
                cx="{x + (2.5) + c * PITCH + (0.2 * DOT_RADIUS):f}" cy="{y+DOT_Y_OFFSET:f}" """
                    f"""rx="{DOT_RADIUS:f}" ry="{DOT_RADIUS:f}" />"""
                )
        y += PITCH


def frontpage_main_labels(org_x, org_y, year):
    "put the main labels on the whole setup"
    x: float = org_x + 25
    y = org_y + 14
    title = "Yearly Calendars"
    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{title}</text>
                """
    )

    x = org_x + 16
    y = org_y + 14
    title = str(year)
    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y + (5 * PITCH):f}"
                >{title}</text>
                """
    )

    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y + (14 * PITCH):f}"
                >{str(year + 1)}</text>
                """
    )


def frontpage_grid_labels(days, org_x, yoff, org_y):
    "fill in the grid with the proper days of the week"
    # date grid
    for i in range(1, 32):
        col = (i - 1) % 7
        row = int((i - 1) / 7)

        x = col * PITCH + (11 * PITCH) + org_x + 3
        if i >= 10:
            x -= 0.8
        y = row * PITCH + yoff + org_y
        print(
            """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
            f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{str(i)}</text>
                """
        )

    # upper DAY Matrix
    for i in range(7):
        row = i
        for day in range(7):
            daytxt = days[(row + day) % 7]
            col = day
            x = col * PITCH + (11 * PITCH) + org_x + 2
            y = row * PITCH + yoff + (5 * PITCH) + org_y
            print(
                """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
                f"""fill-opacity:1;stroke:none"
                        x="{x:f}"
                        y="{y:f}"
                    >{daytxt}</text>
                    """
            )
    # lower DAY Matrix
    for i in range(7):
        row = i
        for day in range(7):
            daytxt = days[(row + day) % 7]
            col = day
            x = col * PITCH + (11 * PITCH) + org_x + 2
            y = row * PITCH + yoff + (14 * PITCH) + org_y
            print(
                """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
                f"""fill-opacity:1;stroke:none"
                        x="{x:f}"
                        y="{y:f}"
                    >{daytxt}</text>
                    """
            )


def frontpage_month_labels(org_x, org_y, yoff, year):
    "put the months on the appropriate lines"
    ## Put first year months
    mos_first_year: List[List[str]] = [[], [], [], [], [], [], []]
    for i in range(1, 13):
        dt = datetime.date(year, i, 1)
        first_day = (dt.weekday() + 1) % 7
        month_l = mos_first_year[first_day]
        month_l.append(MONTHS[i])

    for index, months in enumerate(mos_first_year):
        ls = ", ".join(months)

        x = org_x + 4
        y = index * PITCH + yoff + (5 * PITCH) + org_y
        print(
            """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
            f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{ls}</text>
                """
        )

    ## Put second year months
    mos_second_year: List[List[str]] = [[], [], [], [], [], [], []]
    for i in range(1, 13):
        dt = datetime.date(year + 1, i, 1)
        first_day = (dt.weekday() + 1) % 7
        month_l = mos_second_year[first_day]
        month_l.append(MONTHS[i])

    for index, months in enumerate(mos_second_year):
        ls = ", ".join(months)

        x = org_x + 4
        y = index * PITCH + yoff + (14 * PITCH) + org_y
        print(
            """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
            f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{ls}</text>
                """
        )


def do_frontpage(org_x: int, org_y: int, year: int, frontpage: bool) -> None:
    """
    Draw the yearly calendars for the front sheet
    """
    color = "#b0b0b0"
    line_thickness = 0.1

    frontpage_main_labels(org_x, org_y, year)

    # upper date to day grid lines
    for cno in range(11, 19):
        print(  # 120 -> 6*12 = 72
            """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="105" """
            f"""width="0.25" x="{org_x + (PITCH * cno) + 1.4:f}" y="{org_y + 16:f}"/>
 """
        )

    days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

    yoff = 20

    frontpage_grid_labels(days, org_x, yoff, org_y)

    frontpage_month_labels(org_x, org_y, yoff, year)

    if not frontpage:
        org_x += 4
        x = org_x + 4
    else:
        x = org_x + 4

    y = org_y + 16

    # draw lines
    for i in range(int(126 / PITCH)):
        if i == 13:
            y += PITCH
            continue
        if i == 22:
            break

        if i <= 4:
            width = 35.0
            xoff = 11 * PITCH - 2.5
        else:
            width = 89 - 1.5
            xoff = 0
        print(
            f"""<rect
        style="fill:{color};fill-opacity:1;stroke:{color};stroke-width:0.0688316;"""
            f"""stroke-dasharray:none;stroke-opacity:1"
        width="{width:f}"
        height="{line_thickness:f}"
        x="{x+xoff:f}"
        y="{y:f}" />"""
        )

        y += PITCH


def do_day_title(
    org_x: int, org_y: int, weekday: str, month: str, day: Optional[int]
) -> None:
    """Draw the day/date title for daily sheets"""
    x = org_x + 9  # + 16
    # x = org_x + 16

    y = org_y + 14
    title = weekday + ", " + month
    if day is not None:
        title += " " + str(day)
    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{title}</text>
                """
    )


def do_month_year_title(org_x: int, org_y: int, month: str, year: str) -> None:
    """Draw the month/year for monthly sheets"""
    x = org_x + 32
    y = org_y + 9
    title = month + " " + year

    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{title}</text>
                """
    )


def do_year_stamp(org_x: int, org_y: int, left: bool, year: int) -> None:
    """
    Draw the year stamp that appears at the bottom of the pages on the inside edge
    """
    if left:
        x = org_x + 86
    else:
        x = org_x + 4
    y = org_y + 140
    print(
        """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >{year}</text>
                """
    )


def do_week_stamp(
    org_x: int, org_y: int, date: datetime.date, is_weekend: bool = False
) -> None:
    """Draw the week/quarter stamp that appears at the bottom of daily sheets"""
    x = org_x + 37
    if is_weekend:
        x += 7
    y = org_y + 140
    week_info = get_week_info(date)
    week_of_year = week_info["week_of_year"]
    quarter = week_info["quarter"]
    week_of_quarter = week_info["week_of_quarter"]

    print(
        """<text style="font-size:3px;font-family:sans-serif;fill:#404040;"""
        f"""fill-opacity:1;stroke:none"
                    x="{x:f}"
                    y="{y:f}"
                >W{week_of_year} Q{quarter}/W{week_of_quarter}</text>
                """
    )


def do_numbers(org_x: int, org_y: int) -> None:
    """Draw the time markers on weekday daily sheets"""
    y = org_y

    # for left
    x = org_x + 3
    for ind, val in enumerate([9, 10, 11, 12, 1, 2, 3, 4]):

        num_lines = 126 / PITCH
        start_line = num_lines - (2 * 8)
        starty = start_line * PITCH + PITCH  # skip the top line

        liney = ind * (PITCH * 2) + (10 + PITCH) + starty + y
        xform = 0.5
        if val > 9:
            xform = 0.25

        fs = (16 * PITCH) / 6

        print(
            f"""<g>
              <text style="font-size:{fs:f}px;font-family:sans-serif;fill:#404040;"""
            f"""fill-opacity:1;stroke:none"
              transform="scale({xform:f},1)"
              x="{x / xform:f}" y="{liney:f}">{val}</text>
              </g>
              """
        )

        half_hours_scale = 0.35
        half_hours_scale = 0.6

        print(
            """<g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;"""
            f"""stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                
                x="{(x + 2) / half_hours_scale + half_hours_scale * PITCH:f}"
                y="{liney - (PITCH + 0.5):f}"
                transform="scale({half_hours_scale:f}, 1)"
              >0</text></g>
              """
        )

        toff = (1.5 * PITCH) / 6

        print(
            """
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;"""
            f"""stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                x="{(x + 2) / half_hours_scale + half_hours_scale * PITCH:f}"
                y="{liney - toff:f}"
                transform="scale({half_hours_scale:f}, 1)"
              >3</text></g>
              """
        )


def weekday_todo(org_x: int, org_y: int, todos: List[str], holidays: List[str]) -> None:
    """
    Draw the todos on the weekday daily sheets
    """
    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" """
        f"""x="{org_x + 42 - 0.12:f}" y="{org_y + 16:f}"/>
 """
    )
    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" """
        f"""x="{org_x + (42 + PITCH) - 0.12:f}" y="{org_y + 16:f}"/>
 """
    )

    for ind, t in enumerate(todos):
        print(
            f"""<g><text xml:space="preserve"
                style="font-size:{PITCH * 0.6}px;font-family:sans-serif;fill:#444444;"""
            f"""fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="{org_x + 42 + (1.25 * PITCH):f}"
                y="{org_y + 15 + ((ind + 1) * PITCH):f}"
              >{t}</text></g>"""
        )

    for ind, t in enumerate(holidays):
        print(
            f"""<g><text xml:space="preserve"
                style="font-size:{PITCH * 0.6}px;font-family:sans-serif;fill:#444444;"""
            f"""fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="{org_x + 6:f}"
                y="{org_y + 15 + ((ind + 1) * PITCH):f}"
              >{t}</text></g>"""
        )


def weekend_todo(org_x: int, org_y: int, todos: List[str], holidays: List[str]) -> None:
    """
    Draw todos on weekend daily sheets
    """
    num_lines = int((126 / PITCH))
    nlm3 = num_lines - 3
    height = nlm3 * PITCH
    org_x -= 2.5
    print(
        f"""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="{height:f}" """
        f"""width="0.25" x="{0.6 + org_x + 6 - 0.12:f}" y="{org_y + 16 + (2 * PITCH):f}"/>
 """
    )
    print(
        f"""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="{height:f}" """
        f"""width="0.25" x="{0.6 + org_x + (6 + PITCH) - 0.12:f}" y="{org_y + 16 + (2 * PITCH):f}"/>
 """
    )

    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" """
        f"""height="{height:f}" """
        f"""width="0.25" x="{0.6 + org_x + 6 + (9 * PITCH) - 0.12:f}" """
        f"""y="{org_y + 16 + (2 * PITCH):f}"/>
 """
    )
    print(
        f"""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" """
        f"""height="{height:f}" """
        f"""width="0.25" x="{0.6 + org_x + (6 + (10 * PITCH)) - 0.12:f}" """
        f"""y="{org_y + 16 + (2 * PITCH):f}"/>
 """
    )

    for ind, t in enumerate(todos):
        print(
            f"""<g><text xml:space="preserve"
                style="font-size:{PITCH * 0.6}px;font-family:sans-serif;fill:#444444;"""
            f"""fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="{org_x + 6 + (1.25 * PITCH):f}"
                y="{org_y + 15 + (2 * PITCH) + ((ind + 1) * PITCH):f}"
              >{t}</text></g>"""
        )

    for ind, t in enumerate(holidays):
        print(
            f"""<g><text xml:space="preserve"
                style="font-size:{PITCH*0.6:f}px;font-family:sans-serif;fill:#444444;"""
            f"""fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="{org_x + 6:f}"
                y="{org_y + 15 + ((ind + 1) * PITCH):f}"
              >{t}</text></g>"""
        )


def a4_page_trailer() -> None:
    """Output the trailer for the full A4 page"""
    print(
        """  </g>
</svg>"""
    )


def a4_page_header() -> None:
    """Output the header for the full A4 page"""
    print(
        """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="296mm"
   viewBox="0 0 210 296"
   version="1.1"
   id="svg1"
   inkscape:version="1.3.2 (091e20e, 2023-11-25)"
   sodipodi:docname="drawing.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
      
 <defs
     id="defs1" />
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
"""
    )


def make_monthly_pages() -> None:
    """Draw a full side of an A4 page of monthly sheets"""
    a4_page_header()
    make_monthly_sheet(0, 0)
    make_monthly_sheet(105, 0)
    make_monthly_sheet(105, 148)
    make_monthly_sheet(0, 148)
    a4_page_trailer()


def make_dated_monthly_pages_p1(year: int) -> None:
    """Draw one full side of an A4 page of dated monthly sheets 1/4"""

    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 1, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 3, 1))
    make_dated_monthly_sheet(105, 148, datetime.date(year, 5, 1))
    make_dated_monthly_sheet(0, 148, datetime.date(year, 7, 1))
    a4_page_trailer()


def make_dated_monthly_pages_p2(year: int) -> None:
    """Draw one full side of an A4 page of dated monthly sheets 2/4"""

    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 4, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 2, 1))
    make_dated_monthly_sheet(105, 148, datetime.date(year, 8, 1))
    make_dated_monthly_sheet(0, 148, datetime.date(year, 6, 1))
    a4_page_trailer()


def make_dated_monthly_pages_p3(year: int) -> None:
    """Draw one full side of an A4 page of dated monthly sheets 3/4"""

    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 9, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 11, 1))

    make_lined_sheet(105, 148, left=False, year=year)
    make_lined_sheet(0, 148, left=False, year=year)
    a4_page_trailer()


def make_dated_monthly_pages_p4(year: int) -> None:
    """Draw one full side of an A4 page of dated monthly sheets 4/4"""
    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 12, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 10, 1))
    make_lined_sheet(105, 148, left=True, year=year)
    make_lined_sheet(0, 148, left=True, year=year)
    a4_page_trailer()


def make_blank_pages(left: bool, year: int) -> None:
    """draw a full side of A4 sheet for lined blank pages"""
    a4_page_header()
    make_lined_sheet(0, 0, left=left, year=year)
    make_lined_sheet(105, 0, left=left, year=year)
    make_lined_sheet(105, 148, left=left, year=year)
    make_lined_sheet(0, 148, left=left, year=year)
    a4_page_trailer()


def make_front_page(year: int, left: bool = False) -> None:
    """Make an A4 sheet of one header page, with the other 3 pages being plain lined pages"""
    a4_page_header()
    x, y = RIGHT_PAGES[0]
    if left:
        x, y = LEFT_PAGES[0]
    make_header_sheet(x, y, left=left, year=year)

    for i in range(1, 4):
        x, y = RIGHT_PAGES[i]
        if left:
            x, y = LEFT_PAGES[i]
        make_lined_sheet(x, y, left=left, year=year)

    a4_page_trailer()


def make_date_page(  # pylint: disable=too-many-locals
    left: bool,
    p: int,
    px: List[Tuple[Tuple[int, int], str, int, str, int, datetime.date]],
    todos: dict,
    holidays: dict,
) -> None:
    """Draw a daily page"""
    side = "right"
    if not left:
        side = "left"
    sys.stdout = create_output_file(f"daily{p}-{side}.svg")
    thisp = px[:4]
    a4_page_header()
    for tp in thisp:
        (x, y), dayofweek, day, month, year, d_obj = tp
        day_todos = get_day_todos(todos, d_obj)
        day_holidays = get_day_todos(holidays, d_obj)
        if dayofweek in ("Saturday", "Sunday"):
            make_weekend_sheet(
                x, y, left, year, day, dayofweek, month, d_obj, day_todos, day_holidays
            )
        else:
            make_weekday_sheet(
                x, y, left, year, day, dayofweek, month, d_obj, day_todos, day_holidays
            )

    np = len(thisp)
    for i in range(np, 4):
        if left:
            x, y = LEFT_PAGES[i]
        else:
            x, y = RIGHT_PAGES[i]
        make_lined_sheet(x, y, left=left, year=year)
    a4_page_trailer()
