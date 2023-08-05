# -*- coding: utf-8 -*-
""" Selector Module

    Select data from channels.
    The Selector class is held quite generic. It allows for selection of data from a DataFrame and can
    store generic cuts.

    Some special derivations for this analysis are created below Selector.
    Cut classes perform some special cuts.


"""


from __future__ import print_function

from .utilities import Base, IsIterable

import pandas as pd
import numpy as np


class Selector(Base):
    """ Selector Class

        Mighty mighty class for selecting cuts and getting all the data.
        The idea is that there is the main DataFrame and a subset of the same which data one can directly use.
        The general approach is, that certain masks are created for cuts and the user sees the original DataFrame
        through the masks.

        The special cuts dictionary hods function pointers for functions taking a DataFrame and returning a boolean mask
        for returning the selected columns with true.

    """
    def __init__(self, cuts=None):
        Base.__init__(self, 'Selector')
        self.io.debug("Selector")
        self.cutlist = []
        self._special_cuts = {}
        self.temp_cut = None
        self._special_cuts['temp_cut'] = self._get_temp_cut_mask
        self.applied = False
        self.last_mask = None
        self.id_last = None

        if cuts is not None:
            if isinstance(cuts, str):
                self.add_cut(cuts)
            else:
                assert IsIterable, "Please provide string or list of strings as default cuts"
                for c in cuts:
                    self.add_cut(c)

    def __call__(self, df=None, temp_cut=None, force=False, ):
        """ Main interface for the selector

            Create a mask out of the cuts and then return the masked dataframe

        Args:
            df (DataFrame): Input DataFram object
            force (bool): Force the calculation of the mask

        Returns:
            DataFrame with a mask
        """
        if df is None:
            self.io.info("No DataFrame given.")
            self.show()
            return
        if temp_cut is not None:
            assert isinstance(temp_cut, str), "Please use a string to cut on the data frame"
            self.temp_cut = temp_cut
        if self.id_last == id(df) and not force and self.applied and temp_cut is None:
            self.debug("Yay not need to process again")
            try:
                ret_df = df.loc[self.last_mask]
            except:
                self.io.error("Well maybe we need to redo it again")
                self.id_last = id(df)
                ret_df = self.transform(df, )
        else:
            self.id_last = id(df)
            ret_df = self.transform(df,)

        return ret_df

    def initiate(self, df):
        """ Depreciated initiation function

        Args:
            df:

        """

        assert isinstance(df, pd.DataFrame), "DAAAATAFRAME ?"

        self.io.debug('Initiate')

    def reset(self):
        """ Resets the selector object

        """
        self.cutlist = []
        self._special_cuts = {}
        self.applied = False

    def reset_cuts(self):
        """ Resets all cuts

        """
        self.applied = False
        self.cutlist = []

    def rm_cut(self, i):
        """ Remove a specific cut

        Args:
            i: cut number in array, see show() for index
        """
        self.applied = False
        self.cutlist.pop(i)

    def show(self):
        """ Shows all cuts of the selector

        """
        self.io.info('There are ' + str(len(self.cutlist)) + " Cuts")
        if len(self.cutlist) > 0:
            print("Cuts:")
            for i, c in enumerate(self.cutlist):
                print("- %d : %s"%(i, c))
        #print("Builtin: ")
        #for c in self._special_cuts:
        #    print("- " + self._special_cuts[c].get_info())
        self.applied_warning()

    def applied_warning(self):
        """ Depreciated warning, shold not appear anymore

        """
        if not self.applied:
            self.io.warning('There are some un-applied cuts')

    def add_cut(self, cut,):
        """ Main functionality to add cuts

        Args:
            cut: (str) add a cut
        """
        self.applied = False
        if cut not in self.cutlist:
            self.io.debug(cut)
            self.cutlist.append(cut)
        else:
            self.io.warning(f"Cut '{cut}' already added.")

    def change_cut(self, i, cut):
        """ Change a cut at index i

        Args:
            i: index of the cut
            cut:  new cut
        """
        self.applied = False
        self.cutlist[i] = cut

    def apply_cuts(self, df,):
        """ Applies the cuts to the dataframe

        Args:
            df: DataFrame to apply cuts to

        Returns: DataFrame with cuts

        """
        self.io.debug("DEPRECIATES, use transform instead")
        return self.transform(df)

    def transform(self, df):
        """ Apply the cuts to the DataFrame

        Args:
            df:

        Returns:

        """

        self.last_mask = self.get_mask(df)
        data = df.loc[self.last_mask]
        # self.initiate(data)
        return data

    def get_mask(self, df):
        """ get the bool cut mask for a DataFrame

        Args:
            df: Cut DataFrame

        Returns: bool, Series

        """
        self.io.debug("Applying cuts")
        #
        # mask = pd.Series(np.ones(len(df)) == 1, index=df.index, dtype=bool)
        mask = np.ones(len(df), dtype=bool)

        # Applying special cuts like q2 bin
        for c in self._special_cuts:
            self.io.debug("Applying special cut " + c)
            cut_mask = self._special_cuts[c](df)

            mask = mask & cut_mask

        # Applying cuts selected by a query on the df
        if len(self.cutlist) > 0:
            for c in self.cutlist:
                self.io.debug("Applying cut " + c)
                try:
                    isel = df.eval(c)
                except NameError:
                    self.io.error("Malicious cut " + c)
                else:
                    #cut_mask = pd.Series(np.ones(len(df)) == 0, index=df.index, dtype=bool)
                    cut_mask = np.zeros(len(df), dtype=bool)
                    cut_mask[isel] = True
                    mask = mask & cut_mask
        self.applied = True
        return mask

    def random_subset(self, df, n):
        """ Return a random subset the datafram of length n

        Args:
            df: DataFrame
            n: length of the subset

        Returns: DataFrame randomized length n

        """
        data = self.apply_cuts(df,)
        if len(data) < n:
            self.io.warning("Data set is not long enough")
            return data.sample(n)
        else:
            return data.sample(n)


    def _get_temp_cut_mask(self, df):
        """ Special cut to apply tempcut only once

        Args:
            df: dataframe

        Returns: cut mask

        """
        mask = np.ones(len(df), dtype=bool)
        if self.temp_cut is None:
            return mask
        else:
            if isinstance(self.temp_cut, str):
                try:
                    isel = df.eval(self.temp_cut)
                except NameError:
                    self.io.error("Malicious cut " + self.temp_cut)
                else:
                    cut_mask = np.zeros(len(df), dtype=bool)
                    cut_mask[isel] = True
                    mask = mask & cut_mask
            else:
                self.io.warning("Can't apply temporary cut")
        self.temp_cut = None
        return mask

    def __add__(self, other):
        return MultiSelector(self, other)


