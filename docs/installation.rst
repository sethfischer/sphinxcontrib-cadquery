============
Installation
============

.. rubric:: Poetry

.. code-block:: text

    poetry add sphinxcontrib-cadquery


.. rubric:: Pip

.. code-block:: text

    pip install sphinxcontrib-cadquery


.. note::

    It is not possible to install *sphinxcontrib-cadquery* from VCS i.e.
    ``python -m pip install git+https://github.com/…``, or
    ``poetry add git+https://github.com/…`` as this circumvents the :doc:`build
    process<build>`.


Enable the extension in your Sphinx ``conf.py`` file:

.. code-block:: python

    extensions = [
        "sphinxcontrib.cadquery",
    ]

