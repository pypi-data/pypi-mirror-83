import numpy as np 
import matplotlib.pyplot as plt
import matplotlib as mpl

from .probe import TimeProbe, FreqProbe

def _get_eps(structures, mesh):
    """ Compute the permittivity corresponding to a list of `structures` over a 
    given `mesh`. 
    
    Parameters
    ----------
    structures : list of Structure objects
    mesh : tuple of 3 1D arrays, or None
    
    Returns
    -------
    eps : np.ndarray
        Array of size (mesh[0].size, mesh[1].size, mesh[2].size) defining 
        the relative permittivity at each point.
    """

    Nx, Ny, Nz = [mesh[i].size for i in range(3)]

    eps = np.ones((Nx, Ny, Nz))

    # Apply all structures
    for structure in structures:
        mask = structure.inside(mesh)
        mnzero = mask > 0
        eps[mnzero] = (1-mask[mnzero])*eps[mnzero] + \
                                structure.eps * mask[mnzero]
    return eps

def _get_inside(objects, mesh):
    """ Get a mask defining points inside a list of objects.

    Parameters
    ----------
    objects : list of Structure, Source, or Probe objects
    mesh : tuple of 3 1D arrays, or None
    
    Returns
    -------
    mask : np.ndarray
        Array of size (mesh[0].size, mesh[1].size, mesh[2].size) where each 
        element is one if inside any of the objects, and zero otherwise. 
    """

    Nx, Ny, Nz = [mesh[i].size for i in range(3)]

    mask = np.zeros((Nx, Ny, Nz))

    for obj in objects:
        mtmp = obj.inside(mesh)
        mask[mtmp > 0] = 1

    return mask

def _plot_eps(eps_r, clim=None, ax=None, extent=None, cmap='Greys', 
    cbar=False, cax=None):

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    im = ax.imshow(eps_r, cmap=cmap, origin='lower', extent=extent)
    if clim:
        im.set_clim(vmin=clim[0], vmax=clim[1])

    if cbar:
        if cax is not None:
            plt.colorbar(im, ax=ax, cax=cax)
        else:
            plt.colorbar(im, ax=ax)
        
    return im

