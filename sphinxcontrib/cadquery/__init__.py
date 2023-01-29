"""Sphinx setup."""

import shutil
from pathlib import Path
from typing import TypedDict

from sphinx.application import Sphinx

from .cq_core import (
    CqSvgDirective,
    CqVtkDirective,
    LegacyCqSvgDirective,
    LegacyCqVtkDirective,
)

__version__ = "0.4.0"

_ROOT_DIR = Path(__file__).absolute().parent

_JS_FILES = {
    "static/dist/vtk-lite.js": {"priority": 90},
    "static/render.js": {"priority": 100},
}


class ExtensionMetadata(TypedDict):
    """The metadata returned by this extension."""

    version: str


def setup(app: Sphinx) -> ExtensionMetadata:
    """Sphinx setup."""
    assets_installed = getattr(app, "_sphinxcontrib_cadquery_assets_installed", False)

    if not assets_installed:
        app_static_directory = Path(app.outdir) / "_static"
        app_outdir_dist = app_static_directory / "dist"
        app_outdir_dist.mkdir(parents=True, exist_ok=True)

        for filename, metadata in _JS_FILES.items():
            js_source = _ROOT_DIR / filename
            js_destination = app_outdir_dist / Path(filename).name

            app.add_js_file(
                str(js_destination.relative_to(app_static_directory)),
                priority=metadata["priority"],
            )

            shutil.copyfile(js_source, js_destination)

        css_destination = app_static_directory / "cadquery.css"
        app.add_css_file(str(css_destination.relative_to(app_static_directory)))
        shutil.copyfile(_ROOT_DIR / "static/cadquery.css", css_destination)

        setattr(app, "_sphinxcontrib_cadquery_assets_installed", True)

    app.add_directive("cadquery-svg", CqSvgDirective)
    app.add_directive("cadquery-vtk", CqVtkDirective)

    app.add_directive("cq_plot", LegacyCqSvgDirective)  # deprecated, use cadquery-svg
    app.add_directive("cadquery", LegacyCqVtkDirective)  # deprecated, use cadquery-vtk

    app.add_config_value("cadquery_include_source", True, "env")

    return {
        "version": __version__,
    }
