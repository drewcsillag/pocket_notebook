import io
import sys
import yaml
from typing import Any, Dict, List, TextIO, Tuple, Optional
from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = [
    "X",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

DAY_TO_NUM = {
    "Monday": MO,
    "Tuesday": TU,
    "Wednesday": WE,
    "Thursday": TH,
    "Friday": FR,
    "Saturday": SA,
    "Sunday": SU,
}

ONE_DAY = datetime.timedelta(days=1)
RIGHT_PAGES = [(0, 0), (105, 0), (0, 148), (105, 148)]
LEFT_PAGES = [(105, 0), (0, 0), (105, 148), (0, 148)]
PITCH = 5
LINE_THICKNESS = 0.1
COLOR = "#b0b0b0"
DOT_COLOR = "#909090"
DOT_RADIUS = 0.2
DOT_Y_OFFSET = 0.05


def make_monthly_sheet(org_x: int, org_y: int) -> None:
    org_x += 2
    x = org_x + 4
    y = org_y + 16
    do_monthly_sheet(x, y)


def make_dated_monthly_sheet(org_x: int, org_y: int, m: datetime.date) -> None:
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
            """<text style="font-size:4px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                x="%f"
                y="%f"
                transform="rotate(-90 %f %f)"
                >%d</text>"""
            % (text_x, text_y, text_x, text_y, cur.day)
        )

        if dow == 6:  ##sunday
            horizontal_slot += 1
        cur += ONE_DAY


def make_header_sheet(org_x: int, org_y: int, year: int, left: bool = False) -> None:
    org_x += 2
    x = org_x + 4
    y = org_y + 16
    if not left:
        do_lined_sheet(x, y, dots=True)
    do_year_stamp(org_x, org_y, left, year)
    if left:
        do_frontpage(org_x, org_y, year, left)


def make_weekday_sheet(
    rorg_x: int,
    org_y: int,
    left: bool,
    year: int,
    day: int,
    weekday: str,
    month: str,
    todos: List[str] = [],
    holidays: List[str] = [],
) -> None:
    org_x = rorg_x
    org_x += 2
    x = org_x + 4
    y = org_y + 16

    do_lined_sheet(x, y, dots=False)

    do_day_title(org_x, org_y, weekday, month, day)
    do_numbers(org_x, org_y)
    weekday_todo(org_x, org_y, todos, holidays)

    do_year_stamp(org_x, org_y, left, year)


def make_weekend_sheet(
    rorg_x: int,
    org_y: int,
    left: bool,
    year: int,
    day: int,
    weekend: str,
    month: str,
    todos: List[str] = [],
    holidays: List[str] = [],
) -> None:
    org_x = rorg_x
    org_x += 2
    x = org_x + 4
    y = org_y + 16

    do_lined_sheet(x, y, dots=True)

    do_day_title(org_x, org_y, weekend, month, day)
    weekend_todo(org_x, org_y, todos, holidays)

    do_year_stamp(org_x, org_y, left, year)


def make_lined_sheet(
    rorg_x: int,
    org_y: int,
    left: bool,
    year: int,
) -> None:
    org_x = rorg_x
    org_x += 2
    x = org_x + 4
    y = org_y + 16

    do_lined_sheet(x, y, dots=True)

    do_year_stamp(org_x, org_y, left, year)


def do_monthly_sheet(x: int, y: int) -> None:
    y -= PITCH
    oy = y

    for i in range(8):
        lt = LINE_THICKNESS
        # thicker line between weekdays and weekend
        if i == 2:
            lt *= 3

        print(
            """<rect
            style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
            width="89.0"
            height="%f"
            x="%f"
            y="%f" />"""
            % (COLOR, COLOR, lt, x, y)
        )

        if i < 7:
            dow = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][6 - i]
            print(
                """<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                x="%f"
                y="%f"
                transform="rotate(-90 %f %f)"
            >%s</text>
            """
                % (x + 4, y + 17, x + 4, y + 17, dow)
            )
        y += 18

    for i in range(6):
        print(
            """<rect
            style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
            width="%f"
            height="%f"
            x="%f"
            y="%f" />"""
            % (COLOR, COLOR, LINE_THICKNESS, 18 * 7, x + 4, oy)
        )
        x += 3 * PITCH


