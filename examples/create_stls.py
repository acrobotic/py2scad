"""
Create parts, save scad files and then use openscad form the command
line to convert the scad files to stl files. 
"""
import os
from py2scad import *

c0 = Cylinder(h=1,r1=1,r2=1)
c0 = Translate(c0,v=[5,0,0])

c1 = Cube(size=[3,3,1])
c1 = Translate(c1,v=[-5,0,0])

print 'writng scad files'

prog0 = SCAD_Prog()
prog0.fn = 10
prog0.add(c0)
prog0.write('test0.scad')

prog1 = SCAD_Prog()
prog1.fn = 40
prog1.add(c1)
prog1.write('test1.scad')


print 'writing stl files'

os.system('openscad -s test0.stl test0.scad')
os.system('openscad -s test1.stl test1.scad')

