"""Sphinx option conversion functions."""

from docutils.parsers.rst import directives


def horizontal_align(argument):
    """Sphinx directive align option."""

    return directives.choice(argument, ("left", "center", "right"))


def yes_no(argument):
    """Sphinx directive yes/no option."""

    return directives.choice(argument, ("yes", "no"))


def color_channel_value(argument):
    """Converts the argument into a float.

    Validates that argument is from 0 to 1, with any fractional value in between.
    """

    value = float(argument)
    if value < 0 or value > 1:
        raise ValueError(
            "invalid value; "
            "must be from 0 to 1, with any fractional value in between"
        )
    return value


def rgba(argument):
    """Convert an RGBA quadruplet to a Python list.

    Color in RGBA notation defined as a space- or comma-separated list of channel
    values.
    """

    if "," in argument:
        entries = argument.split(",")
    else:
        entries = argument.split()

    if len(entries) != 4:
        raise ValueError("invalid value; RGBA color must consist of 4 values")

    return [color_channel_value(entry) for entry in entries]