def do_lined_sheet(x: int, y: int, dots: bool) -> None:
    for i in range(int(126 / PITCH)):
        print(
            """<rect
            style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
            width="89.0"
            height="%f"
            x="%f"
            y="%f" />"""
            % (COLOR, COLOR, LINE_THICKNESS, x, y)
        )
        if dots:
            for c in range(int(90 / PITCH)):
                print(
                    """<ellipse
                style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0;stroke-dasharray:none;stroke-opacity:1"
                cx="%f" cy="%f" rx="%f" ry="%f" />"""
                    % (
                        DOT_COLOR,
                        DOT_COLOR,
                        x + (2.5) + c * PITCH + (0.2 * DOT_RADIUS),
                        y + DOT_Y_OFFSET,
                        DOT_RADIUS,
                        DOT_RADIUS,
                    )
                )
        y += PITCH


def do_frontpage(org_x: int, org_y: int, year: int, frontpage: bool) -> None:
    color = "#b0b0b0"
    line_thickness = 0.1

    x: float = org_x + 25
    y = org_y + 14
    title = "Yearly Calendars"
    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
        % (x, y, title)
    )

    x = org_x + 16
    y = org_y + 14
    title = str(year)
    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
        % (x, y + (5 * PITCH), title)
    )

    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
        % (x, y + (14 * PITCH), str(year + 1))
    )

    # upper date to day grid lines
    for cno in range(11, 19):
        print(  # 120 -> 6*12 = 72
            """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="105" width="0.25" x="%f" y="%f"/>
 """
            % (org_x + (PITCH * cno) + 1.4, org_y + 16)
        )

    days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

    YOFF = 20

    # date grid
    for i in range(1, 32):
        col = (i - 1) % 7
        row = int((i - 1) / 7)

        x = col * PITCH + (11 * PITCH) + org_x + 3
        if i >= 10:
            x -= 0.8
        y = row * PITCH + YOFF + org_y
        print(
            """<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
            % (x, y, str(i))
        )

    # upper DAY Matrix
    for i in range(7):
        row = i
        for day in range(7):
            daytxt = days[(row + day) % 7]
            col = day
            x = col * PITCH + (11 * PITCH) + org_x + 2
            y = row * PITCH + YOFF + (5 * PITCH) + org_y
            print(
                """<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                        x="%f"
                        y="%f"
                    >%s</text>
                    """
                % (x, y, daytxt)
            )
    # lower DAY Matrix
    for i in range(7):
        row = i
        for day in range(7):
            daytxt = days[(row + day) % 7]
            col = day
            x = col * PITCH + (11 * PITCH) + org_x + 2
            y = row * PITCH + YOFF + (14 * PITCH) + org_y
            print(
                """<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                        x="%f"
                        y="%f"
                    >%s</text>
                    """
                % (x, y, daytxt)
            )

    ## Put first year months
    mos_first_year: List[List[str]] = [[], [], [], [], [], [], []]
    for i in range(1, 13):
        dt = datetime.date(year, i, 1)
        first_day = (dt.weekday() + 1) % 7
        l = mos_first_year[first_day]
        l.append(MONTHS[i])

    for index, months in enumerate(mos_first_year):
        ls = ", ".join(months)

        x = org_x + 4
        y = index * PITCH + YOFF + (5 * PITCH) + org_y
        print(
            """<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
            % (x, y, ls)
        )

    ## Put second year months
    mos_second_year: List[List[str]] = [[], [], [], [], [], [], []]
    for i in range(1, 13):
        dt = datetime.date(year + 1, i, 1)
        first_day = (dt.weekday() + 1) % 7
        l = mos_second_year[first_day]
        l.append(MONTHS[i])

    for index, months in enumerate(mos_second_year):
        ls = ", ".join(months)

        x = org_x + 4
        y = index * PITCH + YOFF + (14 * PITCH) + org_y
        print(
            """<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
            % (x, y, ls)
        )

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
            """<rect
        style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
        width="%f"
        height="%f"
        x="%f"
        y="%f" />"""
            % (color, color, width, line_thickness, x + xoff, y)
        )

        y += PITCH


def do_day_title(
    org_x: int, org_y: int, weekday: str, month: str, day: Optional[int]
) -> None:
    x = org_x + 16
    y = org_y + 14
    title = weekday + ", " + month
    if day is not None:
        title += " " + str(day)
    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
        % (x, y, title)
    )


def do_month_year_title(org_x: int, org_y: int, month: str, year: str) -> None:
    x = org_x + 32
    y = org_y + 8
    title = month + " " + year

    print(
        """<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
        % (x, y, title)
    )


