netcdf_dataset
==============

Provides a helper class `NetcdfDataset` that serves as a wrapper around 
a `netCDF4.Dataset` instance. All it does is parse all the attributes, 
dimensions, groups and variables in `netCDF4.Dataset`, and populates
a Python class instance with their values. It is most useful for exploring
NetCDF datasets in interactive Python sessions, but may be also used 
in general Python programs to reduce verbosity of the code when parsing 
`netCDF4.Dataset` instances.

Usage
-----

```python
>>> from netcdf_dataset import NetcdfDataset
>>> nc = NetcdfDataset("samplefile.nc")
```

Dependencies
------------
netCDF4
    A third-party library that provides a Python interface to UCAR's
    NetCDF file format. Get from  http://pypi.python.org/pypi/netCDF4.
datetime
    Date and time manipulation library. Part of Python's standard 
    library.
