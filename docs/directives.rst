==========
Directives
==========

.. rst:directive:: .. cadquery-vtk:: [path_name]

    Render a CadQuery model using `kitware/vtk.js`_.

    VTK JavaScript is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and :func:`cadquery-latest:cadquery.occ_impl.assembly.toJSON`.

    The *path_name* argument is a path to a CadQuery source file,
    relative to the Sphinx content root.

    Examples:

    .. code-block:: rst

        .. cadquery-vtk::

            result = cadquery.Workplane("front").box(2, 2, 0.5)

    .. code-block:: rst

        .. cadquery-vtk::
            :height: 100px

            result = cadquery.Workplane("front").box(2, 2, 0.5)

    .. code-block:: rst

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

    Render a CadQuery model using SVG.

    .. tip::

        The CadQuery source must call
        :meth:`show_object() <cadquery-latest:cadquery.cqgi.ScriptCallback.show_object>`.

    Examples:

    .. code-block:: rst

        .. cadquery-svg::

            result = cadquery.Workplane("front").box(2, 2, 0.5)
            show_object(result)

    The SVG image is generated using the :doc:`CadQuery Gateway Interface <cadquery-latest:cqgi>`
    and the :doc:`CadQuery SVG exporter <cadquery-latest:importexport>` .

    .. versionadded:: 0.2.0
      Identical to depreciated :rst:dir:`cq_plot` directive.


.. rst:directive:: .. cadquery::

    Alias for :rst:dir:`cadquery-vtk`.
    Provides compatibility with the CadQuery core directive.

    .. deprecated:: 0.2.0
       Use the :rst:dir:`cadquery-vtk` directive instead.


.. rst:directive:: .. cq_plot::

    Alias for :rst:dir:`cadquery-svg`.
    Provides compatibility with the CadQuery core directive.

    .. deprecated:: 0.2.0
       Use the :rst:dir:`cadquery-svg` directive instead.


.. _`kitware/vtk.js`: https://kitware.github.io/vtk-js/