def do_year_stamp(org_x: int, org_y: int, left: bool, year: int) -> None:
    if left:
        x = org_x + 86
    else:
        x = org_x + 4
    y = org_y + 140
    print(
        """<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """
        % (x, y, year)
    )


def do_numbers(org_x: int, org_y: int) -> None:
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
            """<g>
              <text style="font-size:%fpx;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
              transform="scale(%f,1)"
              x="%f" y="%f">%i</text>
              </g>
              """
            % (fs, xform, x / xform, liney, val)
        )

        half_hours_scale = 0.35
        half_hours_scale = 0.6

        print(
            """<g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                
                x="%f"
                y="%f"
                transform="scale(%f, 1)"
              >0</text></g>
              """
            % (
                (x + 2) / half_hours_scale + half_hours_scale * PITCH,
                liney - (PITCH + 0.5),
                half_hours_scale,
            )
        )

        toff = (1.5 * PITCH) / 6

        print(
            """
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                x="%f"
                y="%f"
                transform="scale(%f, 1)"
              >3</text></g>
              """
            % (
                (x + 2) / half_hours_scale + half_hours_scale * PITCH,
                liney - toff,
                half_hours_scale,
            )
        )
        # """ % ((x+2) / half_hours_scale + half_hours_scale * pitch, liney- toff, half_hours_scale))


def weekday_todo(org_x: int, org_y: int, todos: List[str], holidays: List[str]) -> None:
    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """
        % (org_x + 42 - 0.12, org_y + 16)
    )
    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """
        % (org_x + (42 + PITCH) - 0.12, org_y + 16)
    )

    for ind, t in enumerate(todos):
        print(
            """<g><text xml:space="preserve"
                style="font-size:%spx;font-family:sans-serif;fill:#444444;fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="%f"
                y="%f"
              >%s</text></g>"""
            % (
                PITCH * 0.6,
                org_x + 42 + (1.25 * PITCH),
                org_y + 15 + ((ind + 1) * PITCH),
                t,
            )
        )

    for ind, t in enumerate(holidays):
        print(
            """<g><text xml:space="preserve"
                style="font-size:%spx;font-family:sans-serif;fill:#444444;fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="%f"
                y="%f"
              >%s</text></g>"""
            % (
                PITCH * 0.6,
                org_x + 6,
                org_y + 15 + ((ind + 1) * PITCH),
                t,
            )
        )


def weekend_todo(org_x: int, org_y: int, todos: List[str], holidays: List[str]) -> None:
    num_lines = int((126 / PITCH))
    nlm3 = num_lines - 3
    height = nlm3 * PITCH

    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """
        % (height, 0.6 + org_x + 6 - 0.12, org_y + 16 + (2 * PITCH))
    )
    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """
        % (height, 0.6 + org_x + (6 + PITCH) - 0.12, org_y + 16 + (2 * PITCH))
    )

    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """
        % (height, 0.6 + org_x + 6 + (9 * PITCH) - 0.12, org_y + 16 + (2 * PITCH))
    )
    print(
        """
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """
        % (height, 0.6 + org_x + (6 + (10 * PITCH)) - 0.12, org_y + 16 + (2 * PITCH))
    )

    for ind, t in enumerate(todos):
        print(
            """<g><text xml:space="preserve"
                style="font-size:%spx;font-family:sans-serif;fill:#444444;fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="%f"
                y="%f"
              >%s</text></g>"""
            % (
                PITCH * 0.6,
                org_x + 6 + (1.25 * PITCH),
                org_y + 15 + (2 * PITCH) + ((ind + 1) * PITCH),
                t,
            )
        )

    for ind, t in enumerate(holidays):
        print(
            """<g><text xml:space="preserve"
                style="font-size:%spx;font-family:sans-serif;fill:#444444;fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="%f"
                y="%f"
              >%s</text></g>"""
            % (
                PITCH * 0.6,
                org_x + 6,
                org_y + 15 + ((ind + 1) * PITCH),
                t,
            )
        )


def a4_page_trailer() -> None:
    print(
        """  </g>