class MultiSelector(Base):
    """ Multi Selector Class

        Mighty mighty class for selecting cuts and getting all the data.
        The idea is that there is the main DataFrame and a subset of the same which data one can directly use.
        The general approach is, that certain masks are created for cuts and the user sees the original DataFrame
        through the masks.

        The special cuts dictionary holds function pointers for functions taking a DataFrame and returning a boolean mask
        for returning the selected columns with true.

    """
    def __init__(self, *sels):
        Base.__init__(self, 'MultiSelector')
        self.io.debug("MultiSelector")
        self.selectors = []
        for s in sels:
            self.add(s)

    def add(self, sel):
        """ Add a Selector

        Args:
            sel:

        Returns:

        """
        assert isinstance(sel, Selector), 'Only adding selectors is currently supported'
        self.selectors.append(sel)

    def transform(self, df, temp_cut=None, force=False):
        """ transform the dataframe with the selectors

        Args:
            df:
            temp_cut:
            force:

        Returns:

        """
        first = True
        df_ret = None

        for s in self.selectors:

            n_events = None
            # if subset is not None:
            #     if h in subset:
            #         n_events = subset[h]
            n_events = None

            if first:
                df_ret = s(df, temp_cut, force)
                first = False
            else:
                df_ret = df_ret.append(s(df, temp_cut, force))

        return df_ret.reset_index(drop=True, )

    def __call__(self, df=None, temp_cut=None, force=False, ):
        """ Main interface for the selector

            Create a mask out of the cuts and then return the masked dataframe

        Args:
            df (DataFrame): Input DataFram object
            force (bool): Force the calculation of the mask

        Returns:
            DataFrame with a mask
        """

        ret_df = None

        if temp_cut is not None:
            assert isinstance(temp_cut, str), "Please use a string to cut on the data frame"
            self.temp_cut = temp_cut
        if df is not None:
            ret_df = self.transform(df, temp_cut, force)
        return ret_df
