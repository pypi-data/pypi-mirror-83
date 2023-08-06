import numpy as np

from .utils import listify, inside_box, cs2span
from .constants import int_, float_

class Probe(object):

    def __init__(self, center, size, field, name=None):
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)
        self.field = field
        self.name = None if name is None else str(name)

        # Everything below is set after a run by ``store_Pvals()``.
        self.Pvals = np.empty((0, 3, 0), dtype=float_)
        self.Pinds = np.empty((0, 3), dtype=int_)
        # Indexes defining the span of the Probe in the simulation grid in 
        # which it is embedded. 
        self.Pinds_beg = np.zeros((3, ))
        self.Pinds_end = np.zeros((3, ))

    def inside(self, mesh):
        return inside_box(self.span, mesh, include_zero_size=True)

    def get_Pinds(self, mesh):
        """ Get indexes of the points at which the fields are to be recored.
        
        Parameters
        ----------
        mesh : 3-tuple
            Defines the x, y, and z mesh. 
        
        Returns
        -------
        Pinds : np.ndarray
            An array of shape (Np, 3), where Np is the total number of mesh 
            points in the probe region.
        """
        mask = self.inside(mesh)
        if np.nonzero(mask)[0].size==0: 
            return np.zeros((0, 3), dtype=int_)

        return np.array(np.nonzero(mask), dtype=int_).T

    def store_Pvals(self, Pvals, Pinds):
        """ Store the raw probe values returned by the solver.
        
        Parameters
        ----------
        Pvals : np.ndarray
            An array of shape ``(Np, 3, Nsample)``, where ``Np`` is the total 
            number of probe points, and ``Nsample`` is either the number of 
            time steps in a ``TimeProbe``, or the number of requested 
            frequencies in a ``FreqProbe``.
        Pinds : np.ndarray
            An array of shape ``(Np, 3)`` giving the x, y, and z index for each 
            point in the simulation grid.

        Note
        ----
        ``Probe.Pvals`` is stored in the format ``(3, indx, indy, indz, ind)``, 
        where ``ind`` is either a time or a frequency index.
        """

        self.Pinds = Pinds
        self.Pinds_beg = np.amin(Pinds, axis = 0)
        self.Pinds_end = np.amax(Pinds, axis = 0) + 1
        Pdims = self.Pinds_end - self.Pinds_beg
        self.Pvals = np.zeros((3, Pdims[0], Pdims[1], Pdims[2], 
                        Pvals.shape[2]), dtype=Pvals.dtype)

        # Unscramble everything into the correct format 
        for ipol in range(3):
            self.Pvals[ipol, Pinds[:, 0]-self.Pinds_beg[0],
                    Pinds[:, 1]-self.Pinds_beg[1],
                    Pinds[:, 2]-self.Pinds_beg[2], :] = Pvals[:, ipol, :]

class TimeProbe(Probe):
    """Probe recording a field at all times for all points within a 3D 
    region.
    """

    def __init__(self, center, size, field='E', name=None):
        """ Construct.
        
        Parameters
        ----------
        center : array_like
            Shape (3, ): x, y, and z position of the center of the Probe.
        size : array_like
            Shape (3, ): size in x, y, and z.
        field : {'E'}, optional
            Fields to be recorded.
        name : str, optional
            Custom name of the probe.
        
        Note
        ----
            TODO: Extend to have options for individual components, and H.

            TODO: Add optional starting/stopping time.
        """
        super().__init__(center, size, field)

class FreqProbe(Probe):
    """Probe recording a Fourier transform of a field for all points 
    within a 3D region, and for a given list of frequencies.
    """
    
    def __init__(self, center, size, freqs, field='E', name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            Shape (3, ): x, y, and z position of the center of the Probe.
        size : array_like
            Shape (3, ): size in x, y, and z.
        freqs : float or list of float
            Frequencies at which the fields are sampled.
        field : {'E'}, optional
            Fields to be recorded.
        name : str, optional
            Custom name of the probe.

        Note
        ----
            TODO: Extend to have options for individual components, and H.

            TODO: Add optional starting/stopping time, or better - apodization.
        """

        super().__init__(center, size, field, name)
        self.freqs = listify(freqs)