</svg>"""
    )


def a4_page_header() -> None:
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

    ### DEBUG LINES FOLLOW
    # print(
    #     """<rect
    #     style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
    #     width="0.2"
    #     height="%f"
    #     x="%f"
    #     y="%f" />"""
    #     % ("#000000", "#000000", 297, 105, 0)
    # )

    # print(
    #     """<rect
    #     style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
    #     width="0.1"
    #     height="%f"
    #     x="%f"
    #     y="%f" />"""
    #     % ("#000000", "#000000", 297, 95, 0)
    # )

    # print(
    #     """<rect
    #     style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
    #     width="0.1"
    #     height="%f"
    #     x="%f"
    #     y="%f" />"""
    #     % ("#000000", "#000000", 297, 10, 0)
    # )

    # print(
    #     """<rect
    #     style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
    #     width="0.1"
    #     height="%f"
    #     x="%f"
    #     y="%f" />"""
    #     % ("#000000", "#000000", 297, 200, 0)
    # )

    # print(
    #     """<rect
    #     style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
    #     width="0.1"
    #     height="%f"
    #     x="%f"
    #     y="%f" />"""
    #     % ("#000000", "#000000", 297, 115, 0)
    # )
    # print(
    #     """<rect
    #     style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
    #     width="0.2"
    #     height="%f"
    #     x="%f"
    #     y="%f" />"""
    #     % ("#000000", "#000000", 297, 209, 0)
    # )


def make_monthly_pages() -> None:
    a4_page_header()
    make_monthly_sheet(0, 0)
    make_monthly_sheet(105, 0)
    make_monthly_sheet(105, 148)
    make_monthly_sheet(0, 148)
    a4_page_trailer()


def make_dated_monthly_pages_p1(year: int) -> None:
    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 1, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 3, 1))
    make_dated_monthly_sheet(105, 148, datetime.date(year, 5, 1))
    make_dated_monthly_sheet(0, 148, datetime.date(year, 7, 1))
    a4_page_trailer()


def make_dated_monthly_pages_p2(year: int) -> None:
    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 4, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 2, 1))
    make_dated_monthly_sheet(105, 148, datetime.date(year, 8, 1))
    make_dated_monthly_sheet(0, 148, datetime.date(year, 6, 1))
    a4_page_trailer()


def make_dated_monthly_pages_p3(year: int) -> None:
    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 9, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 11, 1))

    make_lined_sheet(105, 148, left=False, year=year)
    make_lined_sheet(0, 148, left=False, year=year)
    a4_page_trailer()


def make_dated_monthly_pages_p4(year: int) -> None:
    a4_page_header()
    make_dated_monthly_sheet(0, 0, datetime.date(year, 12, 1))
    make_dated_monthly_sheet(105, 0, datetime.date(year, 10, 1))
    make_lined_sheet(105, 148, left=True, year=year)
    make_lined_sheet(0, 148, left=True, year=year)
    a4_page_trailer()


def make_blank_pages(left: bool, year: int) -> None:
    a4_page_header()
    make_lined_sheet(0, 0, left=left, year=year)
    make_lined_sheet(105, 0, left=left, year=year)
    make_lined_sheet(105, 148, left=left, year=year)
    make_lined_sheet(0, 148, left=left, year=year)
    a4_page_trailer()


def add_todos(t: List[str], v: List[str]) -> List[str]:
    t = t[:]
    for i in v:
        if "" in t:
            ind = t.index("")
            t[ind] = i
        else:
            t.append(i)
    return t


def get_day_todos(todos: Dict[str, List[Dict]], d_obj: datetime.date) -> List[str]:
    y = todos["yearly"][0]

    all_todos: List[str] = []

    m_y: Dict[str, List[str]] = {}
    for k, v in y.items():
        bits = k.split(",")
        if len(bits) == 3:
            month, dow, which = bits
        elif len(bits) == 2:
            month = "*"
            dow, which = bits
        if month != "*" and MONTHS.index(month) != d_obj.month:
            continue
        k = "%s,%s" % (dow, which)
        if k in m_y:
            l = m_y[k][:]
            l.extend(v)
            m_y[k] = l
        else:
            m_y["%s,%s" % (dow, which)] = v
    all_todos = add_monthly_todos(d_obj, m_y, all_todos)

    return all_todos


