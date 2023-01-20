===
SVG
===

:rst:dir:`SVG <cadquery-svg>` renderer examples.


Simple rectangular plate
------------------------

.. cadquery-svg::

    result = cadquery.Workplane("front").box(2, 2, 0.5)
    show_object(result)
