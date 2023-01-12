"""
Directives from CadQuery core.
https://github.com/CadQuery/cadquery

SPDX-License-Identifier: Apache-2.0
SPDX-FileCopyrightText: Copyright 2015 Parametric Products Intellectual Holdings, LLC

SPDX-FileContributor: Adam Urbańczyk <adam.jan.urbanczyk@gmail.com>
SPDX-FileContributor: Dave Cowden <dave.cowden@gmail.com>
SPDX-FileContributor: Marcus Boyd <mwb@geosol.com.au>
SPDX-FileContributor: Miguel Sánchez de León Peque <peque@neosit.es>
SPDX-FileContributor: Seth Fischer <seth@fischer.nz>
"""

import traceback
from json import dumps
from textwrap import indent

from cadquery import Assembly, Color, Compound, Sketch, cqgi, exporters
from cadquery.occ_impl.assembly import toJSON
from cadquery.occ_impl.jupyter_tools import DEFAULT_COLOR, TEMPLATE_RENDER
from docutils.parsers.rst import Directive, directives

template = """

.. raw:: html

    <div class="cq" style="text-align:%(txt_align)s;float:left;">
        %(out_svg)s
    </div>
    <div style="clear:both;">
    </div>

"""

template_vtk = """

.. raw:: html

    <div class="cq-vtk"
     style="text-align:{txt_align};float:left;border: 1px solid #ddd; width:{width}; height:{height}">
       <script>
       var parent_element = {element};
       var data = {data};
       render(data, parent_element);
       </script>
    </div>
    <div style="clear:both;">
    </div>

"""


class cq_directive(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 2
    option_spec = {
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "align": directives.unchanged,
    }

    def run(self):
        options = self.options
        content = self.content
        state_machine = self.state_machine
        env = self.state.document.settings.env

        # only consider inline snippets
        plot_code = "\n".join(content)

        # Since we don't have a filename, use a hash based on the content
        # the script must define a variable called 'out', which is expected to
        # be a CQ object
        out_svg = "Your Script Did not assign call build_output() function!"

        try:
            result = cqgi.parse(plot_code).build()
            if result.success:
                out_svg = exporters.getSVG(
                    exporters.toCompound(result.first_result.shape)
                )
            else:
                raise result.exception

        except Exception:
            traceback.print_exc()
            out_svg = traceback.format_exc()

        # Now start generating the lines of output
        lines = []

        # get rid of new lines
        out_svg = out_svg.replace("\n", "")

        txt_align = "left"
        if "align" in options:
            txt_align = options["align"]

        lines.extend((template % locals()).split("\n"))

        if env.config.cadquery_include_source:
            lines.extend(["::", ""])
            lines.extend(["    %s" % row.rstrip() for row in plot_code.split("\n")])
            lines.append("")

        if len(lines):
            state_machine.insert_input(lines, state_machine.input_lines.source(0))

        return []


class cq_directive_vtk(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 2
    option_spec = {
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "align": directives.unchanged,
        "select": directives.unchanged,
    }

    def run(self):

        options = self.options
        content = self.content
        state_machine = self.state_machine
        env = self.state.document.settings.env

        # only consider inline snippets
        plot_code = "\n".join(content)

        # collect the result
        try:
            result = cqgi.parse(plot_code).build()

            if result.success:
                if result.first_result:
                    shape = result.first_result.shape
                else:
                    shape = result.env[options.get("select", "result")]

                if isinstance(shape, Assembly):
                    assy = shape
                elif isinstance(shape, Sketch):
                    assy = Assembly(shape._faces, color=Color(*DEFAULT_COLOR))
                else:
                    assy = Assembly(shape, color=Color(*DEFAULT_COLOR))
            else:
                raise result.exception

        except Exception:
            traceback.print_exc()
            assy = Assembly(Compound.makeText("CQGI error", 10, 5))

        # add the output
        lines = []

        data = dumps(toJSON(assy))

        lines.extend(
            template_vtk.format(
                code=indent(TEMPLATE_RENDER.format(), "    "),
                data=data,
                ratio="null",
                element="document.currentScript.parentNode",
                txt_align=options.get("align", "left"),
                width=options.get("width", "100%"),
                height=options.get("height", "500px"),
            ).splitlines()
        )

        if env.config.cadquery_include_source:
            lines.extend(["::", ""])
            lines.extend(["    %s" % row.rstrip() for row in plot_code.split("\n")])
            lines.append("")

        if len(lines):
            state_machine.insert_input(lines, state_machine.input_lines.source(0))

        return []
