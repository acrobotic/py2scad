"""
Creates a tabbed plate
"""
from py2scad import *

INCH2MM = 25.4

inch = INCH2MM
half_inch = 0.5*INCH2MM
quater_inch = 0.25*INCH2MM
eighth_inch = 0.125*INCH2MM

# Plate size
x,y,z = 8*INCH2MM,1*INCH2MM,eighth_inch
size = x,y,z

# Tab list (pos, width, depth, tab_dir)
xz_pos = [
        (0.15, half_inch, eighth_inch, '+'),
        (0.5, half_inch, eighth_inch, '+'),
        (0.85, half_inch, eighth_inch, '+'),
        ]
xz_neg = xz_pos

yz_pos = [
        (0.5, half_inch, eighth_inch,'-'),
        ]

yz_neg = yz_pos

# Collect  tabbed plate parameters
params = { 
        'size' : size, 
        'xz+'  : xz_pos,
        'xz-'  : xz_neg,
        'yz+'  : yz_pos,
        'yz-'  : yz_neg,
        }

plate_maker = Plate_W_Tabs(params)
plate = plate_maker.make()

prog = SCAD_Prog()
prog.fn = 50
prog.add(plate)
prog.write('tabbed_plate.scad')
