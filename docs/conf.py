"""Sphinx configuration."""

from datetime import date

import sphinx_rtd_theme  # type: ignore[import] # noqa: F401

import sphinxcontrib.cadquery

project = "sphinxcontrib-cadquery"
author = "Seth Fischer"
release = sphinxcontrib.cadquery.__version__
project_copyright = f"{date.today().year}, {author}"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "sphinxcontrib.cadquery",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_context = {
    "display_github": False,
}
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

intersphinx_mapping = {
    "cadquery-latest": ("https://cadquery.readthedocs.io/en/latest/", None),
    "sphinx-master": ("https://www.sphinx-doc.org/en/master/", None),
}


def setup(app):
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
