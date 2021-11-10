from solid import *
from shared.main import *


panel_thickness = 2.5
panel_thickness = 1.5 # debug

panel_a = 150 - 1
panel_a = 20 # debug

panel_b = 20
panel_c = 17.5 - 1
panel_d = 7 - 1
panel_e = 6 - 1
panel_f = 232.75 - 2
panel_g = 8.25 - 1
panel_h = 67 - 1
panel_i = 147 - 1
panel_j = 226 - 1

hole_width = 3.5
hole_height = 5.5
hole_segments = 32


access_hole_height = 65
access_hole_width = 36


def _screw_hole(x, y):
    """
    Create an oblong screw hole, with x and y representing the left and top.
    """
    a = cylinder(h=panel_thickness, d=hole_width, segments=hole_segments)

    b_center = hole_height - hole_width

    b = pipe(
        cylinder(h=panel_thickness, d=hole_width, segments=hole_segments),
        translate([0, b_center, 0])
    )

    return pipe(
        a + b,
        hull(),
        hole(),
        translate([0, int(b_center / -2), 0]),
        translate([x, y, 0]),
    )


def _left_panel():
    body = cube([panel_a, panel_f, panel_thickness])

    screw_0 = _screw_hole(0, 0)

    screw_1 = _screw_hole(panel_d, panel_g)
    screw_2 = _screw_hole(panel_e, panel_h)
    screw_3 = _screw_hole(panel_e, panel_i)
    screw_4 = _screw_hole(panel_c, panel_j)

    return body + screw_1 + screw_2 + screw_3 + screw_4


def main():
    final = _left_panel()

    #  0      1      2
    #
    #
    # 3               4
    #
    # 5               6
    # 7       8       9

    # hole_0 = screw_hole(14.5, body_height - hole_height - 4)
    # hole_1 = screw_hole(146.5, body_height - hole_height - 4)
    # hole_2 = screw_hole(body_width - hole_width - 14.5, body_height - hole_height - 4)
    # hole_3 = screw_hole(3.75, body_height - 82.75)
    # hole_4 = screw_hole(body_width - hole_width - 3.75, body_height - 82.75)
    # hole_5 = screw_hole(3.75, hole_height + 63.25)
    # hole_6 = screw_hole(body_width - hole_width - 3.75, hole_height + 63.25)
    # hole_7 = screw_hole(3.75, hole_height + 3.75)
    # hole_8 = screw_hole(146.5, hole_height + 3.75)
    # hole_9 = screw_hole(body_width - hole_width - 3.75, hole_height + 3.75)
    #
    # final = body \
    #     + hole_0 \
    #     + hole_1 \
    #     + hole_2 \
    #     + hole_3 \
    #     + hole_4 \
    #     + hole_5 \
    #     + hole_6 \
    #     + hole_7 \
    #     + hole_8 \
    #     + hole_9 \
    #     + access_hole() \
    #     + debug_holes()

    # final = cube([10, 10, 1], center=True) + screw_hole(0, 0)

    scad_render_to_file(final, "build/kaptivator_bottom.scad")


if __name__ == "__main__":
    main()
