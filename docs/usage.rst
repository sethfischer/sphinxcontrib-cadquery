=====
Usage
=====

Installation
------------

.. rubric:: Poetry

.. code-block:: text

    poetry add sphinxcontrib-cadquery


.. rubric:: Pip

.. code-block:: text

    pip install sphinxcontrib-cadquery


.. note::

    It is not possible to install *sphinxcontrib-cadquery* from VCS i.e.
    ``python -m pip install git+https://github.com/…``, or
    ``poetry add git+https://github.com/…`` as this circumvents the :doc:`build
    process<build>`.


Configuration
-------------

Enable the extension in your Sphinx ``conf.py`` file:

.. code-block:: python

    extensions = [
        "sphinxcontrib.cadquery",
    ]


.. _usage-directives:

Directives
----------

.. rst:directive:: .. cadquery-vtk::

    Render a CadQuery model using `kitware/vtk.js`_.

    Examples:

    .. code-block:: rst

        .. cadquery-vtk::

            result = cadquery.Workplane("front").box(2, 2, 0.5)

    .. code-block:: rst

        .. cadquery-vtk::
            :height: 100px

            result = cadquery.Workplane("front").box(2, 2, 0.5)

    The VTK JavaScript is generated using the :doc:`CadQuery Gateway Interface <cadquery:cqgi>`
    and :func:`cadquery.occ_impl.assembly.toJSON` [`source`_].

    .. versionadded:: 0.1.2
        Identical to depreciated :rst:dir:`cadquery` directive.

    .. rubric:: Options

    .. rst:directive:option:: align
        :type: left|right|center|justify|initial|inherit (optional, default = "left")

        Alignment of render. Value is used for the CSS ``text-align`` property.

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

    Examples:

    .. code-block:: rst

        .. cadquery-svg::

            result = cadquery.Workplane("front").box(2, 2, 0.5)
            show_object(result)

    .. code-block:: rst

        .. cadquery-svg::
            :align: center

            result = cadquery.Workplane("front").box(2, 2, 0.5)
            show_object(result)

    The SVG image is generated using the :doc:`CadQuery Gateway Interface <cadquery:cqgi>`
    and the :doc:`CadQuery SVG exporter <cadquery:importexport>` .

    .. versionadded:: 0.1.2
      Identical to depreciated :rst:dir:`cq_plot` directive.

    .. rubric:: Options

    .. rst:directive:option:: align
        :type: left|right|center|justify|initial|inherit (optional, default = "left")

        Alignment of render. Value is used for the CSS ``text-align`` property.


.. rst:directive:: .. cadquery::

    .. deprecated:: 0.1.1
       Use the :rst:dir:`cadquery-vtk` directive instead.


.. rst:directive:: .. cq_plot::

    .. deprecated:: 0.1.1
       Use the :rst:dir:`cadquery-svg` directive instead.


.. _`kitware/vtk.js`: https://kitware.github.io/vtk-js/
.. _`source`: https://cadquery.readthedocs.io/en/latest/_modules/cadquery/occ_impl/assembly.html
