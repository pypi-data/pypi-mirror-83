# -*- coding: utf-8 -*-
""" Keep track of all the settings and locations for an analysis

"""

from .utilities import Base, Singleton, AttrDict
from .catalogue import Catalogue
from .selector import Selector
from .trainings import Trainer

import os
import yaml
import pandas as pd


ANALYSISFILE = '/.pandalyse'


@Singleton
class InstantAnalysisDelivery(Base):
    def __init__(self, ):
        Base.__init__(self, "InstantAnalysisDelivery")

    def __call__(self, loc=None, *args, **kwargs):
        return Analysis(loc)


def fcn_save_dataframe(df, filename):

    assert isinstance(df, pd.DataFrame)
    df.to_hdf(filename, 'tree')


class Analysis(Base):
    """ Analysis class

    Keeps track of datasets, trainers, values and selectors.
    A local configuration in ANALYSISFILE can store all the necessary information.

    """
    data = None
    selector = None
    trainings = None
    values = None

    def __init__(self, loc=None):
        """

        Args:
            loc:
        """
        Base.__init__(self, "Analysis")
        self.io.debug("Starting Analysis")
        self.location = loc if loc is not None else os.getcwd()
        self.config = AttrDict({'data': None, 'selectors': None, 'values': None, 'trainings': None})

        self._init_at_location()
        self._init_managers()
        # self.data = Catalogue(self.config['data'], suff='hdf',
        #                       save_fcn=fcn_save_dataframe, load_fcn=pd.read_hdf, create_files=False)
        # self.selectors = Catalogue(self.config['selectors'], suff='sel', autoload=True, data_type=Selector)
        # self.trainings = Catalogue(self.config['trainings'], suff='trainer', autoload=False, data_type=Trainer)
        # self.values = Catalogue(self.config['values'], suff='val',
        #                         save_fcn=yaml.dump, load_fcn=yaml.load, autoload=True, binary_file=False)

    def init(self, force=False):
        """ Inititate the analysis file

        Args:
            force: (bool) Force the creation if already existing

        """
        if os.path.isfile(self.location + ANALYSISFILE) and not force:
            self.io.warning("Previous analysis found. " + self.location + ANALYSISFILE)
            return
        loc = self.location
        self._write_config(loc=loc)
        self._init_managers()

    def _init_managers(self):
        """ Initiate the managers

        """
        self.data = Catalogue(self.config['data'], suff='hdf',
                              save_fcn=fcn_save_dataframe, load_fcn=pd.read_hdf, create_files=False)
        self.selectors = Catalogue(self.config['selectors'], suff='sel', autoload=True, data_type=Selector)
        self.trainings = Catalogue(self.config['trainings'], suff='trainer', autoload=False, data_type=Trainer)
        self.values = Catalogue(self.config['values'], suff='val',
                                save_fcn=yaml.dump, load_fcn=yaml.load, autoload=True, binary_file=False, load_kwdct={'Loader': yaml.Loader})

    def _write_config(self, loc=None):
        """ Write the config file

        Args:
            loc:

        """

        if loc is not None:
            for c in self.config:
                self.config[c] = loc
        with open(self.location + ANALYSISFILE, 'w') as f:
            yaml.dump(dict(self.config), f, default_flow_style=False, allow_unicode=True)

    def _init_at_location(self):
        """ initiate the analysis at a specific location.

        """
        if not os.path.isfile(self.location + ANALYSISFILE):
            self.io.info("No previous analysis found. Run init to create config file.")
            self.io.info("Using default configuration.")
        else:
            self.io.info("Found existing analysis at " + self.location + ANALYSISFILE)
            self.config = AttrDict(yaml.load(open(self.location + ANALYSISFILE), Loader=yaml.SafeLoader))

    def set_data_location(self, location=None):
        self.config.data = location
        self._write_config()

    def set_selector_location(self, location=None):
        self.config.selectors = location
        self._write_config()

    def set_values_location(self, location=None):
        self.config.values = location
        self._write_config()

    def set_trainer_location(self, location=None):
        self.config.trainings = location
        self._write_config()

    def get_data(self, name=None):
        return self.data.get(name)

    def get_selector(self, name=None):
        return self.selectors.get(name)

    def get_values(self, name=None):
        return self.values.get(name)
