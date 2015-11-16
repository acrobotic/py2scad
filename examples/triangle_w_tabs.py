"""
Creates a right triangle with tabs.
"""
from  py2scad import *

x,y,z = 5*INCH2MM, 6*INCH2MM, 0.125*INCH2MM

#(pos_0, width_0, depth_0, dir_0)
xz_tabs = [ 
        (0.2, 0.5*INCH2MM, 0.125*INCH2MM, '+'),
        (0.5, 0.5*INCH2MM, 0.125*INCH2MM, '+'),
        (0.8, 0.5*INCH2MM, 0.125*INCH2MM, '+'),
        ]

yz_tabs =  [
        (0.25, 1.0*INCH2MM, 0.125*INCH2MM, '+'),
        (0.75, 1.0*INCH2MM, 0.125*INCH2MM, '+'),
        ]
hz_tabs = [
        (0.25, 1.0*INCH2MM, 0.125*INCH2MM, '-'),
        (0.5, 1.0*INCH2MM, 0.125*INCH2MM, '-'),
        (0.75, 1.0*INCH2MM, 0.125*INCH2MM, '-'),
        ]

params = {
        'size' : (x,y,z),
        'xz'    : xz_tabs,
        'yz'    : yz_tabs, 
        'hz'    : hz_tabs,
        }

rt = RT_Triangle_W_Tabs(params)
part = rt.make() 

prog = SCAD_Prog()
prog.add(part)
prog.write('rt_triangle.scad')
