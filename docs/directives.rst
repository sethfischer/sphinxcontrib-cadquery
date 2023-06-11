==========
Directives
==========

.. rst:directive:: .. cadquery-vtk:: [path_name]

    .. rubric:: Aliases

    **.. cadquery::**
        Provides compatibility with the CadQuery core directive.

    Render a CadQuery model using `kitware/vtk.js`_.

    VTK JavaScript is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and :func:`cadquery-latest:cadquery.occ_impl.assembly.toJSON`.

    The *path_name* argument is a path to a CadQuery source file,
    relative to the Sphinx content root.

    Examples:

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


    .. versionadded:: 0.2.0
        Identical to depreciated :rst:dir:`cadquery` directive.

    .. rubric:: Options

    .. rst:directive:option:: align
        :type: left|right|center|none (optional, default = "none")

        Alignment of render.

    .. rst:directive:option:: color
        :type: list of RGBA values (optional)

        Default color of render in RGBA notation.
        Defined as a space- or comma-separated list of channel values between ``0`` and ``1``.

    .. rst:directive:option:: height
        :type: length or unitless (optional, default = 500px)

        Height of render. Value is used for the CSS ``height`` property.

    .. rst:directive:option:: select
        :type: name of shape to render (optional, default = result)

        CadQuery object to render.

    .. rst:directive:option:: width
        :type: length or percentage or unitless (optional, default = 100%)

        Width of render.  Value is used for the CSS ``width`` property.


.. rst:directive:: .. cadquery-svg::

    .. rubric:: Aliases

    **.. cq_plot:**
        Provides compatibility with the CadQuery core directive.

    Render a CadQuery model using SVG.

    .. tip::

        The CadQuery source must call
        :meth:`show_object() <cadquery-latest:cadquery.cqgi.ScriptCallback.show_object>`.

    Examples:

    .. code-block:: rst
        :caption: Render the object passed to "show_object()" as a SVG image.

        .. cadquery-svg::

            result = cadquery.Workplane().box(2, 2, 0.5)
            show_object(result)

    The SVG image is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and the :doc:`CadQuery SVG exporter <cadquery-latest:importexport>` .

    .. versionadded:: 0.2.0
      Identical to depreciated :rst:dir:`cq_plot` directive.


.. _`kitware/vtk.js`: https://kitware.github.io/vtk-js/
