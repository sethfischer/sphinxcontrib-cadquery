=====
Usage
=====

Installation
------------

.. rubric:: Poetry

.. code-block:: console

    poetry add sphinxcontrib-cadquery


.. rubric:: Pip

.. code-block:: console

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


Directives
----------

.. rst:directive:: .. cadquery::

    Render a CadQuery model using `kitware/vtk.js`_.

    Examples:

    .. code-block:: rst

        .. cadquery::

            result = cadquery.Workplane("front").box(2, 2, 0.5)

    .. code-block:: rst

        .. cadquery::
            :height: 100px

            result = cadquery.Workplane("front").box(2, 2, 0.5)

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


.. rst:directive:: .. cq_plot::

    Render a CadQuery model using SVG.

    Examples:

    .. code-block:: rst

        .. cq_plot::

            result = cadquery.Workplane("front").box(2, 2, 0.5)
            show_object(result)

    .. code-block:: rst

        .. cq_plot::
            :align: center

            result = cadquery.Workplane("front").box(2, 2, 0.5)
            show_object(result)

    .. rubric:: Options

    .. rst:directive:option:: align
        :type: left|right|center|justify|initial|inherit (optional, default = "left")

        Alignment of render. Value is used for the CSS ``text-align`` property.


.. _`kitware/vtk.js`: https://kitware.github.io/vtk-js/
