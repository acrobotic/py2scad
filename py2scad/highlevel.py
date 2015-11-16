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
try:
    import scipy as numpy
except ImportError:
    import numpy
from primitives import *
from transforms import *
from utility import DEG2RAD
from utility import RAD2DEG

INCH2MM = 25.4

class Basic_Enclosure(object):

    """
    Creates a basic tabbed enclosure for laser cutting. The enclosure is designed
    to be help together without any gluing (or solvent welding) using standoffs.

    Need to add more documentaion on how to use this class ...
    """

    def __init__(self,params):
        self.params = params 

    def make_top_and_bottom(self):
        """
        Create top and bottom panels of the enclosure.
        """
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        top_x_overhang = self.params['top_x_overhang']
        top_y_overhang = self.params['top_y_overhang']
        bottom_x_overhang = self.params['bottom_x_overhang']
        bottom_y_overhang = self.params['bottom_y_overhang']
        lid_radius = self.params['lid_radius']

        # Add slots for tabs
        slot_list = []
        lid2front_tab_width = self.params['lid2front_tab_width']
        lid2side_tab_width = self.params['lid2side_tab_width']

        # Add lid to front slots
        for loc in self.params['lid2front_tabs']:
            for sign in (-1,1):
                x_pos = inner_x*loc - 0.5*inner_x
                y_pos = sign*(0.5*inner_y + 0.5*wall_thickness)
                x_size = lid2front_tab_width
                y_size = wall_thickness
                slot = ((x_pos, y_pos), (x_size, y_size))
                slot_list.append(slot)

        # Add lid to side slots
        for loc in self.params['lid2side_tabs']:
            for sign in (-1,1):
                x_pos = sign*(0.5*inner_x + 0.5*wall_thickness)
                y_pos = (inner_y + 2*wall_thickness)*loc - 0.5*(inner_y +2*wall_thickness)
                x_size = wall_thickness
                y_size = lid2side_tab_width
                slot = ((x_pos, y_pos), (x_size, y_size))
                slot_list.append(slot)

        # Get dimensions of top and bottom panels
        top_x = inner_x + 2.0*(wall_thickness + top_x_overhang)
        top_y = inner_y + 2.0*(wall_thickness + top_y_overhang)
        top_z = wall_thickness
        self.top_x, self.top_y = top_x, top_y

        bottom_x = inner_x + 2.0*(wall_thickness + bottom_x_overhang)
        bottom_y = inner_y + 2.0*(wall_thickness + bottom_y_overhang)
        bottom_z = wall_thickness
        self.bottom_x, self.bottom_y = bottom_x, bottom_y

        # Create top and bottom panels
        self.top = rounded_box(top_x, top_y, top_z, lid_radius, round_z=False)
        self.bottom = rounded_box(bottom_x, bottom_y, bottom_z, lid_radius, round_z=False)

        # Create slot holes for top and bottom panels
        self.tab_hole_list = []
        for panel in ('top', 'bottom'):
            for pos, size in slot_list:
                hole = {
                        'panel'    : panel,
                        'type'     : 'square',
                        'location' : pos,
                        'size'     : size,
                        }
                self.tab_hole_list.append(hole)

        # Add holes for standoffs
        standoff_diameter = self.params['standoff_diameter']
        standoff_offset = self.params['standoff_offset']
        standoff_hole_diameter = self.params['standoff_hole_diameter']

        self.standoff_hole_list = []
        self.standoff_xy_pos = []
        self.standoff_list = []
        for i in (-1,1):
            for j in (-1,1):
                # Create holes for standoffs
                x = i*(0.5*inner_x - 0.5*standoff_diameter - standoff_offset)
                y = j*(0.5*inner_y - 0.5*standoff_diameter - standoff_offset)
                self.standoff_xy_pos.append((x,y))
                top_hole = {
                        'panel'     : 'top',
                        'type'      : 'round',
                        'location'  : (x,y),
                        'size'      : standoff_hole_diameter,
                        }
                bottom_hole = {
                        'panel'     : 'bottom',
                        'type'      : 'round',
                        'location'  : (x,y),
                        'size'      : standoff_hole_diameter,
                        }
                self.standoff_hole_list.append(top_hole)
                self.standoff_hole_list.append(bottom_hole)

                # Create standoff cylinders
                r = 0.5*standoff_diameter
                standoff = Cylinder(r1=r, r2=r, h=inner_z)
                self.standoff_list.append(standoff)

        hole_list = self.tab_hole_list + self.standoff_hole_list
        self.add_holes(hole_list)

    def make_left_and_right(self):
        """
        Creates the left and right side panels of the enclosure.
        Positive tabs can be adjusted independently by passing a 
        dictionary:
        tab_depth_adjust = {'top': , 'bot': , 'side': }
        Note: 'side' key is only used while makeing front and back (below)
        """
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        lid2side_tab_width = self.params['lid2side_tab_width']
        side2side_tab_width = self.params['side2side_tab_width']

        try:
            depth_adjust = self.params['tab_depth_adjust']
        except KeyError:
            depth_adjust = 0.0

        if type(depth_adjust)==dict:
            try:
                depth_adjust_pos = depth_adjust['top']
            except KeyError:
                depth_adjust_pos = 0.0
            try:
                depth_adjust_neg = depth_adjust['bot']
            except KeyError:
                depth_adjust_neg = 0.0
        else:
            depth_adjust_pos = depth_adjust 
            depth_adjust_neg = depth_adjust

        # Only apply tab depth adjustment to positive tabs
        tab_depth_pos_pos = wall_thickness + depth_adjust_pos
        tab_depth_pos_neg = wall_thickness + depth_adjust_neg
        tab_depth_neg = wall_thickness

        # Create tab data for yz faces of side panels
        xz_pos = []
        xz_neg = []
        for loc in self.params['lid2side_tabs']:
            tab_data = (loc, lid2side_tab_width, tab_depth_pos_pos, '+')
            xz_pos.append(tab_data)
            tab_data = (loc, lid2side_tab_width, tab_depth_pos_neg, '+')
            xz_neg.append(tab_data)

        # Create tab data for xz faces of side panels
        yz_pos = []
        yz_neg = []
        for loc in self.params['side2side_tabs']:
            tab_data = (loc, side2side_tab_width, tab_depth_neg, '-')
            yz_pos.append(tab_data)
            yz_neg.append(tab_data)

        # Pack panel data into parameters structure
        params = {
                'size' : (inner_y+2*wall_thickness, inner_z, wall_thickness),
                'xz+'  : xz_pos,
                'xz-'  : xz_neg,
                'yz+'  : yz_pos,
                'yz-'  : yz_neg,
                }

        plate_maker = Plate_W_Tabs(params)
        self.left = plate_maker.make()
        self.right = plate_maker.make()
        
    def make_front_and_back(self):
        """
        Creates the front and back panels of the enclosure.
        Positive tabs can be adjusted independently by passing a 
        dictionary:
        tab_depth_adjust = {'top': , 'bot': , 'side': }
        """
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        lid2front_tab_width =  self.params['lid2front_tab_width']
        side2side_tab_width = self.params['side2side_tab_width']
        
        try:
            depth_adjust = self.params['tab_depth_adjust']
        except KeyError:
            depth_adjust = 0.0

        if type(depth_adjust)==dict:
            try:
                depth_adjust_pos = depth_adjust['top']
            except KeyError:
                depth_adjust_pos = 0.0
            try:
                depth_adjust_neg = depth_adjust['bot']
            except KeyError:
                depth_adjust_neg = 0.0
            try:
                depth_adjust_side = depth_adjust['side']
            except KeyError:
                depth_adjust_side = 0.0
        else:
            depth_adjust_pos = depth_adjust 
            depth_adjust_neg = depth_adjust
            depth_adjust_side = depth_adjust

        # Only apply tab depth adjustment to positive tabs
        tab_depth_pos_pos = wall_thickness + depth_adjust_pos
        tab_depth_pos_neg = wall_thickness + depth_adjust_neg
        tab_depth_pos_side = wall_thickness + depth_adjust_side

        # Create tab data for xz faces of front and back panels
        xz_pos = []
        xz_neg = []
        for loc in self.params['lid2front_tabs']:
            tab_data = (loc, lid2front_tab_width, tab_depth_pos_pos, '+')
            xz_pos.append(tab_data)
            tab_data = (loc, lid2front_tab_width, tab_depth_pos_neg, '+')
            xz_neg.append(tab_data)

        # Create tab data for yz faces of front and back panels
        yz_pos = []
        yz_neg = []
        for loc in self.params['side2side_tabs']:
            tab_data = (loc, side2side_tab_width, tab_depth_pos_side, '+')
            yz_pos.append(tab_data)
            tab_data = (loc, side2side_tab_width, tab_depth_pos_side, '+')
            yz_neg.append(tab_data)

        # Pack panel data into parameters structure
        params = {
                'size' : (inner_x, inner_z, wall_thickness),
                'xz+'  : xz_pos,
                'xz-'  : xz_neg,
                'yz+'  : yz_pos,
                'yz-'  : yz_neg,
                }

        plate_maker = Plate_W_Tabs(params)
        self.front = plate_maker.make()
        self.back = plate_maker.make()

    def add_holes(self, hole_list, cut_depth = None):
        """
        Add holes to given panel of the enclosure.
        """
        if not cut_depth:
            cut_depth = 2*self.params['wall_thickness']

        #panels2holes = {}

        for hole in hole_list:

            # Create differencing cylinder for hole based on hole type.
            if hole['type'] == 'round':
                radius = 0.5*hole['size']
                hole_cyl = Cylinder(r1=radius, r2=radius, h=cut_depth)
            elif hole['type'] == 'square':
                sz_x, sz_y = hole['size']
                sz_z = cut_depth 
                hole_cyl = Cube(size = (sz_x,sz_y,sz_z))
            elif hole['type'] == 'rounded_square':
                sz_x, sz_y, radius = hole['size']
                sz_z = cut_depth 
                hole_cyl = rounded_box(sz_x, sz_y, sz_z, radius, round_z=False)
            else:
                raise ValueError, 'unkown hole type {0}'.format(hole['type'])

            # Translate cylinder into position
            x,y = hole['location']
            hole_cyl = Translate(hole_cyl, v = (x,y,0.0))

            # Get panel in which to make hole
            panel = getattr(self, hole['panel'])

            # Cut hole
            panel = Difference([panel, hole_cyl])
            setattr(self, hole['panel'], panel)

            #try:
            #    panels2holes[hole['panel']].append(hole_cyl)
            #except KeyError:
            #    panels2holes[hole['panel']] = [hole_cyl]

        #for panel_name, panel_holes in panels2holes.iteritems():
        #    panel = getattr(self, hole['panel'])
        #    panel = Difference([panel] + panel_holes)
        #    setattr(self, hole['panel'], panel)




    def make(self):
        self.make_left_and_right()
        self.make_front_and_back()
        self.make_top_and_bottom()
        if self.params.has_key('hole_list'):
            self.add_holes(self.params['hole_list'])

    def get_assembly(self,**kwargs):
        """
        Returns a list of the enclosure parts in assembled positions.
        """
        assembly_options= {
                'explode'       : (0,0,0), 
                'show_top'      : True, 
                'show_bottom'   : True, 
                'show_front'    : True,
                'show_back'     : True, 
                'show_left'     : True, 
                'show_right'    : True, 
                'show_standoffs': True,
                }
        assembly_options.update(kwargs)
        explode = assembly_options['explode']
        
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        explode_x, explode_y, explode_z = explode

        # Translate top and bottom into assembled positions
        top_z_shift = 0.5*inner_z + 0.5*wall_thickness + explode_z
        bottom_z_shift = -top_z_shift
        top = Translate(self.top, v=(0.0,0.0,top_z_shift))
        bottom = Translate(self.bottom,v=(0.0,0.0,bottom_z_shift))

        # Rotate and translate front and back into assembled positions
        back = Rotate(self.back, a=90, v=(1,0,0))
        front = Rotate(self.front, a=90, v=(1,0,0))
        back_y_shift = 0.5*inner_y + 0.5*wall_thickness + explode_y
        front_y_shift = -back_y_shift
        back = Translate(back, v=(0.0, back_y_shift, 0.0))
        front = Translate(front, v=(0.0, front_y_shift, 0.0))

        # Rotate and translate sides into assembled positions
        right = Rotate(self.right, a=90, v=(0,0,1))
        right = Rotate(right, a=90, v=(0,1,0))
        left = Rotate(self.left, a=90, v=(0,0,1))
        left = Rotate(left, a=90, v=(0,1,0))
        right_x_shift = 0.5*inner_x + 0.5*wall_thickness + explode_x
        left_x_shift = -right_x_shift
        right = Translate(right,v=(right_x_shift,0,0))
        left = Translate(left,v=(left_x_shift,0,0))

        # Translate standoffs into position
        standoff_list = []
        for pos, standoff in zip(self.standoff_xy_pos, self.standoff_list):
            x_shift, y_shift = pos
            z_shift = 0.0
            standoff = Translate(standoff,v=(x_shift,y_shift,z_shift))
            standoff_list.append(standoff)

        # Return list of parts in assembly
        part_list = []
        if assembly_options['show_top'] == True:
            part_list.append(top)
        if assembly_options['show_bottom'] == True:
            part_list.append(bottom)
        if assembly_options['show_front'] == True:
            part_list.append(front)
        if assembly_options['show_back'] == True:
            part_list.append(back)
        if assembly_options['show_left'] == True:
            part_list.append(left)
        if assembly_options['show_right'] == True:
            part_list.append(right)
        if assembly_options['show_standoffs'] == True:
            part_list.extend(standoff_list)
        return part_list


    def get_projection(self, show_ref_cube=True, spacing_factor=4, project=True, exclude_list=[]):
        """
        Retruns a list of enclosure parts as 2D projections for saving as a dxf file.

        All Parts, except the floor,  are rotated so that their outside faces are up in the projection.
        This is done to make adding text for etching easier.
        """
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        top_x_overhang = self.params['top_x_overhang']
        top_y_overhang = self.params['top_y_overhang']
        bottom_x_overhang = self.params['bottom_x_overhang']
        bottom_y_overhang = self.params['bottom_y_overhang']
        spacing = spacing_factor*wall_thickness
        bottom = self.bottom

        # Translate front panel
        y_shift = -(0.5*self.bottom_y + 0.5*inner_z + wall_thickness + spacing)
        front = Translate(self.front, v=(0,y_shift,0))

        # Translate back panel
        y_shift = 0.5*self.bottom_y + 0.5*inner_z + wall_thickness + spacing
        back = Rotate(self.back,a=180,v=(1,0,0)) # Rotate part so that outside face is up in projection
        back = Translate(back, v=(0,y_shift,0))

        # Rotate and Translate left panel
        left = Rotate(self.left,a=90,v=(0,0,1))
        left = Rotate(left,a=180,v=(0,1,0)) # Rotate part so that outside face is up in projection
        x_shift = -(0.5*self.bottom_x + 0.5*inner_z + wall_thickness + spacing)
        left = Translate(left, v=(x_shift,0,0))

        # Rotate and translate right panel
        right = Rotate(self.right,a=90,v=(0,0,1))
        x_shift = 0.5*self.bottom_x + 0.5*inner_z + wall_thickness + spacing
        right = Translate(right,v=(x_shift,0,0))

        # Rotate and translate top
        y_shift = -(0.5*self.bottom_y + 0.5*self.top_y + inner_z + 2*wall_thickness + 2*spacing)
        top = Translate(self.top, v=(0,y_shift,0))

        # Create reference cube
        ref_cube = Cube(size=(INCH2MM,INCH2MM,INCH2MM))
        y_shift = 0.5*self.bottom_y + 0.5*INCH2MM + inner_z + 2*wall_thickness + 2*spacing
        ref_cube = Translate(ref_cube,v=(0,y_shift,0))

        # Create part list
        part_dict = {
                'top'     : top, 
                'bottom'  : bottom, 
                'front'   : front, 
                'back'    : back, 
                'left'    : left,
                'right'   : right
                }
        part_list= []
        for name, part in part_dict.iteritems():
            if name in exclude_list:
                continue
            part_list.append(part)

        #part_list = [top, bottom, front, back, left, right]

        if show_ref_cube == True:
            part_list.append(ref_cube)

        # Project parts
        part_list_proj = []
        for part in part_list:
            if project:
                part_list_proj.append(Projection(part))
            else:
                part_list_proj.append(part)


        return part_list_proj


