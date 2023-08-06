import numpy as np

from .utils import inside_box, cs2span
from .constants import fp_eps, int_, float_

class Structure(object):
    
    def __init__(self, eps=1., sigma=0., name=None):
        """Base class for structures 
        
        Parameters
        ----------
        eps : float, optional
            Relative permittivity inside the structure.
        sigma : float, optional
            Electric conductivity inside the structure, s.t. 
            Im(epsilon(omega)) = sigma/omega.
        """

        self.eps = np.array(eps, dtype=float_)
        self.sigma = np.array(sigma, dtype=float_)
        self.name = None if name is None else str(name)

    def inside(self, mesh, include_edges=True):
        """Elementwise indicator function for the structure.
        
        Parameters
        ----------
        mesh : tuple
            3-tuple defining the xgrid, ygrid and zgrid.
        include_edges : bool
            Whether a point sitting exactly on a mesh point (within numerical 
            precision) should be returned as inside (True) or outside (False) 
            the structure.
        
        Note
        ----
        ``include_edges`` will in the future be replaced by actual dielectric 
        smoothening.
        
        Returns
        -------
        mask : np.ndarray
            A 3D array of shape (mesh[0].size, mesh[1].size, mesh[2].size)
            that is 1 inside the structure and 0 outside, and a continuous 
            value between 0 and 1 at interfaces if smoothen==True.
        """

        raise NotImplementedError("inside() needs to be implemented by "
            "Structure subclasses")

class Box(Structure):
    """ Box structure, i.e. a 3D rectangular block.
    """

    def __init__(self, center, size, eps=1., sigma=0.):
        """ Construct.

        Parameters
        ----------
        center : array_like
            Shape (3, ): x, y, and z position of the center of the Box.
        size : array_like
            Shape (3, ): size in x, y, and z.
        eps : float, optional
            Relative permittivity.
        sigma : float, optional
            Electric conductivity.
        """
        super().__init__(eps, sigma)
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)

    def inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Box region."""

        tmp_span = np.copy(self.span)
        if include_edges==True:
            tmp_span[:, 0] -= (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps
            tmp_span[:, 1] += (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps
        else:
            tmp_span[:, 0] += (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps
            tmp_span[:, 1] -= (tmp_span[:, 1] - tmp_span[:, 0])*fp_eps

        return inside_box(tmp_span, mesh, include_zero_size=False)

class Sphere(Structure):
    """ Sphere structre.
    """
    def __init__(self, position, radius, eps=1., sigma=0.):
        """ Construct.

        Parameters
        ----------
        position : array_like
            Shape (3,): x, y, z position of the center of the sphere.
        radius : float
            Radius of the sphere.
        eps : float, optional
            Relative permittivity.
        sigma : float, optional
            Electric conductivity.
        """
        super().__init__(eps, sigma)
        self.position = np.array(position, dtype=float_)
        self.radius = radius

    def inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Sphere."""

        x, y, z = self.position
        r = self.radius * (1 + (include_edges - 0.5) * 2 * fp_eps)

        return np.where((x - mesh[0][:, np.newaxis, np.newaxis])**2 + 
                    (y - mesh[1][np.newaxis, :, np.newaxis])**2 + 
                    (z - mesh[2][np.newaxis, np.newaxis, :])**2 < r**2, 1, 0)
