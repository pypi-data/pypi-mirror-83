# -*- coding: utf-8 -*-

import pytest
from pandalyse.trainings import Trainer, a_bit_fast_groupby_train_test_split
from pandalyse.utilities import IsIterable

from sklearn.datasets import make_classification
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

__author__ = "Simon Wehle"
__copyright__ = "Simon Wehle"
__license__ = "mit"


import pandas as pd 
import numpy as np

def create_test_data(size=10):
    X,y = make_classification(size,5)
    df = pd.DataFrame()
    for i in range(5):
        df['var%d'%i] = X[:,i]
    return df[y==1], df[y==0]

def test_trainer():
    df = create_test_data()
    t = Trainer()
    t()
    assert True

def test_trainer_no_variables():
    sig, bkg = create_test_data()
    t = Trainer()
    t.add_method("lda_test", LDA())
    t.fit(sig, bkg)
    ret = t.add_prediction(sig)
    assert isinstance(ret, pd.DataFrame)
    assert isinstance(ret['lda_test'], pd.Series)
    assert IsIterable(t.ret_prediction(sig))

def test_trainer_with_variables():
    sig, bkg = create_test_data()
    t = Trainer(['var0', 'var1', 'var2', 'var4'])
    t.add_method("lda_test", LDA())
    t.fit(sig, bkg)
    ret = t.add_prediction(sig)
    assert isinstance(ret, pd.DataFrame)
    assert isinstance(ret['lda_test'], pd.Series)    
    assert IsIterable(t.ret_prediction(sig))

def test_trainer_with_variables_alternative():
    X,y = make_classification(10, 5)
    sig, bkg = create_test_data()
    t = Trainer(['var0', 'var1', 'var2', 'var3', 'var4'])
    t.add_method("lda_test", LDA())
    t.fit(X, y)
    ret = t.add_prediction(sig)
    assert isinstance(ret, pd.DataFrame), type(ret)
    assert isinstance(ret['lda_test'], pd.Series)    
    assert IsIterable(t.ret_prediction(sig))    

def test_Trainer_add_prediction_group():
    sig, bkg = create_test_data()
    sig, _ = create_test_data(100)
    sig['mygroup'] = np.random.randint(2,size=len(sig))
    g = sig.groupby('mygroup')
    t = Trainer(['var0', 'var1', 'var2', 'var4'])
    t.add_method("lda_test", LDA())
    t.fit(sig, bkg)
    ret = t.add_prediction(sig, rank=['mygroup'])
    assert IsIterable(t.ret_prediction(sig))

def test_Trainer_comparison():
    sig, bkg = create_test_data()
    t = Trainer(['var0', 'var1', 'var2', 'var4'])
    t.add_method("lda_test", LDA())
    t.fit(sig, bkg)
    ret = t.compare_trainings(sig,bkg)
    assert True

def test_a_bit_fast_groupby_train_test_split():
    sig, _ = create_test_data(100)
    sig['mygroup'] = np.random.randint(2,size=len(sig))
    g = sig.groupby('mygroup')
    df1, df2 = a_bit_fast_groupby_train_test_split(sig, g)
    assert isinstance(df1, pd.DataFrame)
    assert isinstance(df2, pd.DataFrame)

def test_a_bit_fast_groupby_train_test_split_list():
    sig, _ = create_test_data(100)
    sig['mygroup'] = np.random.randint(2,size=len(sig))
    df1, df2 = a_bit_fast_groupby_train_test_split(sig, 'mygroup')
    assert isinstance(df1, pd.DataFrame)
    assert isinstance(df2, pd.DataFrame)

