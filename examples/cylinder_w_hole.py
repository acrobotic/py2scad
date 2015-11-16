"""
Create a Cylinder with a hole cut in it.
"""
from py2scad import *

cyl = Cylinder(h=5,r1=1,r2=1)
hole = Cylinder(h=3,r1=0.2,r2=0.2)
if 1:
    hole = Rotate(hole, v=[1,0,0],a=90) 
else:
    # Show hole making cylinder in tranparent pink
    hole = Rotate(hole, v=[1,0,0],a=90,mod='#') 

cyl_w_hole = Difference([cyl,hole])
prog = SCAD_Prog()
prog.add(cyl_w_hole)
prog.fn=60
prog.write('test.scad')
