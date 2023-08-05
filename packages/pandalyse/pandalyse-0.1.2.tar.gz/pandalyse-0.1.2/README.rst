=========
pandalyse
=========


A toolkit for an analysis environment with pandas.

Documentation
-------------

[![Documentation Status](https://readthedocs.org/projects/pandalyse/badge/?version=latest)](https://pandalyse.readthedocs.io/en/latest/?badge=latest)


What is pandalyse
-----------------

Pandalyse offers an analysis environment and tools for pandas.
The main features are:

* **Selector**: Define and store cuts in a Selector object: `cutted_df = selector(df)`
* **Trainer**: Train multiple mva with scikit-learn interface in the way: `trainer.fit(signal_df, background_df)`
* **Analysis**: Store and retrive Selectors, Trainings, numpy-arrays and dataframes in predefined locations: `df = ana.data.get("MySignalData")`
