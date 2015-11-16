import math

class Quat(object):

    def __init__(self,w,x,y,z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self,other):
        try:
            w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
            x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
            y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
            z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        except AttributeError:
            w = self.w*other
            x = self.x*other
            y = self.y*other
            z = self.z*other
        return Quat(w,x,y,z)

    def __rmul__(self,other):
        w = self.w*other
        x = self.x*other
        y = self.y*other
        z = self.z*other
        return Quat(w,x,y,z)

    def __str__(self):
        return '({0}, {1}, {2}, {3})'.format(self.w, self.x, self.y, self.z)

    def conj(self):
        return Quat(self.w,-self.x,-self.y,-self.z)

    def mag(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def inv(self):
        return self.conj()*(1.0/self.mag())

def quatFromAxisAngle(ax,ang):
    w = math.cos(0.5*ang)
    x = ax[0]*math.sin(0.5*ang)
    y = ax[1]*math.sin(0.5*ang)
    z = ax[2]*math.sin(0.5*ang)
    return Quat(w,x,y,z)

# -------------------------------------------------------------------------------------
if __name__ == '__main__':

    q = quatFromAxisAngle((1,0,0),math.radians(45.0))
    print q


