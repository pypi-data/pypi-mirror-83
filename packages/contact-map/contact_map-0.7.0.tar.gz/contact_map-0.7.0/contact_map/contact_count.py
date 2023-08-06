import collections
import scipy
import numpy as np
import pandas as pd
import warnings
from .plot_utils import ranged_colorbar

# matplotlib is technically optional, but required for plotting
try:
    import matplotlib
    import matplotlib.pyplot as plt
except ImportError:
    HAS_MATPLOTLIB = False
else:
    HAS_MATPLOTLIB = True

# pandas 0.25 not available on py27; can drop this when we drop py27
_PD_VERSION = tuple(int(x) for x in pd.__version__.split('.')[:2])


def _colorbar(with_colorbar, cmap_f, norm, min_val, ax=None):
    if with_colorbar is False:
        return None
    elif with_colorbar is True:
        cbmin = np.floor(min_val)  # [-1.0..0.0] => -1; [0.0..1.0] => 0
        cbmax = 1.0
        cb = ranged_colorbar(cmap_f, norm, cbmin, cbmax, ax=ax)
    # leave open other inputs to be parsed later (like tuples)
    return cb


# TODO: remove following: this is a monkeypatch for a bug in pandas
# see: https://github.com/pandas-dev/pandas/issues/29814
from pandas._libs.sparse import BlockIndex, IntIndex, SparseIndex
def _patch_from_spmatrix(cls, data):  # -no-cov-
    length, ncol = data.shape

    if ncol != 1:
        raise ValueError("'data' must have a single column, not '{}'".format(ncol))

    # our sparse index classes require that the positions be strictly
    # increasing. So we need to sort loc, and arr accordingly.
    arr = data.data
    #idx, _ = data.nonzero()
    idx = data.indices
    loc = np.argsort(idx)
    arr = arr.take(loc)
    idx.sort()

    zero = np.array(0, dtype=arr.dtype).item()
    dtype = pd.SparseDtype(arr.dtype, zero)
    index = IntIndex(length, idx)

    return cls._simple_new(arr, index, dtype)

if _PD_VERSION >= (0, 25):
    pd.core.arrays.SparseArray.from_spmatrix = classmethod(_patch_from_spmatrix)
# TODO: this is the end of what to remove when pandas is fixed

