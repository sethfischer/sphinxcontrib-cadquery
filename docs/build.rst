===============
Build a release
===============

Prerequisites
-------------

* `Git`_ version control system.
* `Python`_ >=3.9.
* `Poetry`_ for Python dependency management and building source and wheel archives.
* `node.js`_ and npm for JavaScript dependency management.


Build
-----

.. code-block:: text

    git clone https://github.com/sethfischer/sphinxcontrib-cadquery.git
    cd sphinxcontrib-cadquery
    poetry env use python3.12
    poetry install
    eval $(poetry env activate)
    npm clean-install
    make npm-build poetry-build

Following the above a ``sdist`` and ``wheel`` will be in the ``dist/`` directory.


Install
-------

The built release can be install into a project as follows.

.. rubric:: Poetry

.. code-block:: text

    poetry add path/to/dist/sphinxcontrib_cadquery-0.1.0.tar.gz


.. rubric:: Pip

.. code-block:: text

    pip install path/to/dist/sphinxcontrib_cadquery-0.1.0.tar.gz


Publish release
---------------

.. code-block:: text

    git checkout main
    cz bump --no-verify
    git push origin main && git push --tags
    make poetry-build
    poetry publish


.. _`Git`: https://git-scm.com/
.. _`Python`: https://www.python.org/
.. _`Poetry`: https://python-poetry.org/
.. _`node.js`: https://nodejs.org/
