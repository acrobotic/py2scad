"""
Copyright 2010  IO Rodeo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import base
import utility

# Variable delcaration -------------------------------------------------------

class Variables(dict):
    """Group variable declarations for inclusion in output file."""
    # Any constructor kwargs become variables
    # Attribute getter returns the varaible name
    # Attribute setter sets variable value
    # cmd_str method returns variable definition in scad syntax
    def __init__(self, comment='', **kwargs):
        self.comment = comment
        if not comment:
            self.comment = "Named variables //\n"
        dict.__init__(self, kwargs)
        self._initialised = True

    def __getattr__(self, name):
        """Return the openscad representation of the indicated variable."""
        if name in self:
            return name
        raise AttributeError(name)

    def __setattr__(self, name, value):
        """Change the value of the named variable."""
        if not self.__dict__.has_key('_initialised'):  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, name, value)
        elif name in self: # any normal attributes are handled normally
            dict.__setattr__(self, name, value)
        else:
            self.__setitem__(name, value)

    def cmd_str(self, tab_level=0):
        tab_str = ' '*utility.TAB_WIDTH*tab_level
        rtn_str = ''
        for k,v in self.items():
            rtn_str += '{0}{1} = {2};\n'.format(tab_str, k, utility.val_to_str(v))
        return rtn_str + '\n'

    def __str__(self, tab_level=0):
        tab_str = ' '*utility.TAB_WIDTH*tab_level
        comment = ''
        if self.comment:
            comment = tab_str + '// ' + self.comment + '\n'
        return '\n{0}{1}'.format(comment, self.cmd_str(tab_level=tab_level))


# 3D primitives ---------------------------------------------------------------

class Cube(base.SCAD_Object):

    def __init__(self, size=1.0, center=True, *args, **kwargs):
        base.SCAD_Object.__init__(self, center=center, *args, **kwargs)
        self.size = size

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        size_str = utility.val_to_str(self.size)
        center_str = self.center_str()
        return 'cube(size={0}, center={1}{2});'.format(size_str,
                                                       center_str,
                                                       facets)

class Sphere(base.SCAD_Object):

    def __init__(self, r=1.0, center=True, *args, **kwargs):
        base.SCAD_Object.__init__(self, center=center, *args, **kwargs)
        self.r = r

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        r_str = utility.val_to_str(self.r)
        center_str = self.center_str()
        return 'sphere(r={0}, center={1}{2});'.format(r_str,
                                                      center_str,
                                                      facets)

class Cylinder(base.SCAD_Object):

    def __init__(self, h=1.0, r1=1.0, r2=None, center=True, *args, **kwargs):
        base.SCAD_Object.__init__(self, center=center, *args, **kwargs)
        self.h = h
        self.r1 = r1
        # r2 is optional
        self.r2 = r2

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        center_str = self.center_str()
        h_str = utility.val_to_str(self.h)
        r1_str = utility.val_to_str(self.r1)
        if self.r2:
            r2_str = utility.val_to_str(self.r2)
            return 'cylinder(h={0},r1={1},r2={2},center={3});'.format(h_str,
                                                                      r1_str,
                                                                      r2_str,
                                                                      center_str,
                                                                      facets)
        # When Cylinder is constant radius the argument is just called 'r'
        return 'cylinder(h={0},r={1},center={2}{3});'.format(h_str,
                                                             r1_str,
                                                             center_str,
                                                             facets)

class Polyhedron(base.SCAD_Object):

    def __init__(self, points, faces, center=True, *args, **kwargs):
        base.SCAD_Object.__init__(self, center=center, *args, **kwargs)
        self.points = points
        self.faces = faces

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        tab_str0 = ' '*utility.TAB_WIDTH*tab_level
        tab_str1 = ' '*utility.TAB_WIDTH*(tab_level+1)
        rtn_str = 'polyhedron(\n'
        rtn_str = '%s%spoints = [\n'%(rtn_str,tab_str1,)
        for p in self.points:
            p_str = utility.val_to_str(p,tab_level=tab_level+2)
            rtn_str = '%s%s,\n'%(rtn_str,p_str)
        rtn_str = '%s%s],\n'%(rtn_str,tab_str1,)
        rtn_str = '%s%striangles = [\n'%(rtn_str,tab_str1,)
        for p in self.faces:
            p_str = utility.val_to_str(p,tab_level=tab_level+2)
            rtn_str = '%s%s,\n'%(rtn_str,p_str)
        rtn_str = '%s%s]\n'%(rtn_str,tab_str1,)
        rtn_str += facets
        rtn_str = '%s%s);\n'%(rtn_str,tab_str0)
        return rtn_str

class Import_STL(base.SCAD_Object):

    def __init__(self, filename, convexity=5, *args, **kwargs):
        base.SCAD_Object.__init__(self, *args, **kwargs)
        self.filename = filename
        self.convexity = convexity

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        return 'import_stl("{0.filename}",convexity={0.convexity:d}{1});'.format(self, facets)

# 2D primatives ---------------------------------------------------------------

class Circle(base.SCAD_Object):

    def __init__(self, r=1, *args, **kwargs):
        base.SCAD_Object.__init__(self, *args, **kwargs)
        self.r = r

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        r_str = utility.val_to_str(self.r)
        rtn_str = 'circle(r={0}{1});'.format(r_str, facets)
        return rtn_str

class Square(base.SCAD_Object):

    def __init__(self, size=[1,1], center=True, *args, **kwargs):
        base.SCAD_Object.__init__(self, center=center, *args, **kwargs)
        self.size = size

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        size_str = utility.val_to_str(self.size)
        center_str = self.center_str()
        return 'square(size={0}, center={1}{2});'.format(size_str,
                                                        center_str,
                                                        facets)

class Polygon(base.SCAD_Object):

    def __init__(self, points, paths,  *args, **kwargs):
        base.SCAD_Object.__init__(self, *args, **kwargs)
        self.points = points
        self.paths = paths

    def cmd_str(self,tab_level=0):
        facets = self.facets() # Retreve object facet information
        tab_str0 = ' '*utility.TAB_WIDTH*tab_level
        tab_str1 = ' '*utility.TAB_WIDTH*(tab_level+1)
        rtn_str = 'polygon(\n'
        rtn_str = '%s%spoints = [\n'%(rtn_str,tab_str1,)
        for p in self.points:
            p_str = utility.val_to_str(p,tab_level=tab_level+2)
            rtn_str = '%s%s,\n'%(rtn_str,p_str)
        rtn_str = '%s%s],\n'%(rtn_str,tab_str1,)
        rtn_str = '%s%spaths = [\n'%(rtn_str,tab_str1,)
        for p in self.paths:
            p_str = utility.val_to_str(p,tab_level=tab_level+2)
            rtn_str = '%s%s,\n'%(rtn_str,p_str)
        rtn_str = '%s%s]\n'%(rtn_str,tab_str1,)
        rtn_str += facets
        rtn_str = '%s%s);\n'%(rtn_str,tab_str0)
        return rtn_str

if __name__ == "__main__":
    v = Variables(foo=5)
    v.bar = [10, 2, 4]
    v.baz = "strings aren't usefull yet!"
    print("{0.foo}, {0.bar}, {0.baz}".format(v))
    print(v)
