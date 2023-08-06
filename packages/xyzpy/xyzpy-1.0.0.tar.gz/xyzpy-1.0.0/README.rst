.. raw:: html

    <img src="https://github.com/jcmgray/xyzpy/blob/master/docs/_static/xyzpy-logo-title.png" width="450px">

.. image:: https://dev.azure.com/xyzpy-org/xyzpy/_apis/build/status/jcmgray.xyzpy?branchName=develop
  :target: https://dev.azure.com/xyzpy-org/xyzpy
  :alt: Azure CI
.. image:: https://codecov.io/gh/jcmgray/xyzpy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jcmgray/xyzpy
  :alt: Code Coverage
.. image:: https://img.shields.io/lgtm/grade/python/g/jcmgray/xyzpy.svg
  :target: https://lgtm.com/projects/g/jcmgray/xyzpy/
  :alt: LGTM Grade
.. image:: https://readthedocs.org/projects/xyzpy/badge/?version=latest
  :target: http://xyzpy.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

-------------------------------------------------------------------------------

`xyzpy <https://github.com/jcmgray/xyzpy>`__ is python library for efficiently
generating, manipulating and plotting data with a lot of dimensions, of the
type that often occurs in numerical simulations. It stands wholly atop the
labelled N-dimensional array library `xarray <http://xarray.pydata.org/en/stable/>`__.
The project's documentation is hosted on `readthedocs <http://xyzpy.readthedocs.io/>`__.

The aim is to take the pain and errors out of generating and exploring data
with a high number of possible parameters. This means:

- you don't have to write super nested for loops
- you don't have to remember which arrays/dimensions belong to which variables/parameters
- you don't have to parallelize over or distribute runs yourself
- you don't have to worry about loading, saving and merging disjoint data
- you don't have to guess when a set of runs is going to finish
- you don't have to write batch submission scripts or leave the notebook to use SGE, PBS or SLURM

As well as the ability to automatically parallelize over runs, ``xyzpy``
provides the ``Crop`` object that allows runs and results to be written to disk,
these can then be run by any process with access to the files - e.g. a batch system
such as SGE, PBS or SLURM - or just serve as a convenient persistent progress mechanism.

Once your data has been aggregated into a ``xarray.Dataset`` or ``pandas.DataFrame``
there exists many powerful visualization tools such as
`seaborn <https://seaborn.pydata.org/>`_, `altair <https://altair-viz.github.io/>`_, and
`holoviews <https://holoviews.org/#>`_ / `hvplot <https://hvplot.holoviz.org/>`_.
To these ``xyzpy`` adds also a simple 'oneliner' interface for interactively plotting the data
using `bokeh <https://bokeh.pydata.org/en/latest/>`__, or for static, publication ready figures
using `matplotlib <https://matplotlib.org/>`__, whilst being able to see the dependence on
up to 4 dimensions at once.

.. image:: docs/ex_simple.png

Please see the `docs <http://xyzpy.readthedocs.io/>`__ for more information.

