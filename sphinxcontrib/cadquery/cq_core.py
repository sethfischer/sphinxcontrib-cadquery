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

from json import dumps
from pathlib import Path

from cadquery import Assembly, Color, Sketch, cqgi, exporters
from cadquery.occ_impl.assembly import toJSON as cq_assembly_toJSON
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from jinja2 import Environment, PackageLoader, select_autoescape
from sphinx.util import logging

logger = logging.getLogger(__name__)

DEFAULT_COLOR = [1, 0.8, 0, 1]


class Cqgi:
    """Execute source using CQGI."""

    @staticmethod
    def _cqgi_parse(model_source: str):
        """Execute source using CQGI."""
        result = cqgi.parse(model_source).build()

        if not result.success:
            raise result.exception

        return result


class CqSvgDirective(Directive, Cqgi):
    """CadQuery SVG directive."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "align": directives.unchanged,
    }

    def run(self):
        """Generate SVG render of CadQuery model."""
        options = self.options
        content = self.content
        state_machine = self.state_machine
        env = self.state.document.settings.env

        model_source = "\n".join(content)

        try:
            result = self._cqgi_parse(model_source)
        except Exception as err:
            message = f"CQGI error in {self.name} directive: {err}."
            p = nodes.paragraph("", "", nodes.Text(message))
            state_machine.reporter.error(message)
            return [p]

        svg_document = exporters.getSVG(exporters.toCompound(result.first_result.shape))

        jinja_env = Environment(
            loader=PackageLoader("sphinxcontrib.cadquery"),
            autoescape=select_autoescape(),
        )

        rst_markup = jinja_env.get_template("svg.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            source=model_source,
            svg_document=svg_document,
            align=options.get("align", "left"),
        )

        state_machine.insert_input(
            rst_markup.splitlines(), state_machine.input_lines.source(0)
        )

        return []


class CqVtkDirective(Directive, Cqgi):
    """CadQuery VTK directive."""

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        "align": directives.unchanged,
        "height": directives.length_or_unitless,
        "select": directives.unchanged,
        "width": directives.length_or_percentage_or_unitless,
    }

    def run(self):
        """Generate VTK render of CadQuery model."""
        options = self.options
        content = self.content
        state_machine = self.state_machine
        env = self.state.document.settings.env

        if len(self.arguments):
            path_name = Path(env.app.builder.srcdir) / self.arguments[0]
            path_name = path_name.resolve()
            if not path_name.is_file():
                logger.error(f"File does not exist: {path_name}")
            model_source = path_name.read_text()
        else:
            model_source = "\n".join(content)

        try:
            result = self._cqgi_parse(model_source)
        except Exception as err:
            message = f"CQGI error in {self.name} directive: {err}."
            p = nodes.paragraph("", "", nodes.Text(message))
            state_machine.reporter.error(message)
            return [p]

        shape = self._select_shape(result, options.get("select", "result"))
        assembly = self._to_assembly(shape)
        vtk_json = dumps(cq_assembly_toJSON(assembly))

        jinja_env = Environment(
            loader=PackageLoader("sphinxcontrib.cadquery"),
            autoescape=select_autoescape(),
        )

        rst_markup = jinja_env.get_template("vtk.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            source=model_source,
            vtk_json=vtk_json,
            element="document.currentScript.parentNode",
            align=options.get("align", "left"),
            width=options.get("width", "100%"),
            height=options.get("height", "500px"),
        )

        state_machine.insert_input(
            rst_markup.splitlines(), state_machine.input_lines.source(0)
        )

        return []

    @staticmethod
    def _select_shape(result, select: str):
        """Select shape from CQGI environment."""
        if result.first_result:
            return result.first_result.shape

        return result.env[select]

    @staticmethod
    def _to_assembly(shape):
        """Convert shape to assembly."""
        if isinstance(shape, Assembly):
            return shape
        elif isinstance(shape, Sketch):
            return Assembly(shape._faces, color=Color(*DEFAULT_COLOR))

        return Assembly(shape, color=Color(*DEFAULT_COLOR))


class LegacyCqSvgDirective(CqSvgDirective):
    """Legacy SVG directive."""

    def run(self):
        """Deprecate legacy SVG directive."""
        logger.info(
            "use of the cq_plot directive is deprecated, "
            'replace ".. cq_plot::" with ".. cadquery-svg::"'
        )
        return super().run()


class LegacyCqVtkDirective(CqVtkDirective):
    """Legacy VTK directive."""

    def run(self):
        """Deprecate legacy VTK directive."""
        logger.info(
            "direct use of the cadquery directive is deprecated, "
            'replace ".. cadquery::" with ".. cadquery-vtk::"'
        )
        return super().run()
