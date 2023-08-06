|pipeline| |coverage| |pypi| |docs| |license|

.. image:: docs/source/_static/logo.svg

========================================

Slurmpter (Slurm Scripter) is a package to build Slurm submit files of a workflow of jobs easily. This package uses PyCondor_ as the backend. The user interface of slurmpter is very similar to that of PyCondor_ except for some arguments dedicated for Slurm.

Documentation
=============

Documentation of ``slurmpter`` can be found at https://slurmpter.readthedocs.io/en/latest/index.html.

Installation
============

PyPI
----

The latest release of ``slurmpter`` can be installed with ``pip``:

.. code-block:: bash

    pip install slurmpter

Conda
-----

The latest release of ``slurmpter`` can be installed with ``conda``:

.. code-block:: bash

    conda install -c isaac-cfwong slurmpter

Useful Links
============

`slurmpter @ GitLab <https://gitlab.com/isaac-cfwong/slurmpter>`_

`slurmpter mirror @ GitHub <https://github.com/isaac-cfwong/slurmpter>`_

`Issue tracker <https://gitlab.com/isaac-cfwong/slurmpter/-/issues>`_

Copyright (c) 2020 Isaac Chun Fung WONG

.. _PyCondor: https://github.com/jrbourbeau/pycondor

.. |pipeline| image:: https://gitlab.com/isaac-cfwong/slurmpter/badges/master/pipeline.svg
    :target: https://gitlab.com/isaac-cfwong/slurmpter/commits/master

.. |coverage| image:: https://gitlab.com/isaac-cfwong/slurmpter/badges/master/coverage.svg
    :target: https://codecov.io/gl/isaac-cfwong/slurmpter/

.. |pypi| image:: https://badge.fury.io/py/slurmpter.svg
    :target: https://pypi.org/project/slurmpter/
    :alt: Package on PyPI

.. |docs| image:: https://readthedocs.org/projects/sphinx/badge/?version=master
    :target: https://slurmpter.readthedocs.io/en/latest/

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://gitlab.com/isaac-cfwong/slurmpter/-/blob/master/LICENSE
