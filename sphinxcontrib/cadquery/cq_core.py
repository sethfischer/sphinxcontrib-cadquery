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

from cadquery import Assembly, Color, Compound, Sketch, cqgi, exporters
from cadquery.occ_impl.assembly import toJSON
from cadquery.occ_impl.jupyter_tools import DEFAULT_COLOR
from docutils.parsers.rst import Directive, directives
from jinja2 import Environment, PackageLoader, select_autoescape


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

        jinja_env = Environment(
            loader=PackageLoader("sphinxcontrib.cadquery"),
            autoescape=select_autoescape(),
        )

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

        txt_align = "left"
        if "align" in options:
            txt_align = options["align"]

        rst_markup = jinja_env.get_template("svg.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            source=plot_code,
            out_svg=out_svg,
            txt_align=txt_align,
        )

        state_machine.insert_input(
            rst_markup.splitlines(), state_machine.input_lines.source(0)
        )

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

        jinja_env = Environment(
            loader=PackageLoader("sphinxcontrib.cadquery"),
            autoescape=select_autoescape(),
        )

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

        data = dumps(toJSON(assy))

        rst_markup = jinja_env.get_template("vtk.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            source=plot_code,
            data=data,
            element="document.currentScript.parentNode",
            txt_align=options.get("align", "left"),
            width=options.get("width", "100%"),
            height=options.get("height", "500px"),
        )

        state_machine.insert_input(
            rst_markup.splitlines(), state_machine.input_lines.source(0)
        )

        return []
