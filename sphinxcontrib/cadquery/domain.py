"""Cadquery domain."""

from base64 import b64encode
from hashlib import sha1
from pathlib import Path
from typing import Optional

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from jinja2 import Environment, PackageLoader, select_autoescape
from sphinx.domains import Domain
from sphinx.util import logging

from .common import DEFAULT_COLOR
from .cqgi import Cqgi, SvgExporter, VtkJsonExporter
from .option_converters import align, rgba, yes_no

logger = logging.getLogger(__name__)

_JINJA_ENV = Environment(
    loader=PackageLoader("sphinxcontrib.cadquery"),
    autoescape=select_autoescape(),
)


def error_node(message: str, detail: str):
    """Error node."""

    node = nodes.paragraph()
    node["classes"].extend(["cadquery-error"])
    node.append(nodes.strong(text=message))
    node.append(nodes.inline(text=detail))

    return node


def set_svg_image_uri(app, doctree):
    """Export SVG images.

    To be called on the Sphinx doctree-read event.
    """

    for img in doctree.traverse(nodes.image):
        if not hasattr(img, "cadquery"):
            continue

        context = img.cadquery["context"]

        try:
            svg_document = export_svg(img.cadquery["source"], img.cadquery["select"])
        except Exception as err:
            error_text = f"CQGI error in {context['name']} directive {err}: "
            detail_text = f"{img.source} on line {context['source_node_line']}."

            logger.error(error_text + detail_text)
            img.replace_self(error_node(error_text, detail_text))

            continue

        if img.cadquery["inline-uri"]:
            svg_bytes = b64encode(svg_document.encode("ascii"))
            img["uri"] = f"data:image/svg+xml;base64,{svg_bytes.decode('ascii')}"
        else:
            output_pathname = (
                Path(app.builder.outdir)
                .joinpath("_static")
                .joinpath("cadquery-exports")
                .joinpath(export_file_name(img.cadquery["source"]))
            )
            output_pathname.parent.mkdir(parents=True, exist_ok=True)

            output_pathname.write_text(svg_document)

            doc_name_absolute = Path(app.srcdir) / Path(app.builder.env.docname)
            doc_depth = len(doc_name_absolute.parent.relative_to(app.srcdir).parts)

            relative_to_document_part = Path("../" * doc_depth)
            uri = relative_to_document_part / output_pathname.relative_to(
                Path(app.builder.outdir)
            )

            img["uri"] = uri.as_posix()


def export_file_name(source: str) -> Path:
    """Create file name for CadQuery export."""
    source_hash = sha1(source.encode()).hexdigest()[:8]

    return Path(source_hash).with_suffix(".svg")


def export_svg(source: str, select: str):
    """Export SVG document."""

    try:
        parser = Cqgi()
        result = parser._cqgi_parse(source)
    except Exception as err:
        raise err

    exporter = SvgExporter(result, select)
    svg_document = exporter()

    return svg_document


class CqDirective(Directive, Cqgi):
    """CadQuery directive parent class."""

    @staticmethod
    def _error_node(message: str, detail: str):
        node = nodes.paragraph()
        node.append(nodes.strong(text=message))
        node.append(nodes.inline(text=detail))

        return node

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

    @staticmethod
    def populate_figure_node(
        figure_node: nodes.Node,
        caption_node: Optional[nodes.Node] = None,
        source_node: Optional[nodes.Node] = None,
        notes_nodes: Optional[nodes.Node] = None,
        *,
        include_source=True,
    ) -> nodes.Node:
        """Populate figure node."""

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

        return figure_node


class CqSvgDirective(CqDirective):
    """CadQuery SVG directive.

    Renders a SVG export wrapped in a HTML figure element.
    """

    required_arguments = 0
    optional_arguments = 0

    option_spec = {
        "align": align,
        "alt": directives.unchanged,
        "figclass": directives.class_option,
        "figwidth": directives.length_or_percentage_or_unitless,
        "include-source": yes_no,
        "inline-uri": directives.flag,
        "name": directives.unchanged,
        "select": directives.unchanged,
    }
    has_content = True

    def run(self):
        """Run."""

        align = self.options.pop("align", None)
        alt = self.options.pop("alt", "SVG image exported by CadQuery.")
        figclasses = self.options.pop("figclass", None)
        figwidth = self.options.pop("figwidth", "100%")
        include_source_value = self.options.pop("include-source", None)

        if "inline-uri" in self.options:
            inline_uri = True
        else:
            inline_uri = False

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

        image_node = nodes.image(source, alt=alt, uri="data:image/svg+xml;")
        image_node["classes"].extend(["cadquery-container-model"])

        if isinstance(image_node, nodes.system_message):
            return [image_node]

        image_node.cadquery = {
            "context": {
                "source_node_line": source_node.line,
            },
            "inline-uri": inline_uri,
            "select": self.options.get("select", "result"),
            "source": source,
        }

        figure_node += image_node

        figure_node = self.populate_figure_node(
            figure_node,
            caption_node,
            source_node,
            notes_nodes,
            include_source=include_source,
        )

        return [figure_node]


class CqVtkDirective(CqDirective):
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

        figure_node = self.populate_figure_node(
            figure_node,
            caption_node,
            source_node,
            notes_nodes,
            include_source=include_source,
        )

        return [figure_node]

    def _vtk_container_node(self, source: str, height: str):
        """VTK.js model container."""

        try:
            result = self._cqgi_parse(source)
        except Exception as err:
            error_text = f"CQGI error in {self.name} directive: "
            detail_text = f"{err}."

            logger.error(error_text + detail_text)

            return [self._error_node(error_text, detail_text)]

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
    """CadQuery Sphinx domain."""

    name = "cadquery"
    label = "CadQuery Sphinx domain"

    directives = {
        "svg": CqSvgDirective,
        "vtk": CqVtkDirective,
    }
