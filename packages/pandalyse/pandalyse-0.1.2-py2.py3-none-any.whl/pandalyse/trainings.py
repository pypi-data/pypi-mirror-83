# -*- coding: utf-8 -*-
""" This is the training interface

    Warning: This part is insufficiently documented..

"""

from .utilities import Singleton, Base, IsIterable

import glob
import os
import numpy as np
import pandas as pd
from time import time

##
## Depreciated 
## vvvvvvvvvvv
##
# class TrainingManager(Base):
#     """ This class manages all the available trainings

#     """
#     def __init__(self, location=None):
#         Base.__init__(self, "TrainingManager")
#         self.io.debug("Initiating Training Manager")
#         self.trainings_location = location
#         self.trainings = None
#         self.names = None
#         self.active_trainer = None

#     def initialize(self):
#         self.trainings = glob.glob(self.trainings_location+self.trainings_prefix + '*')
#         self.names = [i.split(self.trainings_prefix)[1] for i in self.trainings]

#     def get_trainer(self, name=None):
#         self.initialize()
#         if name is None:
#             self.io.debug("Loading active Trainer")
#             if self.active_trainer is not None:
#                 return self.active_trainer
#             else:
#                 if self.active_name is not None:
#                     self.active_trainer = MultiTrainer(self.trainings_location + self.trainings_prefix
#                                                        + self.active_name, self.active_name)
#                     return self.active_trainer
#         else:
#             self.io.debug("Loading trainer " + name)
#             if name in self.names:
#                 trainer = MultiTrainer(self.trainings_location + self.trainings_prefix + name, name)
#                 return trainer
#             else:
#                 self.io.error("This trainer does not seem to exist")
#         self.error("Cant get Trainer for reasons..")
#         return None

#     def ls(self, ):
#         self.io.debug("Listing all Trainings")
#         self.initialize()
#         self.io.info("Training location : " + self.trainings_location)
#         self.io.info("Training prefix : " + self.trainings_prefix)
#         self.io.info("Active Training : " + self.active_name)
#         self.io.info(self.names)

#     def set_active(self, train_name):
#         self.io.debug("Activating training folder " + train_name)
#         self.initialize()
#         if train_name not in self.names:
#             self.io.info(train_name)
#             self.io.info(self.names)
#             self.warn("Training not found")
#             return
#         self.active_name = train_name

#     def create_training(self, trainer, name):
#         self.io.info("Creating a new training for " + name)

#         assert isinstance(trainer, Trainer), "please insert trainer instance"
#         assert isinstance(name, str), "please enter a valid string"

#         new_dir_name = self.trainings_location + self.trainings_prefix + name
#         try:
#             os.mkdir(new_dir_name)
#         except :
#             self.io.error("no way")
#         else:
#             pass
#             #trainer.save(new_dir_name + '/' + s.DEFAULTTRAINING)


# class MultiTrainer(Base):
#     """ This class manages the trainings for all the decay channels.

#     """
#     def __init__(self, location, name, hashes):
#         Base.__init__(self, "MultiTrainer")
#         self.io.debug("Initiating MultiTrainer " + name)
#         self.location = location
#         self.hashes = hashes
#         self.trainers = {}
#         self.name = name
#         self.active = False

#         self.default_training = None

#         if not os.path.exists(self.location):
#             self.io.error("My location does not Exist 0_O")
#             return
#         self.default_training = self.location

#     def activate(self):
#         """Activate the multi trainer

#             This method performs some consistency checks and activates itself afterwards.

#         """
#         self.io.debug("Activating all trainings")

#         trainers = glob.glob(self.location+'/*.trainer')
#         names = [int(n.split('.')[0].split('/')[-1]) for n in trainers]
#         self.trainers = {}

#         for h in self.hashes:
#             if h not in names:
#                 self.io.error("I cannot find " + str(h) + " in the folder")

#         for t in trainers:
#             hash = int(t.split('.')[0].split('/')[-1])
#             self.trainers[hash] = Trainer(t)

