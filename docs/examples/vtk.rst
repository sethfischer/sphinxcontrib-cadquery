============
cadquery:vtk
============

Examples of the :rst:dir:`cadquery:vtk` directive.

.. include:: ../includes/status-pre-alpha.rst

:rst:dir:`cadquery:vtk` is based on the docutils "figure" directive having similar features and syntax:

* The model may be captioned.
* Notes may be added below the code block.
* Models may be referenced by name: :ref:`color example <color-example>`.

The model source code is defined in either a :rst:dir:`sphinx-master:code-block` or
:rst:dir:`sphinx-master:literalinclude`, meaning:

* All options for :rst:dir:`sphinx-master:code-block` or :rst:dir:`sphinx-master:literalinclude`
  may be used such as :rst:dir:`sphinx-master:code-block:linenos` and :rst:dir:`sphinx-master:code-block:emphasize-lines`.
* Model source code blocks may be referenced by name: :ref:`CadQuery source code for a rectangular plate <cq-rectangular-plate>`.

.. include:: ../includes/tip-view-source.rst


Simple rectangular plate
------------------------

.. cadquery:vtk::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. code-block:: python
        :name: cq-rectangular-plate
        :linenos:
        :emphasize-lines: 5

        """Simple rectangular plate."""

        import cadquery as cq

        result = cadquery.Workplane().box(2, 2, 0.5)

    .. rubric:: Notes:

    #. Line numbers are added with ``linenos``.
    #. Line number 5 is emphasized with ``emphasize-lines``.


Assembly
--------

.. cadquery:vtk::

    An assembly of two cones.

    .. code-block:: python

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

.. cadquery:vtk::

    A sketch.

    .. code-block:: python

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


Source from file
----------------

.. cadquery:vtk::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. literalinclude:: ../../examples/simple-rectangular-plate.py


Content variations
------------------

Code block: without caption or source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:vtk::
    :include-source: no

    ..

    .. code-block:: python

        """Simple rectangular plate."""

        import cadquery as cq

        result = cadquery.Workplane().box(2, 2, 0.5)


Code block: with both caption and source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:vtk::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. code-block:: python

        """Simple rectangular plate."""

        import cadquery as cq

        result = cadquery.Workplane().box(2, 2, 0.5)


Code block: with caption, source, and notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:vtk::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. code-block:: python

        """Simple rectangular plate."""

        import cadquery as cq

        result = cadquery.Workplane().box(2, 2, 0.5)

    Notes may follow the ``code-block``.

    #. The model source code is loaded from a ``code-block`` directive.
    #. The model is captioned.
    #. The model source code is displayed.
    #. These are notes.


Source from file: without caption or source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:vtk::
    :include-source: no

    ..

    .. literalinclude:: ../../examples/simple-rectangular-plate.py


Source from file: with both caption and source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:vtk::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. literalinclude:: ../../examples/simple-rectangular-plate.py


Source from file: with caption, source, and notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:vtk::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. literalinclude:: ../../examples/simple-rectangular-plate.py

    Notes may follow the ``literalinclude``.

    :Material: stainless steel
    :Finish: brushed


Options
-------

Default color
~~~~~~~~~~~~~

The :ref:`color option <vtk-option-color>` defines the default color of VTK.js render.

.. cadquery:vtk::
    :name: color-example
    :color: 0.5, 1, 0.8, 1

    Default color set to ``0.5, 1, 0.8, 1``.

    .. code-block:: python

        result = cadquery.Workplane().box(2, 2, 0.5)
