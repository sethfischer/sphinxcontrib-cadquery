"""Sphinx setup."""

import shutil
from pathlib import Path

from sphinx.application import Sphinx

from .cq_core import cq_directive, cq_directive_vtk

__version__ = "0.2.1"

_ROOT_DIR = Path(__file__).absolute().parent

_FILES = {
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

        for filename, metadata in _FILES.items():
            source = _ROOT_DIR / filename
            destination = app_outdir_dist / Path(filename).name

            app.add_js_file(
                str(destination.relative_to(app_static_directory)),
                priority=metadata["priority"],
            )

            shutil.copyfile(source, destination)

        app._sphinxcontrib_cadquery_vtkjs_installed = True

    app.add_directive("cadquery-svg", cq_directive)
    app.add_directive("cadquery-vtk", cq_directive_vtk)

    app.add_directive("cq_plot", cq_directive)  # deprecated, use cadquery-svg
    app.add_directive("cadquery", cq_directive_vtk)  # deprecated, use cadquery-vtk

    app.add_config_value("cadquery_include_source", True, "env")

    return {
        "version": __version__,
    }