#         self.active = True

#     def add_prediction(self, df, name=None, prefix=''):
#         self.io.info("Adding prediction for " + self.name)

#         assert isinstance(df, pd.DataFrame), "We need data frames!!"

#         if not self.active:
#             self.activate()

#         if name is None:
#             name = prefix + self.name

#         df[name] = 0

#         for h in self.trainers:
#             t = self.trainers[h]
#             sel = abs(df.decay_hash) == h
#             ret = t.ret_prediction(df[sel])
#             df.loc[sel, name] = ret

#     def train_all(self):
#         self.io.info("Training all channels")
#         for h in self.hashes:
#             self.train_hash(h)

#     def train_hash(self, h):
#         h = int(h)
#         self.io.info("Training hash " + str(h))
#         if not int(h) in self.hashes:
#             self.io.error("This hash is not supported..")
#             return
#         self.io.debug("Creating new Trainer from default")
#         trainer = Trainer().load(self.default_training)

#         self.io.debug("Loading training data")
#         sig = None #ana.dm.get_train_sig(int(h))
#         sig = sig[sig.MCflag > 0]
#         bkg = None #ana.dm.get_train_bkg(int(h))
#         bkg = bkg[bkg.MCflag <= 0]
#         # datmanager get trainings data...

#         self.io.debug('Starting Training')

#         trainer.fit(sig, bkg)
#         trainer.save(self.location + '/%d.pkl' % h)
#         self.trainers[h] = trainer

#         self.io.info('Training done')