class Plate_W_Slots(object):

    """
    Creates a plate with square (rectangular) slots. Plate is assumed to lie in the
    x-y plane and the holes are cut through the xy faces.

    Usage:

    plate_maker = Plate_W_Slots(params)
    plate = plate_maker.make()

    where:

    params = {
        'size'   : (x,y,z),    # plate size
        'radius' : radius,     # plate raduis if not given assumed to be none
        'slots'  : slot_list,  # list of hole data
    }

    slot_list = [
        (pos_0, size_0),  # position and size of slot 0
        (pos_1, size_1),  # position and size of slot 1
        ... etc
        ]

    pos_i  = (pos_x, pos_y)    # the x and y coordinates of slot i
    size_i = (size_x, size_y)  # the x and y dimensions of slot i
    """

    def __init__(self, params):
        self.params = params

    def __add_holes(self):

        hole_list = []

        for pos, size in self.params['slots']:
            x, y = size
            z = 2*self.params['size'][2]
            hole = Cube(size=(x, y, z))
            pos_x, pos_y = pos
            hole = Translate(hole,v=[pos_x, pos_y, 0])
            hole_list.append(hole)

        self.plate = Difference([self.plate] + hole_list)


    def make(self):
        try:
            radius = self.params['radius']
        except KeyError:
            radius = None

        if radius is None:
            self.plate = Cube(size=self.params['size'])
        else:
            x,y,z = self.params['size']
            self.plate = rounded_box(x, y, z, radius, round_z=False)

        self.__add_holes()
        return self.plate

