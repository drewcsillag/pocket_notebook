import sys

def makea6sheet(rorg_x,org_y, left, weekday=False, weekend=False, monthly=False):
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
        y-=6
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
            x+=18

    else:
        for i in range(21):
            print("""<rect
            style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
            width="89.0"
            height="%f"
            x="%f"
            y="%f" />""" % (color, color, line_thickness, x, y))
            if not weekday:
                for c in range(15):
                    print("""<ellipse
                style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0;stroke-dasharray:none;stroke-opacity:1"
                cx="%f" cy="%f" rx="%f" ry="%f" />""" % (dotcolor, dotcolor,
                    x + (2.5) + c*6 + (.2 * dot_radius),
                    y+dot_y_offset,
                    dot_radius, dot_radius ))
            y += 6
    if weekday:
        do_day_title(org_x, org_y, weekday, left)
        do_numbers(org_x, org_y)
        weekday_todo(org_x, org_y)
    elif weekend:
        do_day_title(org_x, org_y, weekend, left)
        weekend_todo(org_x, org_y)       
        
def do_day_title(org_x, org_y, weekday, left):
    x = org_x + 16
    y = org_y + 14
    year=2024
    print("""<text style="font-size:6px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
                    x="%f"
                    y="%f"
                >%s</text>
                """ % (x,y, weekday))
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

def do_numbers(org_x, org_y):
    y = org_y 

    #for left
    x = org_x + 3
    for ind, val in enumerate([9,10,11,12,1,2,3,4]):
        liney = ind * 12 + 16 + 36+ y
        xform = .5
        if val > 9:
            xform = .25
        print("""<g>
              <text style="font-size:16px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
              transform="scale(%f,1)"
              x="%f" y="%f">%i</text>
              </g>
              """ % (xform, x / xform, liney, val))
        # style="font-size:4px;font-family:sans-serif;fill:#2080ff;fill-opacity:1;stroke:none"
        # style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke-width:.2;stroke:1px #4080ff"
        print("""<g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                
                x="%f"
                y="%f"
                transform="scale(.5, 1)"
              >00</text></g>
              """ % ((x+2) / .5, liney - 6.5))
        print("""
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                x="%f"
                y="%f"
                transform="scale(.5, 1)"
              >30</text></g>
              """ % ((x+2) / .5, liney-1.5))

def weekday_todo(org_x, org_y):
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """ % (org_x + 42-.12, org_y + 16))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="120" width="0.25" x="%f" y="%f"/>
 """ % (org_x + 48-.12, org_y + 16))

def weekend_todo(org_x, org_y):
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="108" width="0.25" x="%f" y="%f"/>
 """ % (.6 + org_x + 6-.12, org_y + 16 + 12))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="108" width="0.25" x="%f" y="%f"/>
 """ % (.6 + org_x + 12-.12, org_y + 16 + 12))


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
