"""Simple rectangular plate."""

import cadquery

result = cadquery.Workplane("front").box(2, 2, 0.5)