class Plate_W_Tabs(object):

    """
    Creates a plate with tabs on the xz and yz faces.

    Usage:

    plate_maker = Tabbed_Plate(params)  where
    plate = plate_maker.make()

    params is a dictionary of the plate's parameters:

    params = {
        'size' : (x,y,z),   # size of plate
        'xz+'  : xz_pos,    # tab data for positive xz face
        'xz-'  : xz_neg,    # tab data for negative xz face
        'yz+'  : yz_pos,    # tab data for positive yz face
        'yz-'  : yz_neg,    # tab data for negative yz face
        }

    the tab data are lists with the follow form:

    tab_data = [
        (pos_0, width_0, depth_0, dir_0),  # data for 0th tab
        (pos_1, width_1, depth_1, dir_1),  # data for 1st tab
        ... etc
        ]

    Where for the i-th tab:

    pos_i   =  position of tab as a fraction of face length. Face length is either
        x or y dimension of plate depending on whether tab is on the xz or yz
        face of the plate.
    width_i =  width of tab along x or y dimension depending of whether tab is on
        the xz or yz face of the plate.
    depth_i =  depth of the tab
    dir_i   =  direction of the tab (either '+' or '-').
    """

    def __init__(self, params):
        self.params = params

    def __add_tabs(self):

        plate_x, plate_y, plate_z = self.params['size']
        pos_tab_list = []
        neg_tab_list = []

        # Loop over face types
        for face in ('xz', 'yz'):

            # Loop over sign of faces
            for sign, sign_val in (('+',1), ('-',-1)):
                tab_data = self.params[face+sign]

                for fpos, width, depth, tab_dir in tab_data:
                    # Make removed tabs, those wth '-' tab_dir, thicker than plate
                    if tab_dir == '-':
                        thickness = 1.5*plate_z
                    else:
                        thickness = plate_z

                    if face == 'xz':
                        # Create tabs for the xz faces
                        tab = Cube(size=(width,2*depth,thickness))
                        tx = fpos*plate_x - 0.5*plate_x
                        ty = sign_val*0.5*plate_y
                        tab = Translate(tab, v=(tx,ty,0))
                    elif face == 'yz':
                        # Create tabs for the yz faces
                        tab = Cube(size=(2*depth,width,thickness))
                        tx = sign_val*0.5*plate_x
                        ty = fpos*plate_y - 0.5*plate_y
                        tab = Translate(tab,v=(tx,ty,0))

                    # Add tabs to appropriate list of tabs based on sign of tab
                    if tab_dir == '+':
                        pos_tab_list.append(tab)
                    elif tab_dir == '-':
                        neg_tab_list.append(tab)

        # Add material for positive tabs
        if len(pos_tab_list) > 0:
            self.plate = Union([self.plate] + pos_tab_list)

        # Remove material for negative tabs
        if len(neg_tab_list) > 0:
            self.plate = Difference([self.plate] + neg_tab_list)


    def make(self):
        """
        Creates a tabbed plate.
        """
        self.plate = Cube(size=self.params['size'])
        self.__add_tabs()
        return self.plate


