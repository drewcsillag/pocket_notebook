import sys
import json

def makea6sheet(rorg_x,org_y, left, year, day = None, weekday=False, weekend=False, monthly=False, pitch=5, todos={}, month=None):
    org_x = rorg_x
    if not left: 
        org_x += 4
        x = org_x + 4
    else:
        org_x += 2
        x = org_x + 4

    y=org_y + 16
    line_thickness = 0.1
    dot_radius = 0.2
    dot_y_offset = 0.05
    color = "#b0b0b0"
    dotcolor = "#909090"

    if monthly:
        y-=pitch
        oy = y

        for i in range(8):
            lt = line_thickness
            if i == 2:
                lt *= 3
            print("""<rect
                style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
                width="89.0"
                height="%f"
                x="%f"
                y="%f" />""" % (color, color, lt, x, y))
            

            if i < 7:
                dow = ['Mon','Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][6-i]
                print("""<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                    transform="rotate(-90 %f %f)"
                >%s</text>
                """ % (x+4,y+17, x+4, y+17, dow))
            y+=18

        for i in range(6):
            print("""<rect
                style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
                width="%f"
                height="%f"
                x="%f"
                y="%f" />""" % (color, color, line_thickness, 18*7, x+4, oy))
            x+= (3*pitch)

    else:
        for i in range(int(126/pitch)):
            print("""<rect
            style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
            width="89.0"
            height="%f"
            x="%f"
            y="%f" />""" % (color, color, line_thickness, x, y))
            if not weekday:
                for c in range(int(90 / pitch)):
                    print("""<ellipse
                style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0;stroke-dasharray:none;stroke-opacity:1"
                cx="%f" cy="%f" rx="%f" ry="%f" />""" % (dotcolor, dotcolor,
                    x + (2.5) + c*pitch + (.2 * dot_radius),
                    y+dot_y_offset,
                    dot_radius, dot_radius ))
            y += pitch
    if weekday:
        do_day_title(org_x, org_y, weekday, left, month, day)
        do_numbers(org_x, org_y, pitch)
        weekday_todo(org_x, org_y, pitch, todos[weekday])
    elif weekend:
        do_day_title(org_x, org_y, weekend, left, month, day)
        weekend_todo(org_x, org_y, pitch, todos[weekend])

    if not monthly:
        do_year_stamp(org_x, org_y, left, year)
        
def do_day_title(org_x, org_y, weekday, left, month, day):
    x = org_x + 16
    y = org_y + 14
    title = weekday + ", " + month
    if day is not None:
        title += " " + str(day)
    print("""<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """ % (x,y, title))

def do_year_stamp(org_x, org_y, left, year):
    if left:
        x = org_x + 86 
    else:
        x = org_x + 4
    y = org_y + 140
    print("""<text style="font-size:3px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """ % (x,y, year))

def do_numbers(org_x, org_y, pitch):
    y = org_y 

    #for left
    x = org_x + 3
    for ind, val in enumerate([9,10,11,12,1,2,3,4]):

        num_lines = (126/pitch)
        start_line = num_lines - (2*8)
        starty = start_line * pitch + pitch # skip the top line


        liney = ind * (pitch*2) + (10 + pitch) + starty + y
        xform = .5
        if val > 9:
            xform = .25

        fs = (16*pitch) / 6

        print("""<g>
              <text style="font-size:%fpx;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
              transform="scale(%f,1)"
              x="%f" y="%f">%i</text>
              </g>
              """ % (fs, xform, x / xform, liney, val))
        
        half_hours_scale = 0.35
        half_hours_scale = 0.6

        print("""<g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                
                x="%f"
                y="%f"
                transform="scale(%f, 1)"
              >0</text></g>
              """ % ((x+2) / half_hours_scale + half_hours_scale * pitch, liney - (pitch + .5), half_hours_scale))
        
        toff = (1.5*pitch) / 6
    
        print("""
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                x="%f"
                y="%f"
                transform="scale(%f, 1)"
              >3</text></g>
              """ % ((x+2) / half_hours_scale + half_hours_scale * pitch, liney- toff, half_hours_scale))
              #""" % ((x+2) / half_hours_scale + half_hours_scale * pitch, liney- toff, half_hours_scale))

def weekday_todo(org_x, org_y, pitch, todos):
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """ % (org_x + 42-.12, org_y + 16))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """ % (org_x + (42+pitch)-.12, org_y + 16))

    for ind, t in enumerate(todos):
        print("""<g><text xml:space="preserve"
                style="font-size:%spx;font-family:sans-serif;fill:#444444;fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="%f"
                y="%f"
              >%s</text></g>""" % (pitch * .6, org_x + 42 + (1.25*pitch), org_y+ 15 + ((ind +1) * pitch), t))

