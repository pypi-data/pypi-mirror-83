# -*- coding: utf-8 -*-

import pytest
import pandalyse
from pandalyse.analysis import Analysis

__author__ = "Simon Wehle"
__copyright__ = "Simon Wehle"
__license__ = "mit"


import pandas as pd 
import numpy as np

def create_test_df(size=10):
    df = pd.DataFrame({'A' : np.arange(size),
                      'B' : np.random.randint(2,size=size),}
                     )
    return df

def test_analysis_delivery():
    ana = pandalyse.analysis()
    assert isinstance(ana, Analysis)

def test_analysis_config_file(tmp_path):
    import os
    ana = pandalyse.analysis(str(tmp_path))

    assert len(list(tmp_path.iterdir())) == 0, "There should not be a config file yet"
    ana.init()
    # print([x for x in tmp_path.iterdir()])
    assert len(list(tmp_path.iterdir())) == 1 ,"There should be the config file"

def test_analysis_catalogue_list(tmp_path):
    ana = pandalyse.analysis(str(tmp_path))
    ana.init()
    ana.values.add([666], "test_list")
    assert ana.values.test_list[0] == 666
    # for f in list(tmp_path.iterdir()):
    #     print("Here")
    #     print(str(f))
    #     with open(str(f), 'r') as fi:
    #         print(fi.read())
    # assert 1==2
    
def test_analysis_catalogue_nparray(tmp_path):
    ana = pandalyse.analysis(str(tmp_path))
    ana.init()
    ana.values.add(np.array([666]), "test_nparray")
    # print(type(ana.values.test_nparray))
    # print(pandalyse.__version__)
    assert ana.values.test_nparray[0] == 666
    
