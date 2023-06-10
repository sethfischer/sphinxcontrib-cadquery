"""Cadquery domain."""

from typing import Optional

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from jinja2 import Environment, PackageLoader, select_autoescape
from sphinx.domains import Domain
from sphinx.util import logging

from .common import DEFAULT_COLOR
from .cqgi import Cqgi, VtkJsonExporter
from .option_converters import align, rgba, yes_no

logger = logging.getLogger(__name__)

_JINJA_ENV = Environment(
    loader=PackageLoader("sphinxcontrib.cadquery"),
    autoescape=select_autoescape(),
)


class CqVtkDirective(Directive, Cqgi):
    """CadQuery VTK directive.

    Renders model wrapped in a HTML figure element.
    """

    required_arguments = 0
    optional_arguments = 0

    option_spec = {
        "align": align,
        "color": rgba,
        "figclass": directives.class_option,
        "figwidth": directives.length_or_percentage_or_unitless,
        "height": directives.length_or_percentage_or_unitless,
        "name": directives.unchanged,
        "select": directives.unchanged,
        "include-source": yes_no,
    }
    has_content = True

    def run(self):
        """Run."""

        align = self.options.pop("align", None)
        figclasses = self.options.pop("figclass", None)
        figwidth = self.options.pop("figwidth", "100%")
        height = self.options.pop("height", "500px")
        include_source_value = self.options.pop("include-source", None)

        env = self.state.document.settings.env

        include_source = self._include_source(
            include_source_value, env.config.cadquery_include_source
        )

        caption_node = None
        source_node = None
        notes_nodes = None

        figure_node = nodes.figure()
        self.add_name(figure_node)

        figure_node["classes"].extend(["cadquery-container"])
        figure_node["width"] = figwidth

        if figclasses:
            figure_node["classes"] += figclasses
        if align:
            figure_node["align"] = align

        if self.content:
            node = nodes.Element()  # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)

            if len(node) >= 2:
                if isinstance(node[0], nodes.paragraph):
                    caption_node = node[0]
                elif not isinstance(node[0], nodes.comment):
                    error = self.state_machine.reporter.error(
                        "Model caption must be a paragraph or empty comment.",
                        nodes.literal_block(self.block_text, self.block_text),
                        line=self.lineno,
                    )
                    return [figure_node, error]

                if isinstance(node[1], nodes.literal_block):
                    source_node = node[1]
                    source = node[1].astext()
                else:
                    error = self.state_machine.reporter.error(
                        "Second node must be a code-block or literalinclude.",
                        nodes.literal_block(self.block_text, self.block_text),
                        line=self.lineno,
                    )
                    return [figure_node, error]
            else:
                error = self.state_machine.reporter.error(
                    (
                        f"Directive {self.name} must be composed of 2 or more nodes. "
                        "The first being a caption which is either a paragraph or "
                        "empty comment. "
                        "The second being a either a code-block or a literalinclude."
                    ),
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno,
                )
                return [figure_node, error]

            if len(node) >= 3:
                notes_nodes = node[2:]

        figure_node += self._vtk_container_node(source, height)

        if caption_node:
            caption = nodes.caption(caption_node.rawsource, "", *caption_node.children)
            caption.source = caption_node.source
            caption.line = caption_node.line
            figure_node += caption

        if source_node and include_source:
            figure_node += source_node

        if notes_nodes:
            notes_container = nodes.container()
            notes_container["classes"].extend(["cadquery-notes"])
            notes_container += notes_nodes
            figure_node += notes_container

        return [figure_node]

    @staticmethod
    def _include_source(option_value: Optional[str], config_value: bool) -> bool:
        """Determine if source code listing should be included in output."""
        if option_value == "no":
            include_source = False
        elif option_value == "yes":
            include_source = True
        else:
            include_source = config_value

        return include_source

    def _vtk_container_node(self, source: str, height: str):
        """VTK.js model container."""

        try:
            result = self._cqgi_parse(source)
        except Exception as err:
            error_text = f"CQGI error in {self.name} directive: "
            detail_text = f"{err}."

            logger.error(error_text + detail_text)

            error_node = nodes.paragraph()
            error_node.append(nodes.strong(text=error_text))
            error_node.append(nodes.inline(text=detail_text))

            return [error_node]

        vtk_json = VtkJsonExporter(result, self.options.get("select", "result"))
        color = self.options.get("color", DEFAULT_COLOR)

        script_element = _JINJA_ENV.get_template("vtk-container.html.jinja").render(
            element="document.currentScript.parentNode",
            height=height,
            vtk_json=vtk_json(color=color),
        )
        vtk_script_node = nodes.raw("", script_element, format="html")

        container = nodes.container()
        container["classes"].extend(["cadquery-container-model"])
        container += vtk_script_node

        return container


class CadQueryDomain(Domain):
    name = "cadquery"
    label = "CadQuery Sphinx domain"

    directives = {
        "vtk": CqVtkDirective,
    }
