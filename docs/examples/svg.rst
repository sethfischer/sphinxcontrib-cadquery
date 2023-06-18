============
cadquery:svg
============

Examples of the :rst:dir:`cadquery:svg` directive.

.. include:: ../includes/status-pre-alpha.rst

:rst:dir:`cadquery:svg` is based on the docutils "figure" directive having similar features and syntax:

* The image may be captioned.
* Notes may be added below the code block.
* Images may be referenced by name: :ref:`include from file example <example-svg-include-from-file>`.

The image source code is defined in either a :rst:dir:`sphinx-master:code-block` or
:rst:dir:`sphinx-master:literalinclude`, meaning:

* All options for :rst:dir:`sphinx-master:code-block` or :rst:dir:`sphinx-master:literalinclude`
  may be used such as :rst:dir:`sphinx-master:code-block:linenos` and :rst:dir:`sphinx-master:code-block:emphasize-lines`.
* Image source code blocks may be referenced by name: :ref:`CadQuery source code for a rectangular plate <example-svg-rectangular-plate-code>`.

.. include:: ../includes/tip-view-source.rst


Simple rectangular plate
------------------------

.. cadquery:svg::
    :alt: A rectangular plate

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. code-block:: python
        :name: example-svg-rectangular-plate-code
        :linenos:
        :emphasize-lines: 5

        """Simple rectangular plate."""

        import cadquery as cq

        result = cadquery.Workplane().box(2, 2, 0.5)

    .. rubric:: Notes:

    #. Line numbers are added with ``linenos``.
    #. Line number 5 is emphasized with ``emphasize-lines``.


Pillow block
------------

.. cadquery:svg::

    A pillow block.

    .. code-block:: python

        (length, height, diam, thickness, padding) = (30.0, 40.0, 22.0, 10.0, 8.0)

        pillow_block = (
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

        show_object(pillow_block)


Source from file
----------------

.. cadquery:svg::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. literalinclude:: ../../examples/simple-rectangular-plate.py


Content variations
------------------

Code block: without caption or source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:svg::
    :include-source: no

    ..

    .. code-block:: python

        """Simple rectangular plate."""

        import cadquery as cq

        result = cadquery.Workplane().box(2, 2, 0.5)


Code block: with both caption and source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:svg::
    :select: plate

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. code-block:: python

        """Simple rectangular plate."""

        import cadquery as cq

        plate = cadquery.Workplane().box(2, 2, 0.5)


Code block: with caption, source, and notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:svg::

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

.. cadquery:svg::
    :include-source: no

    ..

    .. literalinclude:: ../../examples/simple-rectangular-plate.py


Source from file: with both caption and source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:svg::

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. literalinclude:: ../../examples/simple-rectangular-plate.py


Source from file: with caption, source, and notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. cadquery:svg::
    :name: example-svg-include-from-file

    A simple rectangular plate measuring 2 × 2 × 0.5 mm.

    .. literalinclude:: ../../examples/simple-rectangular-plate.py

    Notes may follow the ``literalinclude``.

    :Material: stainless steel
    :Finish: brushed
