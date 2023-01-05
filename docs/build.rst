===============
Build a release
===============

Prerequisites
-------------

* `Git`_ version control system.
* `Python`_ >=3.9, and python-venv.
* `Poetry`_ for Python dependency management and building source and wheels archives.
* `node.js`_ and npm for JavaScript dependency management.


Build
-----

.. code-block:: console

    git clone https://github.com/sethfischer/sphinxcontrib-cadquery.git
    cd sphinxcontrib-cadquery
    python3.9 -m venv .venv
    . .venv/bin/activate
    pip install -U pip
    poetry install
    make npm-build poetry-build

Following the above a ``sdist`` and ``wheel`` will be in the ``dist/`` directory.


Install
-------

The built release can be install into a project as follows.

.. rubric:: Poetry

.. code-block:: console

    poetry add path/to/dist/sphinxcontrib_cadquery-0.1.0.tar.gz


.. rubric:: Pip

.. code-block:: console

    pip install path/to/dist/sphinxcontrib_cadquery-0.1.0.tar.gz


.. _`Git`: https://git-scm.com/
.. _`Python`: https://www.python.org/
.. _`Poetry`: https://python-poetry.org/
.. _`node.js`: https://nodejs.org/
