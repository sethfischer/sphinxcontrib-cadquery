"""CadQuery CQGI utilities."""

from cadquery import cqgi


class Cqgi:
    """Execute script source using CQGI."""

    @staticmethod
    def _cqgi_parse(script_source: str):
        """Execute script source using CQGI."""
        result = cqgi.parse(script_source).build()

        if not result.success:
            raise result.exception

        return result