def add_monthly_todos(
    d_obj: datetime.date, m: Dict[str, List[str]], all_todos: List[str]
) -> List[str]:
    for k, v in m.items():
        dow, which_str = k.split(",")
        if which_str == "*":
            which_str = "0"
        which = int(which_str)

        if dow == "Day":
            # days from end of month
            if which < 0:
                rd = d_obj + relativedelta(day=33, days=which + 1)
                if rd == d_obj:
                    all_todos = add_todos(all_todos, v)
            else:  ## days from start
                rd = d_obj + relativedelta(day=1, days=which - 1)
                if rd == d_obj:
                    all_todos = add_todos(all_todos, v)

        else:
            dow_n = DAY_TO_NUM[dow]
            if which == 0:
                if d_obj.weekday() == dow_n.weekday:
                    all_todos = add_todos(all_todos, v)
            else:
                if which < 0:
                    rd = d_obj + relativedelta(day=31, weekday=dow_n(which))
                else:
                    rd = d_obj + relativedelta(day=1, weekday=dow_n(which))
                if rd == d_obj:
                    all_todos = add_todos(all_todos, v)
    return all_todos


def make_front_page(year: int, left: bool = False) -> None:
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


def make_date_page(
    left: bool,
    p: int,
    px: List[Tuple[Tuple[int, int], str, int, str, int, datetime.date]],
) -> None:
    side = "right"
    if not left:
        side = "left"
    sys.stdout = open("daily%d-%s.svg" % (p, side), "w")
    thisp = px[:4]
    a4_page_header()
    for tp in thisp:
        (x, y), dayofweek, day, month, year, d_obj = tp
        day_todos = get_day_todos(todos, d_obj)
        day_holidays = get_day_todos(holidays, d_obj)
        if dayofweek in ("Saturday", "Sunday"):
            make_weekend_sheet(
                x, y, left, year, day, dayofweek, month, day_todos, day_holidays
            )
        else:
            make_weekday_sheet(
                x, y, left, year, day, dayofweek, month, day_todos, day_holidays
            )

    np = len(thisp)
    for i in range(np, 4):
        if left:
            x, y = LEFT_PAGES[i]
        else:
            x, y = RIGHT_PAGES[i]
        make_lined_sheet(x, y, left=left, year=year)
    a4_page_trailer()


def parse_preserving_duplicates(src: TextIO) -> Dict:
    # We deliberately define a fresh class inside the function,
    # because add_constructor is a class method and we don't want to
    # mutate pyyaml classes.
    class PreserveDuplicatesLoader(yaml.loader.Loader):
        pass

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


if __name__ == "__main__":
    todos = parse_preserving_duplicates(open("todo_holidays/todos.yaml"))
    holidays = parse_preserving_duplicates(open("todo_holidays/holidays.yaml"))
    cur = datetime.date.fromisoformat(sys.argv[1])
    orig_year = cur.year
    numdays = int(sys.argv[2])
    numsplits = numdays / 2
    if numsplits != int(numsplits):
        print("must specify an even number of days %s %s" % (numsplits, int(numsplits)))
        sys.exit(1)
    numsplits = int(numsplits)

    minipageno = 0
    p1 = []
    p2 = []
    for i in range(numsplits):
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
        make_date_page(left=False, p=p, px=p1[:4])
        make_date_page(left=True, p=p, px=p2[:4])

        p1 = p1[4:]
        p2 = p2[4:]

    sys.stdout = open("monthly1.svg", "w")
    make_monthly_pages()
    sys.stdout = open("monthly2.svg", "w")
    make_monthly_pages()

    sys.stdout = open("monthly_dated1.svg", "w")
    make_dated_monthly_pages_p1(orig_year)
    sys.stdout = open("monthly_dated2.svg", "w")
    make_dated_monthly_pages_p2(orig_year)
    sys.stdout = open("monthly_dated3.svg", "w")
    make_dated_monthly_pages_p3(orig_year)
    sys.stdout = open("monthly_dated4.svg", "w")
    make_dated_monthly_pages_p4(orig_year)

    sys.stdout = open("blank1.svg", "w")
    make_blank_pages(False, year=year)
    sys.stdout = open("blank2.svg", "w")
    make_blank_pages(True, year=year)

    sys.stdout = open("header_r.svg", "w")
    make_front_page(year=year, left=True)
    sys.stdout = open("header_l.svg", "w")

    make_front_page(year=year, left=False)
