import numpy as np

from .structure import Structure
from .constants import fp_eps, int_, float_, C_0

class Grid(object):
    
    def __init__(self, span, res, init_mesh=True):
        """
        Parameters
        ----------
        span : np.ndarray of shape (3, 2)
            Defines (xmin, xmax), (ymin, ymax), (zmin, zmax) of the simulation
            region, in micron.
        res : float or array of floats
            Resolution in x, y, and z, in micron.        
        """

        # Setting span also sets self.mesh, self.mesh_b, self.mesh_f
        self.span = np.array(span).astype(float_)
        self.res = np.array(res).astype(float_)

        self.tmesh = None # To be set when a total simulation time is given
        self.set_time_step()

        """ Variables and meshes initialized by `init_meshes()` """
        if init_mesh==True:
            self.init_meshes()
        else:
            empty_mesh = (np.array([]), np.array([]), np.array([]))
            # Grid size
            self.Nx, self.Ny, self.Nz, self.Nxyz = 0, 0, 0, (0, 0, 0)
            # Backward, centered, and forward meshes
            self.mesh_b, self.mesh, self.mesh_f = [empty_mesh for i in range(3)]
            # Ex, Ey, and Ez meshes
            self.mesh_x, self.mesh_y, self.mesh_z = \
                                            [empty_mesh for i in range(3)]


    @property
    def res(self):
        """ Returns the (dx, dy, dz) resolution of the grid """
        return self._res

    @res.setter
    def res(self, new_res):
        restmp = np.array(new_res)
        if restmp.size==1:
            self._res = restmp*np.ones((3, ), dtype=float_)
        elif restmp.size==3:
            self._res = restmp
        else:
            raise ValueError("resolution must be a float or an array of 3 "
                                "floats.")

    def init_meshes(self):
        """ Initialize centered, forward, and backward mesh based on span and 
        res. Also initialize `mesh_x`, `mesh_y`, and `mesh_z` corresponding to 
        the E-field locations on the Yee grid.
        """

        # Increase span by floating point epsilon (relatively to resolution) to 
        # assure pixels at the edges are included
        _span = self.span
        _span[:, 0] -= self.res*fp_eps
        _span[:, 1] += self.res*fp_eps

        # Initialize mesh points in x, y and z 
        self.Nx = int_((_span[0][1]-_span[0][0])/self.res[0])
        self.Ny = int_((_span[1][1]-_span[1][0])/self.res[1])
        self.Nz = int_((_span[2][1]-_span[2][0])/self.res[2])
        self.Nxyz = (self.Nx, self.Ny, self.Nz)
        xcent = (_span[0][1] + _span[0][0])/2
        ycent = (_span[1][1] + _span[1][0])/2
        zcent = (_span[2][1] + _span[2][0])/2

        # Make xcent, ycent, zcent always lie at a Yee cell border
        xgrid = xcent + self.res[0]*np.arange(-((self.Nx+1)//2), (self.Nx)//2)
        ygrid = ycent + self.res[1]*np.arange(-((self.Ny+1)//2), (self.Ny)//2)
        zgrid = zcent + self.res[2]*np.arange(-((self.Nz+1)//2), (self.Nz)//2)

        xgrid = xgrid.astype(float_)
        ygrid = ygrid.astype(float_)
        zgrid = zgrid.astype(float_) 

        # Coordinates of the starting points of the mesh elements
        self.mesh_b = (xgrid, ygrid, zgrid)

        # Coordinates of the mesh centers 
        self.mesh = (xgrid + self.res[0]/2,
                     ygrid + self.res[1]/2,
                     zgrid + self.res[2]/2)        

        # Coordinates of the ending points of the mesh elements
        self.mesh_f = (xgrid + self.res[0],
                     ygrid + self.res[1],
                     zgrid + self.res[2])

        self.yee_meshes()

    def yee_meshes(self):
        # Meshes for the Ex, Ey, and Ez locations.
        self.mesh_x = (self.mesh[0], self.mesh_b[1], self.mesh_b[2])
        self.mesh_y = (self.mesh_b[0], self.mesh[1], self.mesh_b[2])
        self.mesh_z = (self.mesh_b[0], self.mesh_b[1], self.mesh[2])

    def set_time_step(self, stability_factor=0.9):
        """ Set the time step based on the generalized Courant stability
                Delta T < 1 / C_0 / sqrt(1 / dx^2 + 1/dy^2 + 1/dz^2)
                dt = courant_condition * stability_factor, so stability factor 
                should be < 1.
        """

        dL_sum = np.sum([1/self.res[ir]**2 for ir in range(3)])
        dL_avg = 1 / np.sqrt(dL_sum)
        courant_stability = dL_avg / C_0
        self.dt = float_(courant_stability * stability_factor)

    def set_tmesh(self, T=0):
        """ Set the time mesh for a total simulation time T in seconds.
        """
        self.tmesh = np.arange(0, T, self.dt)