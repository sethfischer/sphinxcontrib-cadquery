======
VTK.js
======

:rst:dir:`VTK.js <cadquery-vtk>` renderer examples.


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