class Right_Angle_Bracket(object):

    """
    Creates a tabbed right angle bracket for laser cutting.

    Need to add more documenttion for this class.
    """

    def __init__(self,params):
        self.params = params

    def __make_base_and_face(self):
        """
        Makes the base and face plates of the bracket.
        """

        # Get tab directions for base and face
        base_tab_dir = self.params['base_tab_dir']
        if base_tab_dir == '+':
            face_tab_dir = '-'
        elif base_tab_dir == '-':
            face_tab_dir = '+'
        else:
            raise ValueError, "unknown tab direction, {0}, must be '+' or '-'".format(base_tab_dir)

        # Get base size
        base_x = self.params['base_width']
        base_y = self.params['base_depth']
        base_z = self.params['base_thickness']
        self.base_size = base_x, base_y, base_z

        # Get face size
        face_x = self.params['face_width']
        face_y = self.params['face_height']
        face_z = self.params['face_thickness']
        self.face_size = face_x, face_y, face_z

        # Create base plate
        xz_pos = []
        for tab_data in self.params['base2face_tabs']:
            tab_data = list(tab_data)
            tab_data.append(base_tab_dir)
            xz_pos.append(tuple(tab_data))

        xz_neg = []
        yz_pos = []
        yz_neg = []

        base_params = {
                'size' : self.base_size,
                'xz+'  : xz_pos,
                'xz-'  : xz_neg,
                'yz+'  : yz_pos,
                'yz-'  : yz_neg,
                }

        base_maker = Plate_W_Tabs(base_params)
        self.base = base_maker.make()

        # Create face plate
        xz_neg = []
        for tab_data in self.params['base2face_tabs']:
            fpos_base, width, depth = tab_data
            fpos_face = (base_x*fpos_base - 0.5*base_x + 0.5*face_x)/face_x
            tab_data = (fpos_face, width, depth, face_tab_dir)
            xz_neg.append(tab_data)

        xz_pos = []
        yz_pos = []
        yz_neg = []

        face_params = {
                'size' : self.face_size,
                'xz+'  : xz_pos,
                'xz-'  : xz_neg,
                'yz+'  : yz_pos,
                'yz-'  : yz_neg,
                }

        face_maker = Plate_W_Tabs(face_params)
        self.face = face_maker.make()

        self.__add_slots()


    def __add_slots(self):
        """
        Add slots to base and face plates
        """
        # Add slots for support tabs
        hole_list = []
        for support_data in self.params['supports']:
            support_pos = support_data['pos']
            support_params = support_data['params']
            support_thickness = support_params['thickness']
            support_depth = support_params['depth']
            support_height = support_params['height']

            for tab_data in support_params['face_tabs']:
                fpos, width, depth = tab_data
                x_loc = support_pos
                y_loc = fpos*support_height - 0.5*self.face_size[1] + self.base_size[2]

                # Make slots in face
                hole = {
                        'plate'    : 'face',
                        'type'     : 'square',
                        'size'     : (support_thickness, width),
                        'location' : (x_loc, y_loc),
                        }
                hole_list.append(hole)

            for tab_data in support_params['base_tabs']:
                fpos, width, depth = tab_data
                x_loc = support_pos
                y_loc = -fpos*support_depth + 0.5*self.base_size[1]

                # Make slots in base
                hole = {
                        'plate'    : 'base',
                        'type'     : 'square',
                        'size'     : (support_thickness,width),
                        'location' : (x_loc, y_loc),
                        }
                hole_list.append(hole)

        self.add_holes(hole_list)

    def __make_supports(self):
        """
        Makes the right triangle supports for the bracket.
        """
        self.support_list = []
        self.support_pos_list = []
        for support_data in self.params['supports']:
            support_params = support_data['params']
            x = support_params['depth']
            y = support_params['height']
            z = support_params['thickness']
            face_tabs = [list(val) + ['+'] for val in support_params['face_tabs']]
            base_tabs = [list(val) + ['+'] for val in support_params['base_tabs']]
            triangle_params = {
                    'size' : (x,y,z),
                    'xz'   : base_tabs,
                    'yz'   : face_tabs,
                    'hz'   : [],
                    }
            support_maker = RT_Triangle_W_Tabs(triangle_params)
            support = support_maker.make()
            self.support_list.append(support)
            self.support_pos_list.append(support_data['pos'])

    def add_holes(self, hole_list):
        """
        Add holes to base or face
        """
        # Get plate in which to cut hole
        thickness = max([self.base_size[2], self.face_size[2]])

        for hole in hole_list:

            # Create differencing cylinder for hole based on hole type.
            if hole['type'] == 'round':
                radius = 0.5*hole['size']
                hole_cyl = Cylinder(r1=radius, r2=radius, h = 2*thickness)
            elif hole['type'] == 'square':
                sz_x, sz_y = hole['size']
                sz_z = 2*thickness
                hole_cyl = Cube(size = (sz_x,sz_y,sz_z))
            elif hole['type'] == 'rounded_square':
                sz_x, sz_y, radius = hole['size']
                sz_z = 2*thickness
                hole_cyl = rounded_box(sz_x, sz_y, sz_z, radius, round_z=False)
            else:
                raise ValueError, 'unkown hole type {0}'.format(hole['type'])

            # Translate hole cylinder into position
            x,y = hole['location']
            hole_cyl = Translate(hole_cyl,v=(x,y,0))

            # Get plate in which to make hole
            plate = getattr(self, hole['plate'])

            # Cut hole
            plate = Difference([plate, hole_cyl])
            setattr(self, hole['plate'], plate)


    def make(self):
        """
        Create parts.
        """
        self.__make_base_and_face()
        self.__make_supports()
        if self.params.has_key('hole_list'):
            self.add_holes(self.params['hole_list'])


    def get_assembly(self,explode=(0,0,0)):
        """
        Returns list of parts in assembled positions.
        """
        explode_x, explode_y, explode_z = explode

        # Position base and face plates
        face = Rotate(self.face,a=90,v=(1,0,0))
        y_shift = 0.5*self.base_size[1] + 0.5*self.face_size[2] + explode_y
        z_shift = 0.5*self.face_size[1] - 0.5*self.base_size[2] + explode_z
        face = Translate(face,v=(0,y_shift,z_shift))

        # Add supports
        support_list = []
        for pos, support in zip(self.support_pos_list, self.support_list):
            support = Rotate(support, a=90, v=(1,0,0))
            support = Rotate(support, a=-90, v=(0,0,1))
            x_shift = pos
            y_shift = 0.5*self.base_size[1]
            z_shift = 0.5*self.base_size[2] + explode_z
            support = Translate(support,v=(x_shift,y_shift,z_shift))
            support_list.append(support)

        return [self.base, face,] + support_list

    def get_projection(self,show_ref_cube=True,spacing_factor=2):
        """
        Returns list of parts as 2D projections.

        Not done yet
        """
        # Determine spacing based on thicknesses
        support_thickness_list = []
        for support_data in self.params['supports']:
            support_thickness_list.append(support_data['params']['thickness'])
        max_support_thickness = max(support_thickness_list)
        thickness_list = [self.params['base_thickness'], self.params['face_thickness'],max_support_thickness]
        spacing = spacing_factor*max(thickness_list)

        # Translate base into position
        tx = -max([0.5*self.base_size[0], 0.5*self.face_size[0]]) - 0.5*spacing
        ty = -0.5*self.base_size[1] -0.5*spacing
        base = Translate(self.base, v=(tx,ty,0))

        # Translate face into position
        ty =  0.5*self.face_size[1] + 0.5*spacing
        face = Translate(self.face,v=(tx,ty,0))

        # Get maximum support tab depth
        tab_depth_list = []
        for support_data in self.params['supports']:
            for tab_data in support_data['params']['base_tabs']:
                tab_depth_list.append(tab_data[2])
            for tab_data in support_data['params']['face_tabs']:
                tab_depth_list.append(tab_data[2])
        max_tab_depth = max(tab_depth_list)

        # Translate supports into position
        cnt = 0
        support_list = []
        ty = max_tab_depth + 0.5*spacing
        for support, support_data in zip(self.support_list, self.params['supports']):
            if cnt > 0:
                ty -= support_data['params']['height'] + spacing
            tx = max_tab_depth + 0.5*spacing
            support = Translate(support,v=(tx,ty,0))
            support_list.append(support)
            cnt += 1

        # Create reference cube
        ref_cube = Cube(size=(INCH2MM,INCH2MM,INCH2MM))
        y_shift = self.face_size[1] + 0.5*INCH2MM + spacing
        ref_cube = Translate(ref_cube,v=(0,y_shift,0))

        # Collect part into parts list and project to 2D
        parts_list = [base, face] + support_list
        if show_ref_cube == True:
            parts_list.append(ref_cube)
        parts_list = [Projection(part) for part in parts_list]
        return parts_list


