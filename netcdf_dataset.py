# Copyright (c) 2014, Milan Curcic
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
# 
# * Neither the name of the {organization} nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
netcdf_dataset
==============

Provides a helper class NetcdfDataset that serves as a wrapper around 
a netCDF4.Dataset instance. All it does is parse all the attributes, 
dimensions, groups and variables in netCDF4.Dataset, and populates
a Python class instance with their values. It is most useful for exploring
NetCDF datasets in interactive Python sessions, but may be also used 
in general Python programs to reduce verbosity of the code when parsing 
netCDF4.Dataset instances.

Usage
-----

>>> from netcdf_dataset import NetcdfDataset
>>> nc = NetcdfDataset("samplefile.nc")

Dependencies
------------
netCDF4
    A third-party library that provides a Python interface to UCAR's
    NetCDF file format. Get from  http://pypi.python.org/pypi/netCDF4.
datetime
    Date and time manipulation library. Part of Python's standard 
    library.
"""

__version__ = "0.1.0"
__all__ = ["NetcdfDataset"]


from netCDF4 import Dataset
from datetime import datetime


class Container():
    """
    An empty class. Provides some basic methods to inspect 
    the contents of the instance.
    """
    def dir(self):
        """
        Prints out the contents of the container instance.
        Mostly useful in interactive python sessions.
        """
        keys   = self.__dict__.keys()
        values = self.__dict__.values()
        for n in range(len(self.__dict__)):
            print keys[n],values[n]

    def list(self):
        """
        Returns the list of attributes in the instance.
        """
        return self.__dict__.keys()


class NetcdfDataset():
    """
    Reads in a netCDF4.Dataset from file and populates the metadata
    as class attributes. Takes exactly the same arguments as 
    netCDF4.Dataset plus one:

    convertStringToBooleans - if True (default), converts "T" to True 
    and "F" to False.

    Type help(netCDF4.Dataset) for more information on other keyword 
    arguments.
    """
    def __init__(self,filename,mode="r",clobber=True,diskless=False, 
                 persist=False,format='NETCDF4',convertStringToBooleans=True):
        """
        NetcdfDataset constructor method.
        """
        self.FILENAME = filename
        self.MODE     = mode
        self.CLOBBER  = clobber
        self.DISKLESS = diskless
        self.PERSIST  = persist
        self.FORMAT   = format

        nc = Dataset(filename,mode=mode,clobber=clobber,diskless=diskless,
                     persist=persist,format=format)
        self.nc = nc

        # Add global attributes
        setattr(self,"attributes",Container())
        for attribute in nc.ncattrs():
            attr = nc.getncattr(attribute)
            if convertStringToBooleans:
                if attr == "T":
                    attr = True
                elif attr == "F":
                    attr = False
            setattr(self.attributes,attribute,attr)

        # Add dimensions
        setattr(self,"dimensions",Container())
        for dim in nc.dimensions.keys():
            setattr(self.dimensions,dim,len(nc.dimensions[dim]))

        # Add groups
        setattr(self,"groups",Container())
        for groupName in nc.groups:
            setattr(self.groups,groupName,nc.groups[fieldName])

        # Add variables, for now, only keys. Load later.
        setattr(self,"variables",Container())
        for fieldName in nc.variables:
            setattr(self.variables,fieldName,nc.variables[fieldName])

        self.OPENED      = True
        self.TIME_OPENED = datetime.now()

    def close(self):
        """
        """
        self.nc.close()
        self.OPENED      = False
        self.TIME_CLOSED = datetime.now()
