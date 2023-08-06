import numpy as np
import json

from .utils import listify, cs2span
from .structure import Structure
from .source import Source, PlaneSource
from .probe import Probe, TimeProbe, FreqProbe
from .grid import Grid
from .json_ops import write_parameters, write_structures, write_run_parameters, write_sources, write_probes

class Simulation(object):
    """
    Main class for building a simulation model.
    """

    def __init__(self, center=np.array([0., 0., 0.]),
                    size=np.array([1., 1., 1.]),
                    resolution=0.1, structures=[], sources=[], probes=[],
                    run_time=1e-12,
                    Npml=np.array([[0, 0], [0, 0], [0, 0]])):
        """Parameters
        ----------
        center : list or np.ndarray, optional
            3D vector defining the center of the simulation domain.
        size : list or np.ndarray, optional
            3D vector defining the size of the simulation domain.
        resolution :  float or list or np.ndarray of float, optional
            Resolution in all directions, or a 3D vector defining it separately 
            in x, y, and z. 
        structures : Structure or a list of Structure objects, optional
            Empty list (default) means vacuum. 
        sources : Source or a list of Source objects, optional
            Source(s) to be added to the simulation.
        probes : Probe or a list of Probe objects, optional
            Probe(s) to be added to the simulation.
        Npml : list or np.ndarray of int
            Shape (3, 2) array defining the thickness in grid points of the PML 
            in (xmin, xmax), (ymin, ymax), and (zmin, zmax).

        Note
        ----
        Sources and Probes can also be added after initialization using 
        `Simulation.add()`.
        """

        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)
        self.grid = Grid(self.span, resolution)
        self._structures, self._sources = [], []

        # Set run time 
        self.T = run_time
        self.grid.set_tmesh(self.T)
        self.Nt = np.int(self.grid.tmesh.size)
        
        self.add(sources)

        # Time and frequency domain probes
        self._tprobes, self._fprobes = [], []
        self.add(structures)
        self.add(probes)

        # Set PML size and compute parameters
        self.Npml = np.array(Npml)

        # JSON file from which the simulation is loaded
        self.fjson = None

    @property
    def structures(self):
        """ List conaining all Structure objects. """
        return self._structures

    @structures.setter
    def structures(self, new_struct):
        # Make a list if a single object was given.
        self.add(new_struct)

    @property
    def sources(self):
        """ List conaining all Source objects. """
        return self._sources

    @sources.setter
    def sources(self, new_sources):
        # Make a list if a single object was given.
        self.add(new_sources)

    @property
    def tprobes(self):
        """ List conaining all TimeProbe objects. """
        return self._tprobes

    @tprobes.setter
    def tprobes(self, new_probes):
        # Make a list if a single object was given.
        self.add(new_probes)

    @property
    def fprobes(self):
        """ List conaining all FreqProbe objects. """
        return self._fprobes

    @fprobes.setter
    def fprobes(self, new_probes):
        # Make a list if a single object was given.
        self.add(new_probes)

    def _add_structure(self, structure):
        """ Adds a Structure object to the list of structures and to the 
        permittivity array. """
        self._structures.append(structure)
        if structure.name is None:
            structure.name = 'obj' + str(len(self.structures))

    def _add_source(self, source):
        """ Adds a Source object to the list of sources.
        """
        source._get_Jt(self.grid.tmesh)
        if isinstance(source, PlaneSource):
            # Make the size spanning the whole simulation if no size provided
            source._sim_span(self.span)
        self._sources.append(source)
        if source.name is None:
            source.name = 'source' + str(len(self.sources))

    def _add_probe(self, probe):
        """ Adds a time or frequency domain Probe object to the 
        corresponding list of probes.
        """
        if isinstance(probe, TimeProbe):
            self._tprobes.append(probe)
            if probe.name is None:
                probe.name = 'tprobe' + str(len(self.tprobes))
        elif isinstance(probe, FreqProbe):
            self._fprobes.append(probe)
            if probe.name is None:
                probe.name = 'fprobe' + str(len(self.fprobes))

    def _pml_config(self):
        """Set the CPML parameters. Default configuration is hard-coded. This 
        could eventually be exposed to the user, or, better, named PML profiles 
        can be created.
        """
        cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
                    'korder': 3, 'kmin': 1., 'kmax': 3., 
                    'aorder': 1, 'amin': 0., 'amax': 0}
        return cfs_config

    def add(self, objects):
        """
        Add a list of objects. Can contain structures, sources, and/or probes.
        """

        for obj in listify(objects):
            if isinstance(obj, Structure):
                self._add_structure(obj)
            elif isinstance(obj, Source):
                self._add_source(obj)
            elif isinstance(obj, Probe):
                self._add_probe(obj)

    def store_P(self, P, new_ax, probe=None):
        """ Store the probe data in a list `P` corresponding to the list of 
        probes in `self.tprobes` or `self.fprobes`. The field for each probe is 
        stored in the format `[pol, indx, indy, indz, inds]`, where `inds` is 
        either the time or the frequency index. The axes used in the solver 
        defined by `new_ax` are rotated back to original order.

        TODO: hdf5
        """
        if probe=='time':
            for (iprobe, probe) in enumerate(self.tprobes):
                probe.store_P(P[iprobe], new_ax)
        elif probe=='freq':
            for (iprobe, probe) in enumerate(self.fprobes):
                probe.store_P(P[iprobe], new_ax)
        else: raise ValueError()

    def init_run(self, fdtd_path='', platform='cpu',  mpi=1,
                    print_warnings=True,
                    hostfile='', export_png=False, export_data=False,
                    print_progress=False, smoothen=False, python_cmd="python"):
        """Initialize everything needed for the simulation run.
        
        Parameters
        ----------
        T : float
            Total time of the simulation in fs.
        fdtd_path : str
            Path to the `fdtd3d` repository.
        platform : {'cpu', 'gpu'}
            Solver hardware to use.
        mpi : int
            Number of MPI processes to use. Default is 1.
        export_png : bool, optional
            If True, a cross-section png image (or a set of those if a volume 
            probe) of the E-field intensity of every frequency probe will be 
            stored in the solver tmp folder.
        """
        if print_warnings==True:
            if self.sources==[]:
                print("Warning: add at least one source. All fields stay zero "
                    "otherwise.")

            if self.tprobes==[] and self.fprobes==[]:
                print("Warning: no probes in the simulation, nothing from the "
                    "simulation run will be stored.")

        self.export_png = export_png
        self.export_data = export_data
        self.print_progress = print_progress
        self.smoothen = smoothen

        self.platform = platform
        self.fdtd_path = fdtd_path
        self.mpi = mpi
        self.hostfile = hostfile
        self.python_cmd = python_cmd

    def export_json(self, fjson):
        """Export the simulation to a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """
        
        self.fjson = fjson
        js = {}
        js["parameters"] = write_parameters(self)
        js["run_parameters"] = write_run_parameters(self)
        js["objects"] = write_structures(self.structures)
        js["sources"] = write_sources(self.sources)
        js["probes"] = write_probes(self.tprobes)
        js["probes"] += write_probes(self.fprobes)

        with open(fjson, 'w') as json_file:
            json.dump(js, json_file, indent=4)