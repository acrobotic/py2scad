"""
Creates a sloted plate - i.e., a plate with rectangular holes 
"""
from py2scad import *

INCH2MM = 25.4

inch = INCH2MM
eighth_inch = 0.125*INCH2MM

# Plate size
x,y,z = 6*INCH2MM, 5*INCH2MM, eighth_inch
size = x,y,z
        
# Hole list (pos, size)
slots = [
        ((0.0, 0.0), (inch, 2*inch)), 
        ((2*inch, 0.0), (inch, inch)),
]

params = {'size' : size, 'slots' : slots}

plate_maker = Plate_W_Slots(params)
plate = plate_maker.make()

prog = SCAD_Prog()
prog.fn = 50
prog.add(plate)
prog.write('slotted_plate.scad')