def relative_eps(sim, x=None, y=None, z=None, clim=None, ax=None, cbar=False, 
        cmap='Greys', sources=True, probes=True, pml=True):
    """ Plot the relative permittivity distribution in a 2D cross-section.
    
    Parameters
    ----------
    sim : Simulation
        Simulation object.
    x : float, optional
        Position for the yz-cross section in which eps is plotted.
    y : float, optional
        Position for the xz-cross section in which eps is plotted.
    z : float, optional
        Position for the xy-cross section in which eps is plotted.
    clim : List or tuple of float, optional
        Matplotlib color limit to use for the plot.
    ax : int, optional
        Matplotlib axis object to use for the plot. If ``None``, a new figure 
        is created. 
    cbar : bool, optional
        Whether or not a colorbar should be added to the plot.
    cmap : bool, optional
        Matplotlib colormap to use for plot.
    sources : bool, optional
        Plot the source positions.
    probes : bool, optional
        Plot the probe positions.
    pml : bool, optional
        Plot the pml regions.
    
    Note
    ----
    Exactly one of ``x``, ``y``, and ``z``, must be supplied.

    Note
    ----
    The plotting is discretized at the center positions of the grid and is for 
    illustrative purposes only. In the FDTD evolution, the Yee grid is used and 
    where the permittivity, source, and probe locations depend on the field 
    polarization.
    """

    grid = sim.grid

    if y is None and z is None and x is not None:
        if x < grid.mesh[0][0] or x > grid.mesh[0][-1]:
            raise ValueError("Cross-section position out of grid bounds.")
        ind = np.nonzero(x < grid.mesh[0])[0][0]
        mesh = (np.array([grid.mesh[0][ind]]), grid.mesh[1], grid.mesh[2])
        mesh_sp = (grid.mesh[0][[ind-1, ind]], grid.mesh[1], grid.mesh[2])
        extent = [grid.mesh_b[1][0], grid.mesh_f[1][-1], 
                    grid.mesh_b[2][0], grid.mesh_f[2][-1]]
        x_lab = "y"
        y_lab = "z"
        ax_tit = "yz-plane at x=%1.2f" % x
        npml = sim.Npml[[1, 2], :]

    elif z is None and x is None and y is not None:
        if y < grid.mesh[1][0] or y > grid.mesh[1][-1]:
            raise ValueError("Cross-section position out of grid bounds.")
        ind = np.nonzero(y < grid.mesh[1])[0][0]
        mesh=(grid.mesh[0], np.array([grid.mesh[1][ind]]), grid.mesh[2])
        mesh_sp = (grid.mesh[0], grid.mesh[1][[ind-1, ind]], grid.mesh[2])
        extent = [grid.mesh_b[0][0], grid.mesh_f[0][-1], 
                    grid.mesh_b[2][0], grid.mesh_f[2][-1]]
        x_lab = "x"
        y_lab = "z"
        ax_tit = "xz-plane at y=%1.2f" % y
        npml = sim.Npml[[0, 2], :]

    elif x is None and y is None and z is not None:
        if z < grid.mesh[2][0] or z > grid.mesh[2][-1]:
            raise ValueError("Cross-section position out of grid bounds.")
        ind = np.nonzero(z < grid.mesh[2])[0][0]
        mesh = (grid.mesh[0], grid.mesh[1], np.array([grid.mesh[2][ind]]))
        mesh_sp = (grid.mesh[0], grid.mesh[1], grid.mesh[2][[ind-1, ind]])
        extent = [grid.mesh_b[0][0], grid.mesh_f[0][-1], 
                    grid.mesh_b[1][0], grid.mesh_f[1][-1]]
        x_lab = "x"
        y_lab = "y"
        ax_tit = "xy-plane at z=%1.2f" % z
        npml = sim.Npml[[0, 1], :]

    else:
        raise ValueError("Exactly one of x, y, or z must be supplied.")

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    eps_r = np.squeeze(_get_eps(sim.structures, mesh=mesh))

    im = _plot_eps(eps_r.T, clim=clim, ax=ax, extent=extent,
                    cbar=cbar, cmap=cmap)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(ax_tit)

    def sp_mask(mask, x, y, z):
        if x is not None:
            return mask[-1, :, :]
        elif y is not None:
            return mask[:, -1, :]
        elif z is not None:
            return mask[:, :, -1]

    if sources==True:
        src_mask = sp_mask(_get_inside(sim.sources, mesh=mesh_sp),
                            x, y, z)
        src_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [78/255, 145/255, 78/255, 0.2]]))
        ax.imshow(src_mask.T, clim=(0, 1), cmap=src_cmap, origin='lower',
                        extent=extent)

    if probes==True:
        prb_mask = sp_mask(_get_inside(sim.tprobes + sim.fprobes, mesh=mesh_sp),
                            x, y, z)
        prb_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [236/255, 203/255, 32/255, 0.3]]))
        ax.imshow(prb_mask.T, clim=(0, 1), cmap=prb_cmap, origin='lower',
                        extent=extent)

    if pml==True:
        pml_mask = np.squeeze(np.zeros((mesh[0].size, mesh[1].size,
                                                mesh[2].size)))
        N1, N2 = pml_mask.shape
        pml_mask[:npml[0, 0], :] = 1
        pml_mask[N1-npml[0, 1]:, :] = 1
        pml_mask[:, :npml[1, 0]] = 1
        pml_mask[:, N2-npml[1, 1]:] = 1
        pml_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [229/255, 127/255, 25/255, 0.2]]))
        ax.imshow(pml_mask.T, clim=(0, 1), cmap=pml_cmap, origin='lower',
                        extent=extent)

    return im

def source_time(sim, source_ind, ax=None):
    """Plot the time dependence of a given source.
    
    Parameters
    ----------
    sim : Simulation
        Simulation object containing the source.
    source_ind : int
        Index of the source in the ``Simulation.sources`` list.    
    """

    if ax is None:
        fig, ax = plt.subplots(1)

    im = plt.plot(sim.grid.tmesh, sim.sources[source_ind].Jt)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude [a. u.]")
    labels = ['Jx', 'Jy', 'Jz']
    ax.legend(labels)

    return im 