class RT_Triangle_W_Tabs(object):
    """
    Creates a right triangle with tabs on the x-z, y-z, and h-z faces of the
    triangle.

    Usage:

    rt = RT_Triangle_W_Tabs(params)

    where

    params = {
        'size'   : (x,y,x),    # Size of right triangle
        'xz'      : xz_tab_data, # tab data for x-z face of right triangle
        'yz'      : yz_tab_data, # tab data for y-z face of right triangle
        'hz'      : hz_tab_data, # tab data for h-z face of right triangle
    }

    and

    (face)_tab_data = [
        (pos_0, width_0, depth_0, tab_dir_0),  # data for 0th tab
        (pos_1, width_1, depth_1, tab_dir_1),  # data for 1st tab
        ...
        ]

    pos_i     =   position of tab i as a fraction of face length
    width_i   =   width of tab i along the face
    depth_i   =   depth of tab i
    tab_dir_i =   depth of the tab.
    """

    def __init__(self,params):
        self.params = params

    def __make_rt_triangle(self):
        x,y,z = self.params['size']
        self.rt_triangle =  right_triangle(x,y,z)

    def __add_tabs(self):

        plate_x, plate_y, plate_z = self.params['size']
        pos_tab_list = []
        neg_tab_list = []

        # Loop over face types
        for face in ('xz', 'yz', 'hz'):
            tab_data = self.params[face]

            for fpos, width, depth, tab_dir in tab_data:
                # Select tabs thickness - removed tabs are thicker
                if tab_dir == '-':
                    thickness = 1.5*plate_z
                elif tab_dir == '+':
                    thickness = plate_z
                else:
                    raise ValueError, "unknown tab direction, {0}, must be '+' or '-'".format(tab_dir)

                if face == 'xz':
                    # Create tabs for the x face of the triangle
                    tab = Cube(size=(width,2*depth,thickness))
                    tab = Translate(tab,v=(fpos*plate_x,0,0))
                elif face == 'yz':
                    # Create tabs for the y face of the triangle
                    tab = Cube(size=(2*depth,width,thickness))
                    tab = Translate(tab,v=(0,fpos*plate_y,0))
                else:
                    # Create tabs for the h face of the triangle
                    tab = Cube(size=(width,2*depth,thickness))
                    h = numpy.sqrt(plate_x**2 + plate_y**2)
                    tab = Translate(tab,v=(-fpos*h,0,0))
                    theta = -RAD2DEG(numpy.arctan2(plate_y, plate_x))
                    tab = Rotate(tab,a=theta,v=(0,0,1))
                    tab = Translate(tab,v=(plate_x,0,0))

                # Add tabs to the appropriate list base on tab direction
                if tab_dir == '+':
                    pos_tab_list.append(tab)
                else:
                    neg_tab_list.append(tab)

        # Add material for positive tabs
        if len(pos_tab_list) > 0:
            self.rt_triangle = Union([self.rt_triangle] + pos_tab_list)

        # Remove material for negative tabs
        if len(neg_tab_list) > 0:
            self.rt_triangle = Difference([self.rt_triangle] + neg_tab_list)

    def make(self):
        self.__make_rt_triangle()
        self.__add_tabs()
        return self.rt_triangle

