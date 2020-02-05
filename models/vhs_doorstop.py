from solid import *
from typing import List

from shared.main import *


#       ___
#       | |
# ____  |B|
# |  |  ---
# |A |  ____
# ----  |C |
#  D    ----


case_thickness = 2
max_depth = 3
finger_space = 1
door_height = 3.5

roof_height = 4
roof_diameter = 20
roof_offset = [-4, -2.25]

skirt_size = 4
skirt_height = 0.5

a_pos = [0, 5]
a_length = 4.25
a_width = 6.25
a_depth = 2.5

b_pos = [8.5, 9.25]
b_length = 3.5
b_width = 5.25
b_depth = 2.5

c_pos = [7.6, 2]
c_length = 5
c_width = 4.5
c_depth = 2.5


def _finger(_pos: List[int], _length: int, _width: int, _depth: int):
    length = _length - finger_space
    width = _width - finger_space
    depth = _depth

    x = _pos[0] + (finger_space / 2)
    y = _pos[1] + (finger_space / 2)
    z = max_depth - _depth

    return pipe(
        cube([length, width, depth]),
        translate([x, y, z]),
    )


def _roof():
    half_diameter = roof_diameter / 2

    x = half_diameter + roof_offset[0]
    y = half_diameter + roof_offset[1]
    z = door_height + max_depth

    return pipe(
        cylinder(h=roof_height, d=roof_diameter, segments=200),
        translate([x, y, z])
    )


def _clear_left():
    return pipe(
        cube([50, 50, max_depth + door_height]),
        hole(),
        translate([-50 + (finger_space / 2), -25, 0])
    )


def _foundation():
    skirt_diameter = roof_diameter - 3
    half_diameter = skirt_diameter / 2
    edge_height = 0.35

    x = (roof_diameter / 2) + roof_offset[0]
    y = (roof_diameter / 2) + roof_offset[1]

    core = cylinder(h=door_height + roof_height, d=12, segments=200),

    skirt = pipe(
        cylinder(h=door_height + roof_height, r1=half_diameter, r2=2, segments=200),
        translate([0, 0, edge_height])
    )

    edge = cylinder(h=edge_height, d=skirt_diameter, segments=200),

    return pipe(skirt + edge, translate([x, y, max_depth]))


def main():
    seg_a = _finger(a_pos, a_length, a_width, a_depth)
    seg_b = _finger(b_pos, b_length, b_width, b_depth)
    seg_c = _finger(c_pos, c_length, c_width, c_depth)

    roof = _roof()

    foundation = _foundation()

    final = pipe(
        seg_a + seg_b + seg_c + roof + foundation + _clear_left(),
        translate([roof_offset[0] * -1,roof_offset[1] * -1, 0]),
        rotate([180, 0, 0]),
        translate([0, 0, max_depth + door_height + roof_height])
    )

    scad_render_to_file(final, "build/vhs_doorstop.scad")


if __name__ == "__main__":
    main()