class ContactCount(object):
    """Return object when dealing with contacts (residue or atom).

    This contains all the information about the contacts of a given type.
    This information can be represented several ways. One is as a list of
    contact pairs, each associated with the fraction of time the contact
    occurs. Another is as a matrix, where the rows and columns label the
    pair number, and the value is the fraction of time. This class provides
    several methods to get different representations of this data for
    further analysis.

    In general, instances of this class shouldn't be created by a user using
    ``__init__``; instead, they will be returned by other methods. So users
    will often need to use this object for analysis.

    Parameters
    ----------
    counter : :class:`collections.Counter`
        the counter describing the count of how often the contact occurred;
        key is a frozenset of a pair of numbers (identifying the
        atoms/residues); value is the raw count of the number of times it
        occurred
    object_f : callable
        method to obtain the object associated with the number used in
        ``counter``; typically :meth:`mdtraj.Topology.residue` or
        :meth:`mdtraj.Topology.atom`.
    n_x : int
        number of objects in the x direction (used in plotting)
    n_y : int
        number of objects in the y direction (used in plotting)
    """
    def __init__(self, counter, object_f, n_x, n_y):
        self._counter = counter
        self._object_f = object_f
        self.n_x = n_x
        self.n_y = n_y

    @property
    def counter(self):
        """
        :class:`collections.Counter` :
            keys use index number; count is contact occurrences
        """
        return self._counter

    @property
    def sparse_matrix(self):
        """
        :class:`scipy.sparse.dok.dok_matrix` :
            sparse matrix representation of contacts

            Rows/columns correspond to indices and the values correspond to
            the count
        """
        mtx = scipy.sparse.dok_matrix((self.n_x, self.n_y))
        for (k, v) in self._counter.items():
            key = list(k)
            mtx[key[0], key[1]] = v
            mtx[key[1], key[0]] = v
        return mtx

    @property
    def df(self):
        """
        :class:`pandas.SparseDataFrame` :
            DataFrame representation of the contact matrix

            Rows/columns correspond to indices and the values correspond to
            the count
        """
        mtx = self.sparse_matrix
        index = list(range(self.n_x))
        columns = list(range(self.n_y))

        if _PD_VERSION < (0, 25):  # py27 only  -no-cov-
            mtx = mtx.tocoo()
            return pd.SparseDataFrame(mtx, index=index, columns=columns)

        df = pd.DataFrame.sparse.from_spmatrix(mtx, index=index,
                                               columns=columns)
        # note: I think we can always use float here for dtype; but in
        # principle maybe we need to inspect and get the internal type?
        # Problem is, pandas technically stores a different dtype for each
        # column.
        df = df.astype(pd.SparseDtype("float", np.nan))
        return df

    def _check_number_of_pixels(self, figure):
        """
        This checks to see if the number of pixels in the figure is high enough
        to accuratly represent the the contact map. It raises a RuntimeWarning
        if this is not the case.

        Parameters
        ----------
        figure: :class:`matplotlib.Figure`
            matplotlib figure to compare the amount of pixels from

        """
        # Get dpi, and total pixelswidht and pixelheight
        dpi = figure.get_dpi()
        figwidth = figure.get_figwidth()
        figheight = figure.get_figheight()
        xpixels = dpi*figwidth
        ypixels = dpi*figheight

        # Check if every value has a pixel
        if xpixels/self.n_x < 1 or ypixels/self.n_y < 1:
            msg = ("The number of pixels in the figure is insufficient to show"
                   " all the contacts.\n Please save this as a vector image "
                   "(such as a PDF) to view the correct result.\n Another "
                   "option is to increase the 'dpi' (currently: "+str(dpi)+"),"
                   " or the 'figsize' (currently: " + str((figwidth,
                                                           figheight)) +
                   ").\n Recommended minimum amount of pixels = "
                   + str((self.n_x, self.n_y))+" (width, height).")
            warnings.warn(msg, RuntimeWarning)

    def plot(self, cmap='seismic', vmin=-1.0, vmax=1.0, with_colorbar=True,
             **kwargs):
        """
        Plot contact matrix (requires matplotlib)

        Parameters
        ----------
        cmap : str
            color map name, default 'seismic'
        vmin : float
            minimum value for color map interpolation; default -1.0
        vmax : float
            maximum value for color map interpolation; default 1.0
        **kwargs
            All additional keyword arguments to be passed to the
            :func:`matplotlib.pyplot.subplots` call
        Returns
        -------
        fig : :class:`matplotlib.Figure`
            matplotlib figure object for this plot
        ax : :class:`matplotlib.Axes`
            matplotlib axes object for this plot
        """
        if not HAS_MATPLOTLIB:  # pragma: no cover
            raise RuntimeError("Error importing matplotlib")
        fig, ax = plt.subplots(**kwargs)

        # Check the number of pixels of the figure
        self._check_number_of_pixels(fig)
        self.plot_axes(ax=ax, cmap=cmap, vmin=vmin, vmax=vmax)

        return (fig, ax)

    def plot_axes(self, ax, cmap='seismic', vmin=-1.0, vmax=1.0,
                  with_colorbar=True):
        """
        Plot contact matrix on a matplotlib.axes

        Parameters
        ----------
        ax : matplotlib.axes
           axes to plot the contact matrix on
        cmap : str
            color map name, default 'seismic'
        vmin : float
            minimum value for color map interpolation; default -1.0
        vmax : float
            maximum value for color map interpolation; default 1.0
        with_colorbar : bool
            If a colorbar is added to the axes
        """

        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
        cmap_f = plt.get_cmap(cmap)
        ax.axis([0, self.n_x, 0, self.n_y])
        ax.set_facecolor(cmap_f(norm(0.0)))

        min_val = 0.0
        for (pair, value) in self.counter.items():
            if value < min_val:
                min_val = value
            pair_list = list(pair)
            patch_0 = matplotlib.patches.Rectangle(
                pair_list, 1, 1,
                facecolor=cmap_f(norm(value)),
                linewidth=0
            )
            patch_1 = matplotlib.patches.Rectangle(
                (pair_list[1], pair_list[0]), 1, 1,
                facecolor=cmap_f(norm(value)),
                linewidth=0
            )
            ax.add_patch(patch_0)
            ax.add_patch(patch_1)

        _colorbar(with_colorbar, cmap_f, norm, min_val, ax=ax)

    def most_common(self, obj=None):
        """
        Most common values (ordered) with object as keys.

        This uses the objects for the contact pair (typically MDTraj
        ``Atom`` or ``Residue`` objects), instead of numeric indices. This
        is more readable and can be easily used for further manipulation.

        Parameters
        ----------
        obj : MDTraj Atom or Residue
            if given, the return value only has entries including this
            object (allowing one to, for example, get the most common
            contacts with a specific residue)

        Returns
        -------
        list :
            the most common contacts in order. If the list is ``l``, then
            each element ``l[e]`` is a tuple with two parts: ``l[e][0]`` is
            the key, which is a pair of Atom or Residue objects, and
            ``l[e][1]`` is the count of how often that contact occurred.

        See also
        --------
        most_common_idx : same thing, using index numbers as key
        """
        if obj is None:
            result = [
                ([self._object_f(idx) for idx in common[0]], common[1])
                for common in self.most_common_idx()
            ]
        else:
            obj_idx = obj.index
            result = [
                ([self._object_f(idx) for idx in common[0]], common[1])
                for common in self.most_common_idx()
                if obj_idx in common[0]
            ]
        return result

    def most_common_idx(self):
        """
        Most common values (ordered) with indices as keys.

        Returns
        -------
        list :
            the most common contacts in order. The if the list is ``l``,
            then each element ``l[e]`` consists of two parts: ``l[e][0]`` is
            a pair of integers, representing the indices of the objects
            associated with the contact, and ``l[e][1]`` is the count of how
            often that contact occurred

        See also
        --------
        most_common : same thing, using objects as key
        """
        return self._counter.most_common()

    def filter(self, idx):
        """New ContactCount filtered to idx.

        Returns a new ContactCount with the only the counter keys/values
        where both the keys are in idx
        """
        dct = {k: v for k, v in self._counter.items()
               if all([i in idx for i in k])}
        new_count = collections.Counter()
        new_count.update(dct)
        return ContactCount(new_count, self._object_f, self.n_x, self.n_y)
