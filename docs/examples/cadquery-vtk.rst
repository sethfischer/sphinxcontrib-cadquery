============
cadquery-vtk
============

:rst:dir:`VTK.js <cadquery-vtk>` renderer examples.

.. include:: ../includes/note-view-source.rst


Simple rectangular plate
------------------------

.. cadquery-vtk::

    result = cadquery.Workplane("front").box(2, 2, 0.5)


Assembly
--------

.. cadquery-vtk::

    cone = cq.Solid.makeCone(1, 0, 2)

    assembly = cq.Assembly()
    assembly.add(
        cone,
        loc=cq.Location((0, 0, 0), (1, 0, 0), 180),
        name="cone0",
        color=cq.Color("green"),
    )
    assembly.add(cone, name="cone1", color=cq.Color("blue"))

    show_object(assembly)

Sketch
------

.. cadquery-vtk::

    import cadquery as cq

    result = (
        cq.Sketch()
        .trapezoid(4, 3, 90)
        .vertices()
        .circle(0.5, mode="s")
        .reset()
        .vertices()
        .fillet(0.25)
        .reset()
        .rarray(0.6, 1, 5, 1)
        .slot(1.5, 0.4, mode="s", angle=90)
    )


Load from file
--------------

.. cadquery-vtk:: ../examples/simple-rectangular-plate.py


Options
-------

Default color
~~~~~~~~~~~~~

Set the default color using the ``color`` option.

.. cadquery-vtk::
    :color: 0.5, 1, 0.8, 1

    result = cadquery.Workplane("front").box(2, 2, 0.5)


Size and alignment
~~~~~~~~~~~~~~~~~~

Set the size using the ``width`` and ``height`` options.

Set horizontal alignment using the ``align`` option.

.. rubric:: Center

.. cadquery-vtk::
    :height: 100px
    :width: 200px
    :align: center

    result = cadquery.Workplane("front").box(2, 2, 0.5)


.. rubric:: Align left


.. cadquery-vtk::
    :height: 100px
    :width: 200px
    :align: left

    result = cadquery.Workplane("front").box(2, 2, 0.5)


.. rubric:: Align right

.. cadquery-vtk::
    :height: 100px
    :width: 200px
    :align: right

    result = cadquery.Workplane("front").box(2, 2, 0.5)
