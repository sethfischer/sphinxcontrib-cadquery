================
Related projects
================

.. _cadquery-core:

CadQuery/cadquery
-----------------

:Repository: https://github.com/CadQuery/cadquery
:PyPI: Included in CadQuery core.
:Renderer: `vtk.js`_
:Exporters:
    * :func:`cadquery-latest:cadquery.occ_impl.assembly.toJSON`
    * :doc:`CadQuery SVG exporter <cadquery-latest:importexport>`

This was modified for the initial release of *sphinxcontrib-cadquery*.


CadQuery/sphinxcadquery
-----------------------

:Repository: https://github.com/CadQuery/sphinxcadquery
:PyPI: https://pypi.org/project/sphinxcadquery/
:Renderer: `three.js`_
:Exporters:
    * ``cadquery.exporters`` (TJS)


.. rubric:: Caveats

* Will not render :class:`cadquery-latest:cadquery.assembly.Assembly`


.. _`vtk.js`: https://kitware.github.io/vtk-js/
.. _`three.js`: https://threejs.org/
