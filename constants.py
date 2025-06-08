"""constants for page generation"""

import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

ONE_DAY = datetime.timedelta(days=1)
RIGHT_PAGES = [(0, 0), (105, 0), (0, 148), (105, 148)]
LEFT_PAGES = [(105, 0), (0, 0), (105, 148), (0, 148)]
PITCH = 5
LINE_THICKNESS = 0.1
COLOR = "#b0b0b0"
DOT_COLOR = "#909090"
DOT_RADIUS = 0.2
DOT_Y_OFFSET = 0.05

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