class Trainer(Base):
    """ Class for Trainings

        This class trains all the methods.

    """
    def __init__(self, variables=None, mmd=None, filename=None):
        Base.__init__(self, "Trainer")
        self.io.debug("Initiating")
        self.variables = variables
        self.methods = {} if mmd is None else mmd
        # Ok i know the following is ugly but it keeps backward capability
        if filename is not None or type(variables) is str:
            if filename is None:
                filename = variables
            from sklearn.externals import joblib
            try:
                from_safe = joblib.load(filename)
                self.variables = from_safe[0]
                self.methods = from_safe[1]
            except TypeError:
                self.io.error("What is wrong with " + str(filename))

    def __call__(self, df=None, *args, **kwargs):
        """

        Args:
            df:

        Returns:

        """
        if df is not None:
            return self.ret_prediction(df)
        else:
            vars = ''
            if self.variables is not None:
                for v in self.variables:
                    vars += v + ' '
            self.io.info("Variables : " + vars)
            methods = ''
            for m in self.methods:
                methods += m + ' '
            self.io.info("Methods : " + methods)

    def add_method(self, m_name, m):
        self.methods[m_name] = m

    def _df(self, df):
        """ Select variables from DataFrame if there are predefined
        """
        if not isinstance(df, pd.DataFrame):
            self.io.warning("Did not reicive dataframe")
            return df
        return df if self.variables is None else df[self.variables] 

    def fit(self, sig, bkg, w=None):

        if isinstance(bkg, pd.DataFrame):
            # sig and bkg are DatFrames, construct X and y
            for i in [sig, bkg]:
                assert isinstance(i, pd.DataFrame), "Please provide pandas DataFrames for now"
            X = self._df(sig).append(self._df(bkg))
            X = X.fillna(-999)
            y = np.append(np.zeros(len(sig)) == 0, np.zeros(len(bkg)) > 1)
        else:
            # X and y are given
            if isinstance(sig, pd.DataFrame):
                X = self._df(sig)
            else:
                X = sig
            y = bkg

        if w is not None:
            w = np.append(np.ones(len(sig)), np.array(w))

        for m in self.methods:
            n_vars = 'all' if self.variables is None else str(len(self.variables))
            self.io.info("Training " + m + ' with ' + n_vars +  " Variables")
            start = time()
            try:
                self.methods[m].fit(self._df(X), y, w)
            except Exception:
                self.io.warning(f"Method {m} may not support weights")
                self.methods[m].fit(self._df(X), y)
            end = time()
            self.io.info('This took {:.2f} seconds'.format(end-start))

    def add_prediction(self, d, rank=False, outname=''):
        # d.fillna(-999, inplace=True)
        for name in self.methods:
            try:
                d[name+outname] = self.methods[name].predict_proba(self._df(d))[:, 1]
            except ValueError:
                self.error(f"Input data has bad values or shape.. skipping {name}")
            except AttributeError:
                self.warn("no proba")
                d[name+outname] = self.methods[name].predict(self._df(d))
            if rank:
                group = ['expno', 'runno', 'evtno']  # Default for Belle 1
                if isinstance(rank, list):
                    group = rank
                # if 'fileNO' in d.columns:
                #     group.append('fileNO')
                d[name+outname+'_rank'] = d.groupby(group)[name+outname].rank(ascending=False)
        return d

    def ret_prediction(self, d):
        if len(self.methods) > 1:
            self.io.error("too many methods")
            return
        d.fillna(-999, inplace=True)
        for name in self.methods:
            try:
                    return self.methods[name].predict_proba(self._df(d))[:, 1]
            except ValueError:
                self.io.error("Input data has bad values.. skipping training")
                return np.zeros(len(d))
            except AttributeError:
                self.io.warn("no proba")
                return self.methods[name].predict(self._df(d))
        else:
            self.io.warn('Did not return training')

    def compare_trainings(self, sig, bkg, w=None, figsize=(16, 10), save_as=None):
        """ Experimental trainings comparison

        Args:
            sig:
            bkg:
            w:
            figsize:
            save_as:

        Returns:

        """
        X = sig.append(bkg)
        X = self._df(X.fillna(-999))
        y = np.append(np.zeros(len(sig)) == 0, np.zeros(len(bkg)) > 1)

        X = self.add_prediction(X)

        import matplotlib.pyplot as plt

        plt.figure(figsize=figsize)
        for m in self.methods:
            preds = X[m]

            sort = y[preds.argsort()][::-1]
            s = sort.cumsum()

            eff = s / float(s[-1])
            pur = s / np.arange(1, len(sort) + 1)

            plt.plot(eff, pur, label=m)
            self.io.info('{:30s} Score: {:.2f}'.format(m, self.methods[m].score(self._df(X), y)))

        plt.xlim(0.0, 1.05)
        plt.ylim(0.0, 1.05)
        plt.xlabel('Purity')
        plt.ylabel('Efficiency')
        plt.legend(loc='best')
        if save_as:
            plt.savefig(save_as)
        plt.show()

    def save(self, filename):
        self.io.info('Saving Classifier')
        from sklearn.externals import joblib
        tosafe = (self.variables, self.methods)
        joblib.dump(tosafe, filename)

    def load(self, filename):
        self.io.debug('Loading Classifier')
        from sklearn.externals import joblib
        fromsafe = joblib.load(filename)
        return Trainer(fromsafe[0], fromsafe[1])


def a_bit_fast_groupby_train_test_split(df, g, *args, **kwds):
    """ Split DataFrame within groups

    Args:
        df: DataFrame
        g: Groups, groupby or str or array of str
        *args:
        **kwds:

    Returns:

    """
    import pandas
    import numpy as np
    from sklearn.model_selection import train_test_split

    if not isinstance(g, pandas.core.groupby.DataFrameGroupBy):
        print('Creating groupby')
        g = df.groupby(g)
    l = list(g.groups.keys())
    # shuffle groups
    ltr, lte = train_test_split(l, *args, **kwds)
    # get group indeces for dataframe
    itr = np.array([g.groups[gr].values for gr in ltr])
    ite = np.array([g.groups[gr].values for gr in lte])
    # unravel indeces
    itr = np.concatenate(itr).ravel()
    ite = np.concatenate(ite).ravel()

    df_train = df.loc[itr]
    df_test = df.loc[ite]

    return df_train, df_test
