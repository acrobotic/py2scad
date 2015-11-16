"""
Create parts, save scad files and then use openscad form the command
line to convert the scad files to stl files. 
"""
import os
import pickle
from py2scad import *

c0 = Cylinder(h=1,r1=1,r2=1)
c0 = Translate(c0,v=[5,0,0])

c1 = Cube(size=[3,3,0.3])
c1 = Translate(c1,v=[-5,0,0])

c2 = Sphere(r=2)
c2 = Translate(c2,v=[5,5,0])

print 'writng scad files'

prog0 = SCAD_Prog()
prog0.fn = 40
prog0.add(c0)
prog0.write('test0.scad')

prog1 = SCAD_Prog()
prog1.fn = 40
prog1.add(c1)
prog1.write('test1.scad')

prog2 = SCAD_Prog()
prog2.fn = 40
prog2.add(c2)
prog2.write('test2.scad')

print 'writing stl files'

os.system('openscad -s test0.stl test0.scad')
os.system('openscad -s test1.stl test1.scad')
os.system('openscad -s test2.stl test2.scad')

obj_list = [ 
        {
            'filename'   : 'test0.stl',
            'parameters' : { 
                'color'          : (0.5,0.5,0.5), 
                'opacity'        : 1.0, 
                'specular'       : 1.0, 
                'diffuse'        : 0.8, 
                'specular_power' : 1.0,
                },
            },
        { 
            'filename'   : 'test1.stl',
            'parameters' : {
                'color'          : (0.4, 0.4, 0.9), 
                'opacity'        : 0.1, 
                'specular'       : 1.0, 
                'diffuse'        : 0.8, 
                'specular_power' : 0.6,
                },
            },
        {
            'filename'   : 'test2.stl',
            'parameters' : {
                'color'          : (0.9, 0.9, 0.9), 
                'opacity'        : 1.0,
                'specular'       : 0.5,
                'diffuse'        : 0.5,
                'specular_power' : 0.7,
                }
            }
        ]

config = {
        'background' : (0.4, 0.4, 0.4),
        'size'       : (600,600),
        'objects'    : obj_list,
        }

with open('testconfig.pkl','w') as fid:
    pickle.dump(config,fid)