def weekend_todo(org_x, org_y, pitch, todos):
    num_lines = int((126/pitch))
    nlm3 = num_lines-3 
    height=nlm3 * pitch

    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """ % (height, .6 + org_x + 6-.12, org_y + 16 + (2*pitch)))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """ % (height, .6 + org_x + (6+pitch)-.12, org_y + 16 + (2*pitch)))
    
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """ % (height, .6 + org_x + 6+(9*pitch)-.12, org_y + 16 + (2*pitch)))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """ % (height, .6 + org_x + (6+(10*pitch))-.12, org_y + 16 + (2*pitch)))
    
    for ind, t in enumerate(todos):
        print("""<g><text xml:space="preserve"
                style="font-size:%spx;font-family:sans-serif;fill:#444444;fill-opacity:1;stroke-opacity:0;stroke-width:0;stroke-dasharray:none"
                x="%f"
                y="%f"
              >%s</text></g>""" % (pitch * .6, org_x + 6 + (1.25*pitch), org_y+ 15 + (2*pitch) + ((ind +1) * pitch), t))


def a4pagetrailer():
    print("""  </g>
</svg>""")
    
def a4pageheader():
    print("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
""")
    
# def makeweekdayp1and2(left, days, todos, month, year):
#     a4pageheader()
#     makea6sheet(0,0,     left=left, year=year, weekday=days[0], month=month, todos=todos)
#     makea6sheet(105,0,   left=left, year=year, weekday=days[1], month=month, todos=todos)
#     makea6sheet(105,148, left=left, year=year, weekday=days[2], month=month, todos=todos)
#     makea6sheet(0,148,   left=left, year=year, weekday=days[3], month=month, todos=todos)
#     a4pagetrailer()


# def makeMixedSheet(left, todos, month, year):
#     a4pageheader()
#     if not left:
#         makea6sheet(0,0,     month=month, year=year, left=left, weekend='Saturday', todos=todos)
#         makea6sheet(105,0,   month=month, year=year, left=left, weekday='Friday', todos=todos)
#         makea6sheet(105,148, month=month, year=year, left=left, weekend='Sunday', todos=todos)
#         makea6sheet(0,148,   year=year, left=left)
#     else:    
#         makea6sheet(105,0,   month=month, year=year, left=left, weekend='Sunday', todos=todos)
#         makea6sheet(0,0,     month=month, year=year, left=left, weekend='Saturday', todos=todos)
#         makea6sheet(0,148,   month=month, year=year, left=left, weekday='Monday', todos=todos)
#         makea6sheet(105,148, year=year, left=left)
#     a4pagetrailer()

def makeMonthlyPages(left, year):
    a4pageheader()
    makea6sheet(0,0,     left=left, year=year, monthly=True)
    makea6sheet(105,0,   left=left, year=year, monthly=True)
    makea6sheet(105,148, left=left, year=year, monthly=True)
    makea6sheet(0,148,   left=left, year=year, monthly=True)
    a4pagetrailer()

def makeBlankPages(left, year):
    a4pageheader()
    makea6sheet(0,0,     left=left, year=year)
    makea6sheet(105,0,   left=left, year=year)
    makea6sheet(105,148, left=left, year=year)
    makea6sheet(0,148,   left=left, year=year)
    a4pagetrailer()

todos = json.load(open('todos.json'))

import datetime

cur = datetime.date.fromisoformat(sys.argv[1])
numdays = int(sys.argv[2])
numsplits = numdays / 2
if numsplits != int(numsplits):
    print("must specify an even number of days %s %s" % (numsplits, int(numsplits)))
    sys.exit(1)
numsplits = int(numsplits)
DAYS=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS=["X", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ONE_DAY = datetime.timedelta(days=1)
RIGHT_PAGES=[(0,0), (105,0), (0,148), (105,148)]
LEFT_PAGES = [(105,0), (0,0), (105,148), (0, 148)]

minipageno = 0
p1 = []
p2 = []
for i in range(numsplits):
    p1.append((RIGHT_PAGES[minipageno], DAYS[cur.weekday()], cur.day, MONTHS[cur.month], cur.year))
    cur += ONE_DAY 

    p2.append((LEFT_PAGES[minipageno], DAYS[cur.weekday()], cur.day, MONTHS[cur.month], cur.year))
    cur += ONE_DAY 

    minipageno += 1
    if minipageno == 4:
        minipageno = 0

num_sheets = int(len(p1) / 4)
if len(p1) % 4: 
    num_sheets+=1

for p in range(num_sheets):
    sys.stdout = open('daily%d-left.svg' % (p,), 'w')
    thisp = p1[:4]
    a4pageheader()
    for tp in thisp:
        (x, y), dayofweek, day, month, year = tp
        if dayofweek in ('Saturday', 'Sunday'):
            makea6sheet(x,y,left=False, year=year, weekend=dayofweek, month=month, day=day, todos=todos)
        else:
            makea6sheet(x,y,left=False, year=year, weekday=dayofweek, month=month, day=day, todos=todos)

    np = len(thisp)
    for i in range(np, 4):
        x,y = RIGHT_PAGES[i]
        makea6sheet(x,y, left=False, year=year)

    a4pagetrailer()

    sys.stdout = open('daily%d-right.svg' % (p,), 'w')
    thisp = p2[:4]
    a4pageheader()
    for tp in thisp:
        (x, y), dayofweek, day, month, year = tp 
        if dayofweek in ('Saturday', 'Sunday'):
            makea6sheet(x,y,left=True, year=year, weekend=dayofweek, month=month, day=day, todos=todos)
        else:
            makea6sheet(x,y,left=True, year=year, weekday=dayofweek, month=month, day=day, todos=todos)

    np = len(thisp)
    for i in range(np, 4):
        x,y = LEFT_PAGES[i]
        makea6sheet(x,y, left=False, year=year)
    a4pagetrailer()

    p1 = p1[4:]
    p2 = p2[4:]



# month = 'September'
# year=2024

# sys.stdout=open('weekp1.svg','w')
# makeweekdayp1and2(left=0, year=year, days = ['Monday', 'Wednesday', 'Tuesday', 'Thursday'], todos=todos, month=month)
# sys.stdout=open('weekp2.svg', 'w')
# makeweekdayp1and2(left=1, year=year, days=['Thursday', 'Tuesday', 'Friday', 'Wednesday'], todos=todos, month=month)
# sys.stdout=open('weekp3.svg', 'w')
# makeMixedSheet(0, year=year, todos=todos, month=month)
# sys.stdout=open('weekp4.svg', 'w')
# makeMixedSheet(1, year=year, todos=todos, month=month)


# sys.stdout=open('weekp5.svg','w')
# makeweekdayp1and2(left=0, year=year, days = ['Monday', 'Wednesday', 'Tuesday', 'Thursday'], todos=todos, month="")
# sys.stdout=open('weekp6.svg', 'w')
# makeweekdayp1and2(left=1, year=year, days=['Thursday', 'Tuesday', 'Friday', 'Wednesday'], todos=todos, month="")
# sys.stdout=open('weekp7.svg', 'w')
# makeMixedSheet(0, year=year, todos=todos, month="")
# sys.stdout=open('weekp8.svg', 'w')
# makeMixedSheet(1, year=year, todos=todos, month="")


sys.stdout=open('monthly1.svg', 'w')
makeMonthlyPages(0, year=year)
sys.stdout=open('monthly2.svg', 'w')
makeMonthlyPages(1, year=year)

sys.stdout=open('blank1.svg', 'w')
makeBlankPages(0, year=year)
sys.stdout=open('blank2.svg', 'w')
makeBlankPages(1, year=year)
