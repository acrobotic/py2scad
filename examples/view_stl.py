#!/usr/bin/env python
#
# view_stl.py - A simple vtk based stl file viewer
#
# Author: William Dickson 12/21/04
#
# --------------------------------------------------------------
import vtk
import sys
import optparse
import pickle

# Default parameters 
background = (0.1, 0.2, 0.4)
window_sz = (600,600)

# Set up options parser
usage = ''

parser = optparse.OptionParser(usage=usage)
parser.add_option('-c','--config', 
        help='plotting configuration file',
        action='store', 
        type='string', 
        dest='configfile')

options, args = parser.parse_args()

# Read stl file names given on the command line
stl_files = []
for f in args:
    stl_files.append((f,None))

# Read configuration file if it exists
if not options.configfile == None:

    with open(options.configfile,'r') as fid:
        config = pickle.load(fid)

    # Get background color and window size
    try:
        background = config['background']
    except KeyError:
        pass

    try:
        window_sz = config['size']
    except KeyError:
        pass

    # Read in list of stl objects and parameters
    if config.has_key('objects'):
        for obj in config['objects']:
            stl_files.append((obj['filename'],obj['parameters']))
          

# Create the Renderer, RenderWindow, and RenderWindowInteractor
ren = vtk.vtkRenderer()
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

# Set the background color and window size
ren.SetBackground(*background)
ren_win.SetSize(*window_sz)

# Create Actors for stl objects
for f, prm in stl_files:

    # Create the reader and read a data file.  
    sr = vtk.vtkSTLReader()
    sr.SetFileName(f)

    # Setup actors
    stl_mapper = vtk.vtkPolyDataMapper()
    stl_mapper.ScalarVisibilityOff()
    stl_mapper.SetInput(sr.GetOutput())

    stl_actor = vtk.vtkActor()
    stl_actor.SetMapper(stl_mapper)
    prop = stl_actor.GetProperty()

    if not prm == None:
        try:
            prop.SetColor(*prm['color'])
        except KeyError:
            pass
        try: 
            prop.SetOpacity(prm['opacity'])
        except KeyError:
            pass
        try:
            prop.SetSpecular(prm['specular'])
        except KeyError:
            pass
        try:
            prop.SetDiffuse(prm['diffuse'])
        except KeyError:
            pass
        try:
            prop.SetSpecularPower(prm['specular_power'])
        except KeyError:
            pass
        try:
            prop.SetAmbient(prm['ambient'])
        except KeyError:
            pass

    prop.SetInterpolationToGouraud()
    stl_mapper.Update()
    ren.AddActor(stl_actor)


# Render
iren.Initialize()
ren.ResetCameraClippingRange()
ren_win.Render()
iren.Start()
