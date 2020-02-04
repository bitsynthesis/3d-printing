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
    depth = _depth + door_height

    x = _pos[0] + (finger_space / 2)
    y = _pos[1] + (finger_space / 2)
    z = max_depth - _depth

    return pipe(
        cube([length, width, depth]),
        translate([x, y, z]),
    )


# def _skirt(_pos: List[int], _length: int, _width: int):
#     mod = skirt_size - finger_space
#
#     length = _length + mod
#     width = _width + mod
#     height = skirt_height
#
#     x = _pos[0] - (mod / 2)
#     y = _pos[1] - (mod / 2)
#     z = max_depth
#
#     return pipe(
#         cube([length, width, height]),
#         translate([x, y, z]),
#     )


def _roof():
    half_diameter = roof_diameter / 2

    x = half_diameter + roof_offset[0]
    y = half_diameter + roof_offset[1]
    z = door_height + max_depth

    return pipe(
        cylinder(h=roof_height, d=roof_diameter, segments=200),
        translate([x, y, z])
    )


def _foundation():
    length = b_length + b_pos[0] - finger_space
    width = a_pos[1] + a_width - c_pos[1] - finger_space

    x = finger_space / 2
    y = c_pos[1] + (finger_space / 2)

    return pipe(
        cube([length, width, door_height]),
        translate([x, y, max_depth])
    )


def main():
    seg_a = _finger(a_pos, a_length, a_width, a_depth)
    seg_b = _finger(b_pos, b_length, b_width, b_depth)
    seg_c = _finger(c_pos, c_length, c_width, c_depth)

    # skirt_b = _skirt(b_pos, b_length, b_width)

    roof = _roof()

    foundation = _foundation()

    final = seg_a + seg_b + seg_c + roof + foundation

    scad_render_to_file(final, "build/vhs_doorstop.scad")


if __name__ == "__main__":
    main()
