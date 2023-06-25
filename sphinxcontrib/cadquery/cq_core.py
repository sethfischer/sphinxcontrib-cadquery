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

from pathlib import Path
from typing import Any

from cadquery import exporters
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from jinja2 import Environment, PackageLoader, select_autoescape
from sphinx.util import logging

from .common import DEFAULT_COLOR
from .cqgi import Cqgi, VtkJsonExporter
from .option_converters import rgba

logger = logging.getLogger(__name__)

_JINJA_ENV = Environment(
    loader=PackageLoader("sphinxcontrib.cadquery"),
    autoescape=select_autoescape(),
)


class CqSvgDirective(Directive, Cqgi):
    """CadQuery SVG directive."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {}  # type: ignore[var-annotated]

    def run(self) -> list[Any]:
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

        rst_markup = _JINJA_ENV.get_template("cadquery-svg.rst.jinja").render(
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
        "color": rgba,
        "height": directives.length_or_unitless,
        "select": directives.unchanged,
        "width": directives.length_or_percentage_or_unitless,
    }

    def run(self) -> list[Any]:
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

        color = options.get("color", DEFAULT_COLOR)
        vtk_json = VtkJsonExporter(result, options.get("select", "result"))

        rst_markup = _JINJA_ENV.get_template("cadquery-vtk.rst.jinja").render(
            include_source=env.config.cadquery_include_source,
            script_source=script_source,
            vtk_json=vtk_json(color=color),
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


class LegacyCqSvgDirective(CqSvgDirective):
    """Legacy SVG directive."""

    def run(self) -> list[Any]:
        """Deprecate legacy SVG directive."""

        logger.info(
            "use of the cq_plot directive is deprecated, "
            'replace ".. cq_plot::" with ".. cadquery-svg::"'
        )
        return super().run()


class LegacyCqVtkDirective(CqVtkDirective):
    """Legacy VTK directive."""

    def run(self) -> list[Any]:
        """Deprecate legacy VTK directive."""

        logger.info(
            "direct use of the cadquery directive is deprecated, "
            'replace ".. cadquery::" with ".. cadquery-vtk::"'
        )
        return super().run()
