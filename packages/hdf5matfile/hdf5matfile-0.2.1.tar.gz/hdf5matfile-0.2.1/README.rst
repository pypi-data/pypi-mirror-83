hdf5matfile
===========

Load data from v7.3 \*.mat files. Only reading is supported, no writing.


Usage
-----

Provides a class ``Hdf5Matfile`` and a convience function ``load_hdf5mat``.

To load all the variables from the file, use ``Hdf5Matfile.load_file``:

.. code:: python

    with Hdf5Matfile(filename) as file:
        data = file.load_file()

To load a specific variable, use ``Hdf5Matfile.load_variable``:

.. code:: python

    with Hdf5Matfile(filename) as file:
        results = file.load_variable('results')

If you're not using a context manager, make sure to close the file after
you're done:

.. code:: python

    file = Hdf5Matfile(filename)
    data = file.load_file()
    file.close()

By default, arrays are not squeezed; since MATLAB represents even scalars
as 2-D arrays, this means that something you expect to be a scalar will in
fact be a 1-by-1 np.ndarray. You can change this by passing ``squeeze=True``
to the constructor:

.. code:: python

    with Hdf5Matfile(filename, squeeze=True) as file:
        data = file.load_file()


Supported data types
--------------------

Data type support is pretty limited; this isn't a terribly fancy class.
Supported MATLAB data types, and the Python objects or NumPy dtypes they map
to:

===============  =============  =============
  MATLAB type    Python object   NumPy dtype
===============  =============  =============
cell             np.ndarray     object
char             str            n/a
double           np.ndarray     np.double
int8             np.ndarray     np.byte
int16            np.ndarray     np.short
int32            np.ndarray     np.intc
int64            np.ndarray     np.int\_
logical          np.ndarray     bool8
single           np.ndarray     single
struct (scalar)  dict           n/a
struct (array)   np.ndarray     object (dict)
uint8            np.ndarray     np.ubyte
uint16           np.ndarray     np.ushort
uint32           np.ndarray     np.uintc
uint64           np.ndarray     np.uint
===============  =============  =============