def rounded_box(length, width, height, radius,
                round_x=True, round_y=True, round_z=True):
    """
    Create a box with rounded corners
    """
    assert round_x or round_y == True, 'x and y faces not rounded - at least two sides must be rounded'
    assert round_x or round_z == True, 'x and z faces not rounded - at least two faces must be rounded'
    assert round_y or round_z == True, 'y and z faces not rounded - at least two faces must be rounded'

    if round_x == True:
        dx = length - 2.0*radius
    else:
        dx = length
    if round_y == True:
        dy = width - 2.0*radius
    else:
        dy = width
    if round_z == True:
        dz = height - 2.0*radius
    else:
        dz = height
    union_list = []

    inner_box = Cube([dx,dy,dz])
    union_list.append(inner_box)

    if round_x==True:
        xface_box = Cube([2*radius,dy,dz])
        xface_box0 = Translate(xface_box,v=[0.5*dx,0,0])
        xface_box1 = Translate(xface_box,v=[-0.5*dx,0,0])
        union_list.extend([xface_box0, xface_box1])

    if round_y==True:
        yface_box = Cube([dx,2*radius,dz])
        yface_box0 = Translate(yface_box,v=[0, 0.5*dy,0])
        yface_box1 = Translate(yface_box,v=[0, -0.5*dy,0])
        union_list.extend([yface_box0, yface_box1])

    if round_z==True:
        zface_box = Cube([dx,dy,2*radius])
        zface_box0 = Translate(zface_box,v=[0, 0, 0.5*dz])
        zface_box1 = Translate(zface_box,v=[0, 0, -0.5*dz])
        union_list.extend([zface_box0, zface_box1])

    xaxis_cly = Cylinder(h=dx,r1=radius,r2=radius)
    xaxis_cly = Rotate(xaxis_cly,a=90,v=[0,1,0])
    yaxis_cly = Cylinder(h=dy,r1=radius,r2=radius)
    yaxis_cly = Rotate(yaxis_cly,a=90,v=[1,0,0])
    zaxis_cly = Cylinder(h=dz,r1=radius,r2=radius)

    for i in [-1,1]:
        for j in [-1,1]:
            if round_y==True and round_z==True:
                temp_cyl = Translate(xaxis_cly,v=[0,i*0.5*dy,j*0.5*dz])
                union_list.append(temp_cyl)
            if round_z==True and round_x==True:
                temp_cyl = Translate(yaxis_cly,v=[i*0.5*dx,0,j*0.5*dz])
                union_list.append(temp_cyl)
            if round_x==True and round_y==True:
                temp_cyl = Translate(zaxis_cly,v=[i*0.5*dx,j*0.5*dy,0])
                union_list.append(temp_cyl)

    if round_x==True and round_y==True and round_z==True:
        corner_sph = Sphere(r=radius)
        for i in [-1,1]:
            for j in [-1,1]:
                for k in [-1,1]:
                    temp_sph = Translate(corner_sph,v=[i*0.5*dx,j*0.5*dy,k*0.5*dz])
                    union_list.append(temp_sph)

    box = Union(union_list)
    return box

