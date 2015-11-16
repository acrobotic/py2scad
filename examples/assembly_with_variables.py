"""
An example of creating a parameterized assembly and using variables to make the
Scad output file more readable.
"""
import sys, os
from py2scad import *

# Setup the path to the Scad executable
scad = '' # Default to False
if sys.platform == 'darwin':
    scad = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
elif sys.platform == "win32":
    scad = r'"D:\Program files\OpenSCAD\OpenSCAD.exe"'

outfilename = "assembly.scad"

# This is just an example, so we are going to make pointless mounting plate!

########################### Variables ###########################
# Assume the user of the script might want to play with w/h/d and edge offsets
vars = Variables(width=50.0, height=25.0, depth=2.0, inset=3.0)
# Hole sizes are fixed though
bolt_dia = 3.0
hole_dia = 10.0
tol = 0.25 # Gap tolerance

########################### Assembly ############################
# Make a faux m3 socket head bolt assembly
m3_bolt = Assembly(name="m3bolt", parameters=["length"],
            obj=Union([
                # socket cylinder
                Translate(Cylinder(h=bolt_dia, r1=bolt_dia), [0,0,bolt_dia/2]),
                # threaded shaft
                Translate(Cylinder(h="length+1", r1=bolt_dia/2), [0,0,"-length/2"])
                ]),
            comment="Generate an m3 bolt at the specific length."
            )

############################# Part ##############################
# The part is just a cube with some holes, and transparent bolts in the holes
part = Difference([
    Cube(size=[vars.width, vars.height, vars.depth]),
    # Bolt holes
    Translate(Cylinder(h='2+'+vars.depth, r1=(bolt_dia/2)+tol),
              ["({0.width}/2)-{0.inset}".format(vars),
               "({0.height}/2)-{0.inset}".format(vars),
               0]
            ),
    Translate(Cylinder(h='2+'+vars.depth, r1=(bolt_dia/2)+tol),
              ["(-{0.width}/2)+{0.inset}".format(vars),
               "({0.height}/2)-{0.inset}".format(vars),
               0]
            ),
    Translate(Cylinder(h='2+'+vars.depth, r1=(bolt_dia/2)+tol),
              ["(-{0.width}/2)+{0.inset}".format(vars),
               "(-{0.height}/2)+{0.inset}".format(vars),
               0]
            ),
    Translate(Cylinder(h='2+'+vars.depth, r1=(bolt_dia/2)+tol),
              ["({0.width}/2)-{0.inset}".format(vars),
               "(-{0.height}/2)+{0.inset}".format(vars),
               0]
            ),
    # Bolts
    Union([
        Translate(m3_bolt(16),
                  ["({0.width}/2)-{0.inset}".format(vars),
                   "({0.height}/2)-{0.inset}".format(vars),
                   0]
                ),
        Translate(m3_bolt(16),
                  ["(-{0.width}/2)+{0.inset}".format(vars),
                   "({0.height}/2)-{0.inset}".format(vars),
                   0]
                ),
        Translate(m3_bolt(16),
                  ["(-{0.width}/2)+{0.inset}".format(vars),
                   "(-{0.height}/2)+{0.inset}".format(vars),
                   0]
                ),
        Translate(m3_bolt(16),
                  ["({0.width}/2)-{0.inset}".format(vars),
                   "(-{0.height}/2)+{0.inset}".format(vars),
                   0]
                )],
        mod='%'
    ),
    # Center hole
    Cylinder(h=vars['depth']+2, r1=hole_dia/2)

])


design = SCAD_Prog()
design.add([vars, m3_bolt, part])
design.write(outfilename)

if scad: # If we can find scad
    # Generate a stl file in the same dir with the same namd as the scad file
    os.system('{scad} -s {stl} {file}'.format(scad=scad,
                                              stl=outfilename.replace('.scad', '.stl'),
                                              file=outfilename))
