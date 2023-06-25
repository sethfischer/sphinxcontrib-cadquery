"""CadQuery CQGI utilities."""

from json import dumps

from cadquery import Assembly, Color, Shape, Sketch, exporters
from cadquery.cqgi import BuildResult  # type: ignore[attr-defined]
from cadquery.cqgi import parse as cqgi_parse  # type: ignore[attr-defined]
from cadquery.occ_impl.assembly import toJSON as cq_assembly_toJSON

from .common import DEFAULT_COLOR


class Cqgi:
    """Execute script source using CQGI."""

    @staticmethod
    def cqgi_parse(script_source: str) -> BuildResult:
        """Execute script source using CQGI."""

        result = cqgi_parse(script_source).build()

        if not result.success:
            raise result.exception

        return result


class Exporter:
    """Exporter base class."""

    @staticmethod
    def _select_shape(result: BuildResult, select: str):
        """Select shape from CQGI environment."""

        if result.first_result:
            return result.first_result.shape

        return result.env[select]


class VtkJsonExporter(Exporter):
    """Export CadQuery assembly as VTK.js JSON."""

    def __init__(self, result: BuildResult, select: str):
        self.result = result
        self.select = select

    def __call__(self, *, color=None):
        """Export CadQuery assembly as VTK.js JSON."""

        if color is None:
            color = DEFAULT_COLOR

        shape = self._select_shape(self.result, self.select)
        assembly = self._to_assembly(shape, color=color)
        vtk_json = dumps(cq_assembly_toJSON(assembly), separators=(",", ":"))

        return vtk_json

    @staticmethod
    def _to_assembly(shape: Shape, color: list[float]) -> Assembly:
        """Convert shape to assembly."""

        if isinstance(shape, Assembly):
            return shape
        elif isinstance(shape, Sketch):
            return Assembly(shape._faces, color=Color(*color))

        return Assembly(shape, color=Color(*color))


class SvgExporter(Exporter):
    """Export CadQuery object as SVG."""

    def __init__(self, result: BuildResult, select: str) -> None:
        """
        Initialise exporter.

        :param result: CQGI result
        :param select: name of object to select from CQGI result
        """

        self.result = result
        self.select = select

    def __call__(self) -> str:
        """Export CadQuery object as SVG."""

        shape = self._select_shape(self.result, self.select)
        compound = exporters.toCompound(shape)

        return exporters.getSVG(compound)