def plate_w_holes(length, width, height, holes=[], hole_mod='', radius=False):
    """
    Create a plate with holes in it.

    Arguments:
        length = x dimension of plate
        width  = y dimension of plate
        height = z dimension of plate
        holes  = list of tuples giving x position, y position and diameter of
            holes
    """
    if radius == False:
        plate = Cube(size=[length,width,height])
    else:
        plate = rounded_box(length,width,height,radius,round_z=False)
    cylinders = []
    for x,y,r in holes:
        c = Cylinder(h=4*height,r1=0.5*r, r2=0.5*r)
        c = Translate(c,v=[x,y,0],mod=hole_mod)
        cylinders.append(c)
    obj_list = [plate] + cylinders
    plate = Difference(obj_list)
    return plate

def disk_w_holes(height, d1, holes=[], hole_mod=''):
    """
    Create a disk with holes in it.

    Arguments:
        d1 = diameter of the disk
        height = z dimension of disk
        holes  = list of tuples giving x position, y position and diameter of
            holes
    """

    cyl = Cylinder(h=height,r1=d1*0.5,r2=d1*0.5)
    cylinders = []
    for x,y,r in holes:
        c = Cylinder(h=4*height,r1=0.5*r, r2=0.5*r)
        c = Translate(c,v=[x,y,0],mod=hole_mod)
        cylinders.append(c)
    obj_list = [cyl] + cylinders
    disk = Difference(obj_list)
    return disk

def grid_box(length, width, height, num_length, num_width,top_func=None,bot_func=None):
    """
    Create a box with given length, width, and height. The top and bottom surface of the
    box will be triangulate bases on a grid with num_length and num_width points.
    Optional functions top_func and bot_func can be given to distort the top or bottom
    surfaces of the box.
    """
    nl = num_length + 1
    nw = num_width + 1
    xpts = numpy.linspace(-0.5*length,0.5*length,nl)
    ypts = numpy.linspace(-0.5*width,0.5*width,nw)

    points_top = []
    points_bot = []
    for y in ypts:
        for x in xpts:
            if top_func == None:
                zval_top = 0.0
            else:
                zval_top = top_func(x,y)
            if bot_func == None:
                zval_bot = 0.0
            else:
                zval_bot = bot_func(x,y)
            points_top.append([x,y,0.5*height+zval_top])
            points_bot.append([x,y,-0.5*height+zval_bot])

    faces_top = []
    faces_bot = []
    numtop = len(points_top)
    for i in range(0,nl-1):
        for j in range(0,nw-1):
            # Top triangles
            f = [(j+1)*nl+i, (j+1)*nl+i+1, j*nl+i+1]
            faces_top.append(f)
            f = [(j+1)*nl+i, j*nl+i+1, j*nl+i]
            faces_top.append(f)
            # Botton triangles
            f = [numtop+j*nl+i+1, numtop+(j+1)*nl+i+1, numtop+(j+1)*nl+i]
            faces_bot.append(f)
            f = [numtop+j*nl+i, numtop+j*nl+i+1,  numtop+(j+1)*nl+i]
            faces_bot.append(f)

    faces_front = []
    faces_back = []
    for i in range(0,nl-1):
        # Front triangles
        f = [i+1,numtop+i+1,numtop+i]
        faces_front.append(f)
        f = [i,i+1,numtop+i]
        faces_front.append(f)
        # Back triangles
        f = [2*numtop-nl+i+1,numtop-nl+i+1,numtop-nl+i]
        faces_back.append(f)
        f = [2*numtop-nl+i,2*numtop-nl+i+1,numtop-nl+i]
        faces_back.append(f)

    faces_right = []
    faces_left = []
    for j in range(0,nw-1):
        # Right triangles
        f = [nl-1 +(j+1)*nl,numtop+nl-1+(j+1)*nl,numtop+nl-1+j*nl]
        faces_right.append(f)
        f = [nl-1 + j*nl,nl-1 +(j+1)*nl,numtop+nl-1+j*nl]
        faces_right.append(f)
        # Left triangles
        f = [numtop+(j+1)*nl,(j+1)*nl,j*nl]
        faces_left.append(f)
        f = [numtop+j*nl,numtop+(j+1)*nl,j*nl]
        faces_left.append(f)

    points = points_top + points_bot
    faces = faces_top + faces_bot
    faces.extend(faces_front)
    faces.extend(faces_back)
    faces.extend(faces_right)
    faces.extend(faces_left)

    p = Polyhedron(points=points,faces=faces)
    return p

def wedge_cut(obj,ang0,ang1,r,h,numpts=20,mod=''):
    """
    Cut out a wedge from obj from ang0 to ang1 with given radius r
    and height h.
    """
    ang0rad = DEG2RAD*ang0
    ang1rad = DEG2RAD*ang1
    angs = numpy.linspace(ang0rad,ang1rad,numpts)
    points_arc = [[r*numpy.cos(a),r*numpy.sin(a)] for a in angs]
    points = [[0,0]]
    points.extend(points_arc)
    paths = [range(0,len(points))]
    poly = Polygon(points=points, paths=paths)
    cut = Linear_Extrude(poly,h=h,mod=mod)
    cut_obj = Difference([obj,cut])
    return cut_obj

