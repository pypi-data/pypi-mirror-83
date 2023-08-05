=========
pandalyse
=========

This is the documentation of **pandalyse**.

.. note::

    This package is in the early stage of development.

What is pandalyse
=================

Pandalyse offers an analysis environment and tools for pandas.
The main features are

* **Selector**: Define and store cuts in a Selector object: `cutted_df = selector(df)`
* **Trainer**: Train multiple mva with scikit-learn interface in the way: `trainer.fit(signal_df, background_df)`
* **Analysis**: Store and retrive Selectors, Trainings, numpy-arrays and dataframes in predefined locations: `df = ana.data.get("MySignalData")`


Installation
============

::

    pip install pandalyse 


Usage
=====

Selectors
---------

Selectors store cuts on colums of a `pandas.Dataframe`.
All cuts are stored as a list of strings, which are applied with the AND condition.

Example::

    import pandalyse
    
    sel = pandalyse.Selector(['column1 > 0', 'column2 == 1'])
    
    # Assume the existance of a pandas datframe 'df' and 'second_df'
    df_cutted_1 = sel(df)

    sel.add_cut('column3 < 100')
    df_cutted_2 = sel(second_df)

    df_cutted_3 = sel(df, 'Temporary_Cut == 1')


Analysis
--------

The Analysis is the central part of `pandalyse`. 
It consists of a `.pandalyse` file which contains information on folders where pandas.DatsFrames, pandalyse.Selectors, pandalyse.Trainer and numpy.arrays are stored.

Example::

    import pandalyse
    import numpy as np 

    ana = pandalyse.analysis('path/to/(desired)/analysis/dir')
    # ana = pandalyse.analysis() will use `pwd`

    # ...
    # assuming the existance of a signal and background dataframe
    ana.data.add(df_bkg, 'background')
    ana.data.add(df_sig, 'signal')

    # doing some calculations
    ana.values.add(0.5, 'efficiency')
    ana.values.add(np.arange(3), 'example_array')

    print(ana.values.example_array/ana.values.efficiency)
    # >> [0, 0.5, 1]

    # ls path/to/(desired)/analysis/dir
    # >> background.hdf signal.hdf efficiency.val example_array.val


Trainer
-------

A `pandalyse.Trainer` can take a list of features of a dataframe and classifyer with an `sklearn` interface methods can be added.

Example::

    import pandalyse

    ana = pandalyse.analysis()

    tr = pandalyse.Trainer(['column1', 'column2'])
    tr.add_method('bdt', some.sklearn_like.classifyer())
    tr.add_method('nn',  some.sklearn_like.classifyer2())

    tr.fit(ana.data.get('signal'), ana.data.get('background'))

    ana.trainigs.add(tr, 'first_training')


Contents
========

.. toctree::
   :maxdepth: 2
   Overview <index>
   License <license>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