def _probe_slice(sim, probe, pind=None, normal=None, normal_ind=0, val='re',
                    comp='z'):

    if normal is None:
        dmin = np.argmin(probe.Pinds_end - probe.Pinds_beg)
        normal = ['x', 'y', 'z'][dmin]

    inds = {'x': 0, 'y': 1, 'z': 2}
    comp_ind = inds[comp]
    ftmp = probe.Pvals[:, :, :, :, pind]

    if isinstance(probe, TimeProbe):
        tit_string = 't='+"%1.2e"%(sim.grid.tmesh[pind]*1e12)+'fs'
    elif isinstance(probe, FreqProbe):
        tit_string = 'f='+"%1.2e"%(probe.freqs[pind]*1e-12)+'THz'

    if val=='int':
        field = ftmp[0, :, :, :]**2 + ftmp[1, :, :, :]**2 + ftmp[2, :, :, :]**2
        ax_tit = "||E||^2"
    else:
        field = ftmp[comp_ind, :, :, :]
        ax_tit = val + "(E" + comp + ")"

    pbeg = probe.Pinds_beg
    pend = probe.Pinds_end

    if normal=='x':
        field = field[normal_ind, :, :]
        norm_pos = sim.grid.mesh[0][pbeg[0]+normal_ind]
        mesh = (np.array([norm_pos]), sim.grid.mesh[1][pbeg[1]:pend[1]],
                    sim.grid.mesh[2][pbeg[2]:pend[2]])
    elif normal=='y':
        field = field[:, normal_ind, :]
        norm_pos = sim.grid.mesh[1][pbeg[1]+normal_ind]
        mesh = (sim.grid.mesh[0][pbeg[0]:pend[0]], np.array([norm_pos]),
                    sim.grid.mesh[2][pbeg[2]:pend[2]])
    elif normal=='z':
        field = field[:, :, normal_ind]
        norm_pos = sim.grid.mesh[2][pbeg[2]+normal_ind]
        mesh = (sim.grid.mesh[0][pbeg[0]:pend[0]],
                    sim.grid.mesh[1][pbeg[1]:pend[1]], np.array([norm_pos]))

    eps_r = np.squeeze(_get_eps(sim.structures, mesh=mesh))

    grid_dict = {
            'x': (1, 2, 0, 'y', 'z'),
            'y': (0, 2, 1, 'x', 'z'),
            'z': (0, 1, 2, 'x', 'y'),
            }

    (d1, d2, dn, x_lab, y_lab) = grid_dict[normal]
    grid1 = sim.grid.mesh[d1][pbeg[d1]:pend[d1]]
    grid2 = sim.grid.mesh[d2][pbeg[d2]:pend[d2]]

    ax_tit += ', ' + tit_string
    ax_title = 'Probe ' + probe.name + ', ' + normal + '=' + \
                '%1.2eum\n'%norm_pos + ax_tit

    return (field, eps_r, norm_pos, grid1, grid2, x_lab, y_lab, ax_title)

def _plot_probe_2D(sim, probe, time_ind, normal, normal_ind,
                    val, comp, ax, cbar, eps, clim):

    (field, eps_r, _, grid1, grid2, x_lab, y_lab, ax_title) = _probe_slice(sim,
                    probe, time_ind, normal, normal_ind, val, comp)

    cmap = "RdBu"
    if val=='re':
        field = np.real(field)
    elif val=='im':
        field = np.imag(field)
    else:
        cmap = "magma"
        field = np.abs(field)

    # Consider using grid.mesh_b and grid.mesh_f as in viz.eps
    extent = [grid1[0], grid1[-1], grid2[0], grid2[-1]]

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    im = ax.imshow(field.T, extent=extent, cmap=cmap, clim=clim, origin='lower')
    if eps==True and (np.amax(eps_r) - np.amin(eps_r) > 1e-10):
        grey = mpl.cm.get_cmap('Greys', 256)
        newgrey = grey(np.linspace(0, 1, 256))
        newgrey[:, 3] = 0.2
        newgrey[0, 3] = 0
        _plot_eps(eps_r.T, clim=None, ax=ax, extent=extent,
                cmap=mpl.colors.ListedColormap(newgrey), cbar=False)

    if cbar==True:
        plt.colorbar(im, ax=ax, shrink=0.8)

    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(ax_title)

    return im

