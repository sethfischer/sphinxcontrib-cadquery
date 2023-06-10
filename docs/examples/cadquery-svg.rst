============
cadquery-svg
============

:rst:dir:`SVG <cadquery-svg>` renderer examples.

.. include:: ../includes/note-view-source.rst


Simple rectangular plate
------------------------

.. cadquery-svg::

    result = cadquery.Workplane().box(2, 2, 0.5)
    show_object(result)


Pillow block
------------

.. cadquery-svg::

    (length, height, diam, thickness, padding) = (30.0, 40.0, 22.0, 10.0, 8.0)

    result = (
        cq.Workplane()
        .box(length, height, thickness)
        .faces(">Z")
        .workplane()
        .hole(diam)
        .faces(">Z")
        .workplane()
        .rect(length - padding, height - padding, forConstruction=True)
        .vertices()
        .cboreHole(2.4, 4.4, 2.1)
    )

    show_object(result)