def partial_cylinder(h,r1,r2,ang0,ang1,cut_extra=1.0,mod=''):
    """
    Create a partial cylinder with given height h, start and end
    radii r1 and r2, from angle ang0 t0 angle ang1.
    """
    cut_ang0 = ang1
    cut_ang1 = ang0 + 360.0
    cyl = Cylinder(h=h,r1=r1,r2=r2)
    cut_r = max([r1,r2]) + cut_extra
    cut_h = h + cut_extra
    cut_cyl = wedge_cut(cyl,cut_ang0,cut_ang1,cut_r,cut_h,mod=mod)
    return cut_cyl

def ellipse_edged_disk(h,r,edge_scale=1.0):
    """
    Create a disk with an ellipse around the edge
    """
    assert edge_scale <= r, 'edge_scale must be <= disk radius'
    edge_len = 0.5*h*edge_scale
    disk = Cylinder(h=h,r1=r-edge_len,r2=r-edge_len)
    c = Circle(r=0.5*h)
    c = Scale(c,v=[edge_scale,1.0,1.0])
    c = Translate(c,v=[r-edge_len,0,0])
    torus = Rotate_Extrude(c)
    disk = Union([disk,torus])
    return disk

def rounded_disk(h,r,edge_r):
    pass



def right_triangle(x,y,z):
    """
    Creates an object which is a right triangle in the x,y plane  and height z.
    The hypotenuse of the triangle is given by sqrt(x**2 + y**2) and the right
    angle of the triangle is located at the origin.
    """
    rect_base = Cube(size=[x,y,z])
    rect_diff = Cube(size=[2*numpy.sqrt(x**2+y**2),y,2*z])
    rect_diff = Translate(rect_diff,v=[0,0.5*y,0])
    theta = -RAD2DEG(numpy.arctan2(y,x))
    rect_diff = Rotate(rect_diff,a=theta,v=[0,0,1])
    triangle = Difference([rect_base,rect_diff])
    triangle = Translate(triangle,v=[0.5*x, 0.5*y, 0])
    return triangle


def right_triangle_w_tabs(x, y, z, num_x=1, num_y=1, tab_depth='z', tab_epsilon=0.0,
        solid=True, removal_frac=0.6):
    """
    Creates a polygonal object which is a right triangle in the x,y plane with
    hypotenuse sqrt(x**2 + y**2). The shape is rectangular in the x,z and y,z
    planes with the z dimension given by z. Tabs are placed along the x and y
    edges of the part.

    Arguments:
    x = x dimension of part
    y = y dimension of part
    z = z dimension of (thickness)

    Keyword Arguments:
    num_x         = number of tabs along the x dimension of the triangle (default=1)
    num_y         = number of tabs along the y dimension of the triangle (default=1)
    tab_depth     = the length the tabs should stick out from the part. If set to
        'z' this will be the z dimension or thickness of the part.
        Otherwise it should be a number. (default = 'z')
    tab_epsilon   = amount the tabs should be over/under sized. 2 times this value
        is added to the tabe width.
    solid         = specifies whether the part should be solid or not.
    removal_frac  = specifies the fraction of the interior to be removed. Only used
        when solid == False

    """
    if tab_depth in ('z','Z'):
        # Sets the depth of the tabs to that of the part z dim (the thickness)
        tab_depth = z

    triangle = right_triangle(x,y,z)
    tabs = []
    tabs = []
    if num_x > 0:
        # Make x-tabs
        tab_x_width = x/(2.0*num_x+1) + 2*tab_epsilon
        tab_x_base = Cube(size=[tab_x_width,2*tab_depth,z])
        tab_x_pos = numpy.linspace(0,x,num_x+2)
        tab_x_pos = tab_x_pos[1:-1]
        for x_pos in tab_x_pos:
            tabs.append(Translate(tab_x_base,v=[x_pos,0,0]))
    if num_y > 0:
        # Make y-tabe
        tab_y_width = y/(2.0*num_y+1) + 2*tab_epsilon
        tab_y_base = Cube(size=[2*tab_depth,tab_y_width,z])
        tab_y_pos = numpy.linspace(0,y,num_y+2)
        tab_y_pos = tab_y_pos[1:-1]
        for y_pos in tab_y_pos:
            tabs.append(Translate(tab_y_base,v=[0,y_pos,0]))

    triangle = Union([triangle]+tabs)

    if solid == False:
        xx,yy = removal_frac*x, removal_frac*y
        sub_triangle = right_triangle(xx,yy,2*z)
        x_shift = (x - xx)/3.0
        y_shift = (y - yy)/3.0
        sub_triangle = Translate(sub_triangle,v=[x_shift,y_shift,0])
        triangle = Difference([triangle,sub_triangle])

    return triangle


def right_angle_bracket(length_base, length_face, width, thickness, num_x_tabs=2, num_y_tabs=2,bracket_frac=0.6):
    """
    Creates a right angle bracket -- not finished yet.
    """
    length_face_adj = length_face - thickness
    base = Cube(size=[length_base, width, thickness])
    face = Cube(size=[length_face_adj, width, thickness])
    face= Rotate(face,a=90,v=[0,1,0])
    x_shift = 0.5*length_base-0.5*thickness
    z_shift = 0.5*length_face_adj+0.5*thickness
    face = Translate(face,v=[x_shift,0,z_shift])

    bracket_x = bracket_frac*(length_base - thickness)
    bracket_y = bracket_frac*length_face_adj
    bracket = right_triangle_w_tabs(bracket_x,bracket_y,thickness,num_x=num_x_tabs,num_y=num_y_tabs)
    bracket = Rotate(bracket,a=90,v=[1,0,0])
    bracket = Rotate(bracket,a=180,v=[0,0,1])
    bracket = Translate(bracket,v=[0,0,0.5*thickness])
    bracket = Translate(bracket,v=[0.5*length_base-thickness,0,0])
    y_shift = 0.5*width-0.5*thickness
    bracket_pos = Translate(bracket,v=[0,y_shift,0])
    bracket_neg = Translate(bracket,v=[0,-y_shift,0])

    #base.mod = '%'
    #face.mod = '%'
    return [base,face,bracket_pos,bracket_neg]