def tprobe_2D(sim, probe_ind, time_ind=-1, normal=None, normal_ind=0, val='re',
                comp='z', ax=None, cbar=False, clim=None, eps=True):
    """Plot a 2D cross-section of the field stored in a TimeProbe object at a 
    given time step.
    
    Parameters
    ----------
    sim : Simulation
        A simulation object.
    probe_ind : int
        Index of the time probe in ``sim``.
    time_ind : int, optional
        Index of the time step in the ``TimeProbe``. Default is the last step.
    normal : None, optional
        Axis normal to the 2D plane of plotting. If ``None``, the shortest 
        dimension is taken as the normal.
    normal_ind : int, optional
        Spatial index along the normal dimension, for 3D probes.
    val : {'re', 'abs', 'int'}, optional
        Plot the real part (default), or the absolute value of a field 
        component, or the total field intensity. 
    comp : {'x', 'y', 'z'}, optional
        Component of the field to plot. If ``val`` is ``'int'``, this parameter 
        is irrelvant.
    ax : Matplotlib axis object, optional
        If None, a new figure is created. 
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps : bool, optional
        If True, also plot a contour of the underlying permittivity.
    
    Returns
    -------
    Matplotlib image object
    """

    probe = sim.tprobes[probe_ind]

    im = _plot_probe_2D(sim, probe, time_ind, normal, normal_ind,
                        val, comp, ax, cbar, eps, clim)

    return im

def fprobe_2D(sim, probe_ind, freq_ind=0, normal=None, normal_ind=0, val='re',
                comp='z', ax=None, cbar=False, clim=None, eps=True):
    """Plot a 2D cross-section of the field stored in a FreqProbe object at a 
    given frequency.
    
    Parameters
    ----------
    sim : Simulation
        A simulation object.
    probe_ind : int
        Index of the frequency probe in ``sim``.
    freq_ind : int, optional
        Index of the frequency in the ``FreqProbe``. Default is 0.
    normal : None, optional
        Axis normal to the 2D plane of plotting. If ``None``, the shortest 
        dimension is taken as the normal.
    normal_ind : int, optional
        Spatial index along the normal dimension, for 3D probes.
    val : {'re', 'im', 'abs', 'int'}, optional
        Plot the real part (default), or the imaginary or absolute value of a 
        field component, or the total field intensity. 
    comp : {'x', 'y', 'z'}, optional
        Component of the field to plot. If ``val`` is ``'int'``, this parameter 
        is irrelvant.
    ax : Matplotlib axis object, optional
        If None, a new figure is created. 
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps : bool, optional
        If True, also plot a contour of the underlying permittivity.
    
    Returns
    -------
    Matplotlib image object
    """

    probe = sim.fprobes[probe_ind]

    im = _plot_probe_2D(sim, probe, freq_ind, normal, normal_ind,
                        val, comp, ax, cbar, eps, clim)

    return im

def export_fprobes(sim, folder_path, val='int', comp='z'):
    """Export png images of 2D cross-sections for all frequency probes in a 
    given simulation. For 3D probes, all 2D slices along the shortest dimension 
    are exported. 

    Parameters
    ----------
    sim : Simulation
        Simulation object with stored probe data after a run.
    folder_path : string
        Path in which the images will be exported.
    """

    fig = plt.figure(constrained_layout=True)

    for (ip, probe) in enumerate(sim.fprobes):
        min_dir = np.argmin(probe.Pvals.shape[1:4])
        normal = ['x', 'y', 'z'][min_dir]

        for normal_ind in range(probe.Pvals.shape[1+min_dir]):
            for (find, _) in enumerate(probe.freqs):
                ax = fig.add_subplot(111)
                fprobe_2D(sim, ip, freq_ind=find, normal=normal,
                            normal_ind=normal_ind, val=val, comp=comp, ax=ax,
                            cbar=True, eps=True)
                fname = probe.name + "_find%d_nind%d.png"%(find, normal_ind)
                plt.savefig(folder_path+fname)
                plt.clf()

    plt.close(fig)
