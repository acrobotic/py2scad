"""
A bunch of random examples in no apparent order. However, almost every feature
is demonstrated here.
"""
from py2scad import *
import scipy

if 0:

    c = Circle(r=2.0)
    s = Square(size=[3,1])
    p = Polygon(points=[[0,0],[1,0],[1,1]], paths=[[0,1,2]])
    p.write('test.scad',fn=100)
    print p
    print c

if 0:

    c = Circle(r=1.0)
    c = Translate(c,v=[2,0,0])
    torus = Rotate_Extrude(c)
    torus.write('test.scad')
    print torus

if 1:

    x = scipy.linspace(0,8,500)

    points1 = []
    points2 = []
    for xx in x:
        y = scipy.cos(2.0*scipy.pi*xx)+0.3*scipy.cos(4.0*scipy.pi*xx) + 0.25
        points1.append([5.0*xx,y])
    for xx in x:
        y = scipy.cos(2.0*scipy.pi*xx)+0.3*scipy.cos(4.0*scipy.pi*xx) - 0.25 
        points2.append([5.0*xx,y])

    points2.reverse()
    points = points1 + points2

    paths = [range(0,len(points))]
    poly = Polygon(points, paths)
    part = Linear_Extrude(poly,h=40.0)
    c = Cylinder(h=5,r1=20,r2=20,mod='')
    c = Rotate(c,a=90,v=[1,0,0])
    c = Translate(c,v=[20,0,0])
    c2 = Cylinder(h=5,r1=2,r2=2,mod='')
    c2 = Rotate(c2,a=90,v=[1,0,0])
    c2 = Translate(c2,v=[20,0,0])
    part = Intersection([part,c])
    part = Difference([part,c2])
    prog = SCAD_Prog()
    prog.add(part)
    prog.fn = 50
    print prog
    prog.write('test.scad')



if 0:
    import math
    DEG2RAD = math.pi/180.0

    length = 11.0
    width = 5.0
    height = 0.5
    hole_diam = 0.1
    pat_radius = 0.4
    hole_ang = 30

    holes = []
    for x_shift in [-4.5,-3.0,-1.5, 0,1.5,3.0,4.5]:
        for y_shift in [-1.5,0, 1.5]:
            for ang in range(0,360,hole_ang):
                x = pat_radius*math.cos(DEG2RAD*ang) + x_shift
                y = pat_radius*math.sin(DEG2RAD*ang) + y_shift
                holes.append((x,y,hole_diam))

    plate = plate_w_holes(length,width,height,holes,hole_mod='')
    prog = SCAD_Prog()
    prog.add(plate)
    prog.fn=50
    prog.write('test.scad')
    print prog

if 0:

    c1 = Cylinder(h=0.5, r1=3.5, r2=3.5) 
    c3 = Cylinder(h=1.0, r1=2.6, r2=2.6)
    c1 = Difference([c1,c3])
    c2 = Cylinder(h=0.75, r1=1.5, r2=1.6)
    c2 = Translate(c2,v=[0,0,-4.5],mod='')
    c4 = Cylinder(h=0.75,r1=5.5,r2=5.5)
    c4 = Translate(c4,v=[0,0,4.5],mod='')
    c5 = Cylinder(h=1.0, r1=4.5, r2=4.5)
    c5 = Translate(c5,v=[0,0,4.5])
    c4 = Difference([c4,c5])
    h = Cylinder(h=10,r1=0.1,r2=0.1)
    h = Rotate(h,a=25,v=[0,1,0])
    h = Translate(h,v=[3,0,0])
    hr_list = []
    for ang in range(0,360,20):
        hr = Rotate(h,a=ang,v=[0,0,1],mod='%') 
        hr_list.append(hr)

    obj_list1 = [c1] + hr_list
    part1 = Difference(obj_list1)
    obj_list2 = [c2] + hr_list
    part2 = Difference(obj_list2)
    obj_list3 = [c4] + hr_list
    part3 = Difference(obj_list3)

    prog = SCAD_Prog()
    prog.add(part1)
    prog.add(part2)
    prog.add(part3)
    prog.fn=50
    prog.write('test.scad')
    print prog


