"""
Creates an enclosure
"""
from py2scad import *

INCH2MM = 25.4

# Inside dimensions
x,y,z = 8*INCH2MM, 5.15*INCH2MM, 1.5*INCH2MM
hole_list = []

# Create 1/4-20 holes in bottom
for hole_x in (-4.5,4.5):
    for hole_y in (-2,0,2):
        hole = {
                'panel'     : 'bottom',
                'type'      : 'round',
                'location'  : (hole_x*INCH2MM,hole_y*INCH2MM),
                'size'      : 0.257*INCH2MM,
                } 
        hole_list.append(hole)

params = {
        'inner_dimensions'        : (x,y,z), 
        'wall_thickness'          : (1.0/8.0)*INCH2MM, 
        'lid_radius'              : 0.25*INCH2MM,  
        'top_x_overhang'          : 0.2*INCH2MM,
        'top_y_overhang'          : 0.2*INCH2MM,
        'bottom_x_overhang'       : 0.75*INCH2MM,
        'bottom_y_overhang'       : 0.2*INCH2MM, 
        'lid2front_tabs'          : (0.2,0.5,0.8),
        'lid2side_tabs'           : (0.25, 0.75),
        'side2side_tabs'          : (0.5,),
        'lid2front_tab_width'     : 0.75*INCH2MM,
        'lid2side_tab_width'      : 0.75*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.05*INCH2MM,
        'standoff_hole_diameter'  : 0.116*INCH2MM, 
        'hole_list'               : hole_list,
        }

enclosure = Basic_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(explode=(5,5,5))
part_projection = enclosure.get_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
prog_projection.write('enclosure_projection.scad')
