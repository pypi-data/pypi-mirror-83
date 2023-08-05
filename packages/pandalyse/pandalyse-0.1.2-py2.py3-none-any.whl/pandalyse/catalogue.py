# -*- coding: utf-8 -*-
""" Data Management system Catalogue

    Keeps track of all open data frames and interfaces the trainigs data..

"""

from .utilities import Base, AttrDict

import glob
import os
import pickle


class Catalogue(AttrDict, Base):
    """ Catalog object

    Generic storage manager for object in the context of the analysis tools.

    """
    def __init__(self, location=None, suff='pkl', save_fcn=pickle.dump, load_fcn=pickle.load, create_files=True,
                 autoload=False, data_type=None, binary_file=True, load_kwdct={},
                 ):
        AttrDict.__init__(self)
        Base.__init__(self, "Catalogue"+'.'+suff)
        self.suff = suff
        self.is_init = False
        self.location = location
        self._data = AttrDict()
        self._files = {}
        self._save_fcn = save_fcn
        self._load_fcn = load_fcn
        self._load_kwdct = load_kwdct
        self._create_file = create_files
        self._autoload = autoload
        self._data_type = data_type
        self._binary_file = '' if binary_file is False else 'b'
        if self._autoload:
            self.initiate()

    def __call__(self, name=None,):
        """ Main interface

        Returns objects or shows lists of available objects

        Args:
            name: Name
        """
        if name is not None:
            return self.get(name,)
        else:
            self.ls()

    def _save_entry(self, e, filename, overwrite=False):
        """ Save an enty to  afile

        Args:
            e:
            filename:
            overwrite:

        Returns:

        """
        if os.path.isfile(filename) and not overwrite:
            self.io.warning("The file already exist, confirm with overwrite=True")
            return
        if self._create_file:
            with open(filename, 'w'+self._binary_file) as f:
                self._save_fcn(e, f)
        else:
            self._save_fcn(e, filename)

    def _load_entry(self, filename):
        """ Load an entry from a file

        Args:
            filename:

        Returns: entry

        """

        if self._create_file:
            with open(filename, 'r'+self._binary_file) as f:
                obj = self._load_fcn(f, **self._load_kwdct)
        else:
            obj = self._load_fcn(filename, **self._load_kwdct)
        if isinstance(obj, dict):
            obj = AttrDict(obj)
        return obj

    def ls(self):
        """ List all availabel data sets

        """
        self.io.debug("Listing all recorded files")
        self.initiate()
        print("Type: " + self.suff)
        print("  ---  %d objects, loaded %d: " % (len(self._files), len(self._data)))
        for k in self._files:
            print('- {0:10}  >> {1}'.format(k, self._files[k]))

    def initiate(self):
        """ Initiating the catalog by scanning the folder for siuted files

        """
        self.io.debug("Inititating")
        if self.location is None:
            self.location = './'
        files = glob.glob(self.location + '/*.%s' % self.suff)
        for f in files:
            index = f.split('/')[-1].split('.')[0]
            self._files[index] = f
            if self._autoload:
                self.get(index, True)
        self.is_init = True

    def add(self, obj, name, overwrite=False):
        """ Add an object to the data storage

        Args:
            obj: object
            name: name in the catalogue

        """
        self.io.info("Adding object to the collection")

        if self._data_type is not None:
            assert isinstance(obj, self._data_type), 'Given object is not supported'

        if self.location is not None:
            # assert type in self.data, "Not a valid data type"
            self._save_entry(obj, self.location + '/%s.%s' % (name, self.suff), overwrite=overwrite)
            self.initiate()
            self.io.debug("Data set successfully added")
        else:
            self.warn('No location set')

    def get(self, name=None, reload=False):
        """ Get an item from the catalogue

        Args:
            name:
            reload:

        Returns:

        """

        if name is None:
            return self.ls()

        self.io.debug("Getting data set " + name)
        if not self.is_init and reload is False:
            self.initiate()
        if name in self._data and reload is False:
            return self._data[name]
        elif name in self._files:
            self._data[name] = self._load_entry(self._files[name])
            self[name] = self._data[name]
            return self._data[name]
        else:
            self.warn('Did not find entry %s' % name)