if 0:

    # Note this example will fail in openscad if test.stl doesn't  exist
    model = Import_STL('test.stl')
    hole = Cylinder(h=10,r1=2,r2=2)
    hole = Translate(hole,v=[0,7,0],mod='')
    model = Difference([model,hole])

    prog = SCAD_Prog()
    prog.add(model)
    prog.fn=50
    prog.write('test.scad')

if 0:

    prog = SCAD_Prog()
    p = Cube(size=[15,15,1])
    p = Color(p,rgba=[0.5,0.5,0.5,1.0])
    c = Cylinder(h=5,r1=2,r2=1)
    c = Color(c,rgba=[0,1,0,1.0])
    s = Sphere(r=1)
    s = Color(s,rgba=[1,0,0,1.00])
    p = AnimRotate(p,a='$t*360.0',v=[1.0,0.0,0.0])
    c = AnimTranslate(c,v='[0.0,0.0,10.0*cos($t*360)]')
    s = AnimTranslate(s,v='[20*cos($t*360),10*sin($t*360*2),0]')

    prog.add(p)
    prog.add(c)
    prog.add(s)
    prog.fn=50
    prog.write('test.scad')

        
if 0:
    prog = SCAD_Prog()
    box = rounded_box(20,20,10,2.0)
    prog.add(box)
    #test = Cube(size=[20,20,10],mod='%')
    #prog.add(test)
    prog.fn=30
    prog.write('test.scad')

if 0:
    prog = SCAD_Prog()
    box = rounded_box(10,10,5,2.5)
    cube = rounded_box(20,20,5,0.5)
    box = Translate(box,v=[0,0,2.5])
    part = Difference([cube,box])
    prog.add(part)
    prog.fn=50
    prog.write('test.scad')


if 0:
    prog = SCAD_Prog()
    points = [[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]]
    
    faces = [[0,1,2,3],[7,6,5,4],[4,5,1,0],[5,6,2,1],[2,6,7,3],[0,3,7,4]]
    p = Polyhedron(points = points, faces = faces)
    p = Translate(p,v=[-0.5,-0.5,-0.5])
    prog.add(p)
    prog.fn=20
    prog.write('test.scad')

if 0:
    
    def sqr(x,y):
        return x**2 + y**2
    def gaussian(x,y):
        return scipy.exp(-(x**2+y**2)/1.0)

    prog = SCAD_Prog()
    #box = grid_box(1,1,0.1,30,30,top_func=sqr,bot_func=sqr)
    box = grid_box(5,5,0.1,50,50,top_func=gaussian,bot_func=gaussian)
    #box = grid_box(1,1,0.4,2,2,xy_func=None)
    cyl = Cylinder(h=4,r1=0.2,r2=0.2)
    part = Difference([box,cyl])
    #prog.add(box)
    #prog.add(cyl)
    prog.add(part)
    prog.fn=20
    prog.write('test.scad')

if 0:

    prog = SCAD_Prog()
    c = Circle(r=0.25)
    c = Translate(c,v=[2,0,0])
    torus = Rotate_Extrude(c)
    cut = wedge_cut(torus,145,270,4,2,mod='')
    prog.add(cut)
    prog.fn=30
    prog.write('test.scad')

if 0:
    prog = SCAD_Prog()
    p = partial_cylinder(5,1,2,90.0,360.0,mod='')
    prog.fn=40
    prog.add(p)
    prog.write('test.scad')

if 0:
    prog = SCAD_Prog()
    p = ellipse_edged_disk(1,5,edge_scale=1.5)
    prog.fn=40
    prog.add(p)
    prog.write('test.scad')

if 0:
    prog = SCAD_Prog()
    prog.fn = 40
    base = Cube(size=[2,3,0.1])
    cyl = Cylinder(h=3,r1=0.5, r2=0.5)
    part = Difference([base,cyl])
    part = Projection(part)
    prog.add(part)
    prog.write('test.scad')

