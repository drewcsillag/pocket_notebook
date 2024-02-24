import sys

def makea6sheet(rorg_x,org_y, left, weekday=False, weekend=False, monthly=False, pitch=5):
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
            print("""<rect
                style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
                width="89.0"
                height="%f"
                x="%f"
                y="%f" />""" % (color, color, line_thickness, x, y))
            

            if i < 7:
                dow = ['Mon','Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][6-i]
                print("""<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                    transform="rotate(-90 %f %f)"
                >%s</text>
                """ % (x+4,y+17, x+4, y+17, dow))
            y+=18

        for i in range(5):
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
        do_day_title(org_x, org_y, weekday, left)
        do_numbers(org_x, org_y, pitch)
        weekday_todo(org_x, org_y, pitch)
    elif weekend:
        do_day_title(org_x, org_y, weekend, left)
        weekend_todo(org_x, org_y, pitch)

    do_year_stamp(org_x, org_y, left)
        
def do_day_title(org_x, org_y, weekday, left):
    x = org_x + 16
    y = org_y + 14
    print("""<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """ % (x,y, weekday))
    # do_year_stamp(org_x, org_y, left)

def do_year_stamp(org_x, org_y, left):
    year=2024
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
        print("""<g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                
                x="%f"
                y="%f"
                transform="scale(.5, 1)"
              >00</text></g>
              """ % ((x+2) / .5, liney - (pitch + .5)))
        
        toff = (1.5*pitch) / 6
        print("""
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                x="%f"
                y="%f"
                transform="scale(.5, 1)"
              >30</text></g>
              """ % ((x+2) / .5, liney- toff))

def weekday_todo(org_x, org_y, pitch):
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """ % (org_x + 42-.12, org_y + 16))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """ % (org_x + (42+pitch)-.12, org_y + 16))

def weekend_todo(org_x, org_y, pitch):
    num_lines = int((126/pitch))
    nlm3 = num_lines-3 
    height=nlm3 * pitch

    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """ % (height, .6 + org_x + 6-.12, org_y + 16 + (2*pitch))) #12))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="%f" width="0.25" x="%f" y="%f"/>
 """ % (height, .6 + org_x + (6+pitch)-.12, org_y + 16 + (2*pitch)))#12))


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
    
def makeweekdayp1and2(left, days):
    a4pageheader()
    makea6sheet(0,0,     left=left, weekday=days[0])
    makea6sheet(105,0,   left=left, weekday=days[1])
    makea6sheet(105,148, left=left, weekday=days[2])
    makea6sheet(0,148,   left=left, weekday=days[3])
    a4pagetrailer()


def makeMixedSheet(left):
    a4pageheader()
    if not left:
        makea6sheet(0,0,     left=left, weekend='Saturday')
        makea6sheet(105,0,   left=left, weekday='Friday')
        makea6sheet(105,148, left=left, weekend='Sunday')
        makea6sheet(0,148,   left=left)
    else:    
        makea6sheet(105,0,   left=left, weekend='Sunday')
        makea6sheet(0,0,     left=left, weekend='Saturday')
        makea6sheet(0,148,   left=left, weekday='Monday')
        makea6sheet(105,148, left=left)
    a4pagetrailer()

def makeMonthlyPages(left):
    a4pageheader()
    makea6sheet(0,0,     left=left, monthly=True)
    makea6sheet(105,0,   left=left, monthly=True)
    makea6sheet(105,148, left=left, monthly=True)
    makea6sheet(0,148,   left=left, monthly=True)
    a4pagetrailer()

sys.stdout=open('weekp1.svg','w')
makeweekdayp1and2(left=0, days = ['Monday', 'Wednesday', 'Tuesday', 'Thursday'])
sys.stdout=open('weekp2.svg', 'w')
makeweekdayp1and2(left=1, days=['Thursday', 'Tuesday', 'Friday', 'Wednesday'])
sys.stdout=open('weekp3.svg', 'w')
makeMixedSheet(0)
sys.stdout=open('weekp4.svg', 'w')
makeMixedSheet(1)


sys.stdout=open('monthly1.svg', 'w')
makeMonthlyPages(0)
sys.stdout=open('monthly2.svg', 'w')
makeMonthlyPages(1)
