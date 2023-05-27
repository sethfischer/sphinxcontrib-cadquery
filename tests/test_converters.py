"""Test Sphinx option converters."""

import pytest

from sphinxcontrib.cadquery.option_converters import color_channel_value, rgba


class TestSphinxRGBAConverter:
    """Test Sphinx RGBA option converter."""

    def test_comma_seperator(self):
        """Test parsing of comma separated values."""
        result = rgba("0.1, 0.2, 0.3, 1")

        assert [0.1, 0.2, 0.3, 1] == result

    def test_space_seperator(self):
        """Test parsing of space separated values."""
        result = rgba("0.1 0.2 0.3 1")

        assert [0.1, 0.2, 0.3, 1] == result


class TestSphinxColorChannelConverter:
    """Test Sphinx color channel converter."""

    def test_zero(self):
        result = color_channel_value("0")

        assert 0 == result

    def test_one(self):
        result = color_channel_value("1")

        assert 1 == result

    def test_fraction_leading_zero(self):
        result = color_channel_value("0.5")

        assert 0.5 == result

    def test_fraction_no_leading_zero(self):
        result = color_channel_value(".5")

        assert 0.5 == result

    def test_exception_on_value_greater_than_one(self):
        with pytest.raises(ValueError):
            color_channel_value("2")

    def test_exception_on_value_less_than_zero(self):
        with pytest.raises(ValueError):
            color_channel_value("-1")

    def test_exception_on_non_numeric_value(self):
        with pytest.raises(ValueError):
            color_channel_value("a")
