"""Sphinx setup."""

import shutil
from pathlib import Path

from sphinx.application import Sphinx

from .cq_core import (
    CqSvgDirective,
    CqVtkDirective,
    LegacyCqSvgDirective,
    LegacyCqVtkDirective,
)

__version__ = "0.3.0"

_ROOT_DIR = Path(__file__).absolute().parent

_JS_FILES = {
    "static/dist/vtk-lite.js": {"priority": 90},
    "static/render.js": {"priority": 100},
}


def setup(app: Sphinx):
    """Sphinx setup."""
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    vtkjs_is_installed = getattr(app, "_sphinxcontrib_cadquery_vtkjs_installed", False)

    if not vtkjs_is_installed:
        app_static_directory = Path(app.outdir) / "_static"
        app_outdir_dist = app_static_directory / "dist"
        app_outdir_dist.mkdir(parents=True, exist_ok=True)

        for filename, metadata in _JS_FILES.items():
            source = _ROOT_DIR / filename
            destination = app_outdir_dist / Path(filename).name

            app.add_js_file(
                str(destination.relative_to(app_static_directory)),
                priority=metadata["priority"],
            )

            shutil.copyfile(source, destination)

        app._sphinxcontrib_cadquery_vtkjs_installed = True

    app.add_directive("cadquery-svg", CqSvgDirective)
    app.add_directive("cadquery-vtk", CqVtkDirective)

    app.add_directive("cq_plot", LegacyCqSvgDirective)  # deprecated, use cadquery-svg
    app.add_directive("cadquery", LegacyCqVtkDirective)  # deprecated, use cadquery-vtk

    app.add_config_value("cadquery_include_source", True, "env")

    return {
        "version": __version__,
    }
