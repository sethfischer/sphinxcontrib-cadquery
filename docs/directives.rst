==========
Directives
==========

.. rst:directive:: .. cadquery-vtk:: [path_name]

    Aliases
        :cadquery: Provides compatibility with the CadQuery core directive.

    Render a CadQuery model using `kitware/vtk.js`_.

    The *path_name* argument is a path to a CadQuery source file,
    relative to the Sphinx content root.

    .. rubric:: Examples

    .. code-block:: rst
        :caption: Default is to render the "result" object.

        .. cadquery-vtk::

            result = cadquery.Workplane().box(2, 2, 0.5)

    .. code-block:: rst
        :caption: Set the height of the VTK.js render window.

        .. cadquery-vtk::
            :height: 100px

            result = cadquery.Workplane().box(2, 2, 0.5)

    .. code-block:: rst
        :caption: Load CadQuery source code from a file.

        .. cadquery-vtk:: ../examples/simple-rectangular-plate.py

    VTK JavaScript is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and :func:`cadquery-latest:cadquery.occ_impl.assembly.toJSON`.

    .. versionadded:: 0.2.0
        Identical to depreciated :rst:dir:`cadquery` directive.

    .. rubric:: Options

    .. rst:directive:option:: align
        :type: left|center|right (optional, default = none)

        Horizontal alignment of render.

    .. rst:directive:option:: color
        :type: list of RGBA values (optional, default = 1, 0.8, 0, 1)

        Default color of render in RGBA notation.
        Defined as a space- or comma-separated list of channel values between ``0`` and ``1``.

    .. rst:directive:option:: height
        :type: length or unitless (optional, default = 500px)

        Define the height of VTK.js render window.
        Value is used for the CSS ``height`` property.

    .. rst:directive:option:: select
        :type: name of shape to render (optional, default = result)

        Select the CadQuery object to render.

    .. rst:directive:option:: width
        :type: length or percentage or unitless (optional, default = 100%)

        Define the width of the VTK.js render window.
        Value is used for the CSS ``width`` property.


.. rst:directive:: .. cadquery-svg::

    Aliases
        :cq_plot: Provides compatibility with the CadQuery core directive.

    Render a CadQuery model using SVG.

    .. tip::

        The CadQuery source must call
        :meth:`show_object() <cadquery-latest:cadquery.cqgi.ScriptCallback.show_object>`.

    .. rubric:: Examples

    .. code-block:: rst
        :caption: Render the object passed to "show_object()" as a SVG image.

        .. cadquery-svg::

            result = cadquery.Workplane().box(2, 2, 0.5)
            show_object(result)

    The SVG image is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and the :doc:`CadQuery SVG exporter <cadquery-latest:importexport>` .

    .. versionadded:: 0.2.0
      Identical to depreciated :rst:dir:`cq_plot` directive.


.. rst:directive:: .. cadquery:vtk::

    Render a CadQuery model using `kitware/vtk.js`_.
    Differs from :rst:dir:`cadquery-vtk` in that it is rendered as a figure node.

    .. include:: includes/status-pre-alpha.rst

    A **cadquery:vtk** directive consists of:

    #. A paragraph to be used as the caption (or empty comment to omit a caption), and;
    #. a :rst:dir:`sphinx-master:code-block` or :rst:dir:`sphinx-master:literalinclude`
       from which the source is extracted to render the model, and;
    #. optional additional content that follows will be used as notes.

    There must be a blank line before each of the caption, paragraph, and code block.
    If notes are included then they must separated from the code block by a blank line.
    To specify an empty caption, use an empty comment ("..") in place of the caption.

    Refer to the :doc:`cadquery:vtk examples section <examples/vtk>` for demonstrations of the various options.

    VTK JavaScript is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and :func:`cadquery-latest:cadquery.occ_impl.assembly.toJSON`.

    .. versionadded:: 0.8.0

    .. rubric:: Examples

    .. code-block:: rst
        :caption: Code block: with caption, source, and notes

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

    .. code-block:: rst
        :caption: Code block: without caption or source

        .. cadquery:vtk::
            :include-source: no

            ..

            .. code-block:: python

                """Simple rectangular plate."""

                import cadquery as cq

                result = cadquery.Workplane().box(2, 2, 0.5)


    .. code-block:: rst
        :caption: Source from file: with caption, source, and notes

        .. cadquery:vtk::

            A simple rectangular plate measuring 2 × 2 × 0.5 mm.

            .. literalinclude:: ../../examples/simple-rectangular-plate.py

            Notes may follow the ``literalinclude``.

            :Material: stainless steel
            :Finish: brushed


    .. rubric:: Options

    .. rst:directive:option:: name
        :type: a label for hyperlink (optional)

        Define an implicit target name that can be referenced using ``:ref:`label-name```.

    .. rst:directive:option:: align
        :type: left|center|right (optional, default = none)

        Horizontal alignment of figure element.

    .. _vtk-option-color:

    .. rst:directive:option:: color
        :type: list of RGBA values (optional, default = 1, 0.8, 0, 1)

        Default color of render in RGBA notation.
        Defined as a space- or comma-separated list of channel values between ``0`` and ``1``.

    .. rst:directive:option:: figclass
        :type: space separated list of class names (optional)

        Add classes to the figure element.

    .. rst:directive:option:: figwidth
        :type: length or percentage or unitless (optional, default = 100%)

        Define the width of the figure element.
        Value is used for the CSS ``width`` property.

    .. rst:directive:option:: height
        :type: length or unitless (optional, default = 500px)

        Define the height of VTK.js render window.
        Value is used for the CSS ``height`` property.

    .. rst:directive:option:: select
        :type: name of shape to render (optional, default = result)

        Select the CadQuery object to render.

    .. rst:directive:option:: include-source
        :type: yes|no (optional)

        Whether to include CadQuery source code listing.
        Defaults to :confval:`cadquery_include_source`.


.. _`kitware/vtk.js`: https://kitware.github.io/vtk-js/
