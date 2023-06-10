======================
sphinxcontrib-cadquery
======================

A `Sphinx`_ extension for rendering `CadQuery`_ models.
A fork of the Sphinx extension in :ref:`CadQuery/cadquery <cadquery-core>`.


Directives
----------

Refer to the :doc:`directives` section for more details.

:rst:dir:`cadquery-vtk`
    Alias: **cadquery**

    Render a CadQuery model using `kitware/vtk.js`_.

:rst:dir:`cadquery-svg`
    Alias: **cq_plot**

    Render a CadQuery model using :abbr:`SVG (Scalable Vector Graphics)`.

:rst:dir:`cadquery:vtk`
    Render a CadQuery model using `kitware/vtk.js`_.
    Differs from :rst:dir:`cadquery-vtk` in that it provides additional options and content variations.


.. toctree::
    :maxdepth: 2
    :caption: Contents

    installation
    configuration
    directives
    examples/index
    related
    build


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Sphinx: https://www.sphinx-doc.org/
.. _CadQuery: https://cadquery.readthedocs.io/
.. _`kitware/vtk.js`: https://kitware.github.io/vtk-js/
