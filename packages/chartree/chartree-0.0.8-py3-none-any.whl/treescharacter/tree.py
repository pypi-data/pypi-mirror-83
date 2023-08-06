"""
Grow a tree in an Ecosystem object.
"""

import numpy as np
from IPython.display import clear_output
from math import pi
from time import sleep

def vec_from_angle(from_vec, angle):
    from_vec = np.copy(from_vec)
    arc = np.arctan(from_vec[1]/from_vec[0])*180/pi
    if from_vec[0]<0:
        big = 180+arc+angle
    elif from_vec[1]<0:
        big = 360+arc+angle
    else:
        big = arc+angle
    big = pi*big/180
    return np.array([np.cos(big), np.sin(big)])

class Branch:
    def __init__(self, center, width, direction):
        self.center = np.array(center)
        self.width = width
        self.direction = np.array(direction)/np.linalg.norm(np.array(direction))
        self.thresh = .5

class Ecosystem:
    """
    A must for most trees. Set up your Ecosystem and then use grow() and show() methods to create your tree.
    
    Parameters
    ------------
    size : array_like
        The shape of the character grid, equalized to account for characters being taller than they are wide. Default is [50,40].
    material : char
        The character used to fill the tree. Must be a single character. Default is '$'
    background : char
        The character used to fill the background of the Ecosystem. Default is '`'.
        
    Returns
    ------------
    Ecosystem object, with grow() and show() methods.
    """

    def __init__(self, size=[50,40], material='$', background='`'):
        self.w = int(size[0]*2)
        self.h = int(size[1])
        self.mat = material
        self.bg = background
        self.plot = 'Nothing has grown!'
        
    def make_wood(self, coor):
        coor = np.copy(coor)
        coor[0] = coor[0]*2
        coor = np.round(coor).astype(int)
        if(coor[1]>=0 and coor[1]<self.h and coor[0]>=0 and coor[0]<self.w):
            self.plot[coor[1], coor[0]] = 1

    def show(self, material='', background=''):
        """
        Shows the grown tree. Can be used to experiment with characters without changing the shape of the tree. 
        
        Parameters:
        -------------
        material : char
            Optional. Changes the Ecosystem material.
        background : char
            Optional. Changes the Ecosystem background.

        Returns:
        ------------
        Nothing. Simply prints tree.
        """

        if material: self.mat = material
        if background: self.bg = background
        if isinstance(self.plot, str):
            print(self.plot)
        else:
            whole = ''
            for row in self.plot:
                line = ''
                for let in row:
                    if let==1:
                        line += self.mat
                    else:
                        line += self.bg
                whole += (line+'\n')
            clear_output(wait=True)
            print(whole)
            
    def grow(self, trunk=3, n_iter=40, density=9, ang_mean=35, ang_range=5, watch=True, speed=.04):
        """
        Grows a tree, starting at the bottom center of the grid.
        
        Parameters:
        -------------
        trunk : int
            The starting radius of the trunk. Default is 3.
        n_iter : int
            The number of growth iterations. Default is 40.
        density : int
            The rate at which new branches form. Lower numbers are denser. Default is 9, which means new branches form every 9 growth iterations.
        ang_mean : int
            The mean angle of branch splits. Default is 35.
        ang_range : int
            The range, above and below ang_mean, of angle possibilities. A higher range means a more unpredictable tree. Default is 5.
        watch : bool
            Whether or not to watch the tree as it grows. Default True.
        speed : float
            Speed at which the tree grows (only applies if watch=True). Default is .04, which means each growth iteration takes .04 seconds.
            
        Returns:
        ------------
        Nothing. View the grown tree with show().
        """

        self.plot = np.full(shape=(self.h, self.w), fill_value=0)
        branches = [Branch(center=[self.w/4, self.h], width=trunk, direction=[.001,-7])]
        
        for i in range(n_iter):
            hard_length = len(branches)
            for br in branches:
                if branches.index(br) == hard_length:
                    break
                for r in np.arange(0, br.width/2, .1):
                    ring = np.array([1.,1.])
                    ring -= ring.dot(br.direction) * br.direction
                    ring /= np.linalg.norm(ring)
                    ring *= r

                    self.make_wood(br.center + ring)
                    self.make_wood(br.center - ring)

                if i%density == 0:
                    ang = np.random.randint(ang_mean-ang_range, ang_mean+ang_range)\
                                            * (1 if np.random.random() > br.thresh else -1)
                    if ang<0:
                        br.thresh -= .5
                    else:
                        br.thresh += .5

                    if i>.5*n_iter and br.width > .4:
                        branches.append(Branch(center=br.center,
                                               width=((br.width**2)*.5)**(1/2),
                                               direction=vec_from_angle(br.direction,.5*ang)))
                        br.direction = vec_from_angle(br.direction, -.5*ang)
                        br.width = ((br.width**2)*.5)**(1/2)
                    else:
                        branches.append(Branch(center=br.center, 
                                               width=((br.width**2)*.2)**(1/2),
                                               direction=vec_from_angle(br.direction,ang)))
                        br.direction = vec_from_angle(br.direction, -.15*ang)
                        br.width = ((br.width**2)*.8)**(1/2)
                br.center = br.center + br.direction
                br.width *= .97
            if watch:
                sleep(speed)
                self.show()

    def __repr__(self):
        return "Ecosystem of size {}x{}, material='{}', background='{}'".format(int(self.w/2), self.h, self.mat, self.bg)
