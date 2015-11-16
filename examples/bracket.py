"""
Creates a right angle bracket w/ tabs for laser cutting. 
"""
from  py2scad import *

# Define base-to-face tabs (pos, width, depth, tab_dir)
base2face_tabs = [
        (0.2, 0.5*INCH2MM, 0.25*INCH2MM),
        (0.50, 0.5*INCH2MM, 0.25*INCH2MM),
        (0.8, 0.5*INCH2MM, 0.25*INCH2MM),
        ]

# Define right angle supports
face_tabs = [ 
        (0.2, 0.5*INCH2MM, 0.25*INCH2MM),
        (0.5, 0.5*INCH2MM, 0.25*INCH2MM),
        (0.8, 0.5*INCH2MM, 0.25*INCH2MM),
        ]

base_tabs =  [
        (0.2, 0.5*INCH2MM, 0.25*INCH2MM),
        (0.5, 0.5*INCH2MM, 0.25*INCH2MM),
        (0.8, 0.5*INCH2MM, 0.25*INCH2MM),
        ]

support_params = {
        'depth'     :  4.0*INCH2MM, 
        'height'    :  5.0*INCH2MM - 0.25*INCH2MM, 
        'thickness' : 0.25*INCH2MM, 
        'face_tabs' : face_tabs, 
        'base_tabs' : base_tabs, 
        }

support_list = [ 
        { 'pos':  1.5*INCH2MM, 'params': support_params},
        { 'pos': -1.5*INCH2MM, 'params': support_params}, 
        ]

# Create list of holes
hole_list = []
for x in range(-2,3):
    for y in range(-2,3):
        hole = {
                'plate'    : 'base', 
                'type'     : 'round',
                'size'     :  0.25*INCH2MM, 
                'location' :  (x*INCH2MM,y*INCH2MM),
                }
        hole_list.append(hole)
        hole = {
                'plate'    : 'face', 
                'type'     : 'round',
                'size'     :  0.21*INCH2MM, 
                'location' :  (x*INCH2MM,y*INCH2MM),
                }
        hole_list.append(hole)

        

# Parameters for right angle bracket
params = {
        'base_width'         : 5.0*INCH2MM,
        'base_depth'         : 5.0*INCH2MM,
        'base_thickness'     : 0.25*INCH2MM,
        'face_width'         : 5.0*INCH2MM,
        'face_height'        : 6.0*INCH2MM,
        'face_thickness'     : 0.25*INCH2MM,
        'base2face_tabs'     : base2face_tabs, 
        'base_tab_dir'       : '+',
        'supports'           : support_list,
        'hole_list'          : hole_list,
        }

rt_bracket = Right_Angle_Bracket(params)
rt_bracket.make()
assembly = rt_bracket.get_assembly(explode=(0,10,10))
prog = SCAD_Prog()
prog.add(assembly)
prog.write('bracket_assembly.scad')

projection = rt_bracket.get_projection()
prog = SCAD_Prog()
prog.add(projection)
prog.write('bracket_projection.scad')
