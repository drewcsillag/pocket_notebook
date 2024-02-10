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

def makea6sheet(rorg_x,org_y, left, weekday=False, weekend=False, box=False):
    org_x = rorg_x
    if not left: 
        org_x+=10
    x=org_x + 3

    y=org_y + 16
    line_thickness = 0.1
    dot_radius = 0.2
    dot_y_offset = 0.05
    color = "#b0b0b0"
    for i in range(21):
        print("""
        <rect
        style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0.0688316;stroke-dasharray:none;stroke-opacity:1"
        width="89.0"
        height="%f"
        x="%f"
        y="%f" />
    """ % (color, color, line_thickness, x, y))
        for c in range(15):
            print("""
        <ellipse
        style="fill:%s;fill-opacity:1;stroke:%s;stroke-width:0;stroke-dasharray:none;stroke-opacity:1"
        cx="%f"
        cy="%f"
        rx="%f"
        ry="%f" />
                """ % (color, color,
                    org_x + 6 + c*6,
                    y+dot_y_offset,
                    dot_radius, dot_radius ))
        y += 6
    if weekday:
        do_numbers(org_x, org_y)
        weekday_todo(org_x, org_y)
    elif weekend:
        weekend_todo(org_x, org_y)

#     if box:
#         bx = rorg_x
#         # if not left:
#         #     bx += 7
#         print("""
# <rect style="fill:black;fill-opacity:1;stroke:0.1;stroke-width:0.05" height="148" width="0.5" x="%f" y="%f"/>
#  """ % (bx, org_y))
#         print("""
# <rect style="fill:black;fill-opacity:1;stroke:0.1;stroke-width:0.05" height="148" width="0.5" x="%f" y="%f"/>
#  """ % (bx+105, org_y))
        
        
        
def do_numbers(org_x, org_y):
    y = org_y 

    #for left
    x = org_x + 3
    for ind, val in enumerate([9,10,11,12,1,2,3,4]):
        liney = ind * 12 + 16 + 36+ y
        xform = .5
        if val > 9:
            xform = .25
        print("""
        <g>
              <text style="font-size:16px;font-family:sans-serif;fill:#808080;fill-opacity:1;stroke:none"
              transform="scale(%f,1)"
              x="%f" y="%f">%i</text>
              </g>
              """ % (xform, x / xform, liney, val))
        # style="font-size:4px;font-family:sans-serif;fill:#2080ff;fill-opacity:1;stroke:none"
        # style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke-width:.2;stroke:1px #4080ff"
        print("""
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                
                x="%f"
                y="%f"
                transform="scale(.5, 1)"
              >00</text>
              
              </g>
              """ % ((x+2) / .5, liney - 6.5))
        print("""
              <g>
              <text
                xml:space="preserve"
                style="font-size:4px;font-family:sans-serif;fill:#ffffff;fill-opacity:1;stroke:#1242ff;stroke-opacity:1;stroke-width:0.2;stroke-dasharray:none"
                x="%f"
                y="%f"
                transform="scale(.5, 1)"
              >30</text>
              
              </g>
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
 """ % (org_x + 6-.12, org_y + 16 + 12))
    print("""
<rect style="fill:#b0b0b0;fill-opacity:1;stroke-width:0.0688316" height="108" width="0.25" x="%f" y="%f"/>
 """ % (org_x + 12-.12, org_y + 16 + 12))


def makeweekdayp1and2(left):
    makea6sheet(0,0,     left=left, weekday=True, box=False)
    makea6sheet(105,0,   left=left, weekday=True)
    makea6sheet(105,148, left=left, weekday=True)
    makea6sheet(0,148,   left=left, weekday=True)

def makeMixedSheet(left):
    makea6sheet(0,0,     left=left, weekend=True, box=False)
    makea6sheet(105,0,   left=left, weekend=True)
    makea6sheet(105,148, left=left, weekend=True)
    makea6sheet(0,148,   left=left, weekend=True)

makeMixedSheet(1)



print("""  </g>
</svg>""")