"""CadQuery CQGI utilities."""

from json import dumps

from cadquery import Assembly, Color, Sketch, cqgi
from cadquery.occ_impl.assembly import toJSON as cq_assembly_toJSON

from .common import DEFAULT_COLOR


class Cqgi:
    """Execute script source using CQGI."""

    @staticmethod
    def _cqgi_parse(script_source: str):
        """Execute script source using CQGI."""
        result = cqgi.parse(script_source).build()

        if not result.success:
            raise result.exception

        return result


class VtkJsonExporter:
    """Export CadQuery assembly as VTK.js JSON."""

    def __init__(self, result, select: str):
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
    def _select_shape(result, select: str):
        """Select shape from CQGI environment."""
        if result.first_result:
            return result.first_result.shape

        return result.env[select]

    @staticmethod
    def _to_assembly(shape, color: list[float]):
        """Convert shape to assembly."""
        if isinstance(shape, Assembly):
            return shape
        elif isinstance(shape, Sketch):
            return Assembly(shape._faces, color=Color(*color))

        return Assembly(shape, color=Color(*color))
