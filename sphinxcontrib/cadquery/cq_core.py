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

_JINJA_ENV = Environment(
    loader=PackageLoader("sphinxcontrib.cadquery"),
    autoescape=select_autoescape(),
)


class Cqgi:
    """Execute script source using CQGI."""

    @staticmethod
    def _cqgi_parse(script_source: str):
        """Execute script source using CQGI."""
        result = cqgi.parse(script_source).build()

        if not result.success:
            raise result.exception

        return result


class CqSvgDirective(Directive, Cqgi):
    """CadQuery SVG directive."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {}  # type: ignore[var-annotated]

    def run(self):
        """Generate SVG render of CadQuery model."""
        content = self.content
        state_machine = self.state_machine
        env = self.state.document.settings.env

        self.assert_has_content()
        script_source = "\n".join(content)

        try:
            result = self._cqgi_parse(script_source)
        except Exception as err:
            message = f"CQGI error in {self.name} directive: {err}."
            p = nodes.paragraph("", "", nodes.Text(message))
            state_machine.reporter.error(message)
            return [p]

        try:
            compound = exporters.toCompound(result.first_result.shape)
        except AttributeError as err:
            raise self.error(
                f"{err} Does your script source include a call to `show_object()`?"
            )

        svg_document = exporters.getSVG(compound)

        rst_markup = _JINJA_ENV.get_template("svg.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            script_source=script_source,
            svg_document=svg_document,
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
        state_machine = self.state_machine
        env = self.state.document.settings.env

        script_source = self._script_source()

        try:
            result = self._cqgi_parse(script_source)
        except Exception as err:
            message = f"CQGI error in {self.name} directive: {err}."
            p = nodes.paragraph("", "", nodes.Text(message))
            state_machine.reporter.error(message)
            return [p]

        shape = self._select_shape(result, options.get("select", "result"))
        assembly = self._to_assembly(shape)
        vtk_json = dumps(cq_assembly_toJSON(assembly), separators=(",", ":"))

        rst_markup = _JINJA_ENV.get_template("vtk.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            script_source=script_source,
            vtk_json=vtk_json,
            element="document.currentScript.parentNode",
            align=options.get("align", "none"),
            width=options.get("width", "100%"),
            height=options.get("height", "500px"),
        )

        state_machine.insert_input(
            rst_markup.splitlines(), state_machine.input_lines.source(0)
        )

        return []

    def _script_source(self):
        """Get script source."""
        env = self.state.document.settings.env

        if len(self.arguments):
            path_name = Path(env.app.builder.srcdir) / self.arguments[0]
            path_name = path_name.resolve()
            if not path_name.is_file():
                logger.error(f"File does not exist: {path_name}")

            return path_name.read_text()

        if not self.content:
            raise self.error(
                f"{self.name} Expected script source as content"
                " as path name not provided as first argument."
            )

        return "\n".join(self.content)

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
