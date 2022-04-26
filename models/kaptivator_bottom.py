from solid import *
from shared.main import *


# panel_thickness = 2.5
panel_thickness = 2.1
# panel_thickness = 1.5 # debug

panel_a = 150 - 1
# panel_a = 20 # debug

panel_b = 20
panel_c = 17.5 - 1
panel_d = 7 - 1
panel_e = 6 - 1
panel_f = 232.75 - 2
panel_g = 8.25 - 1
panel_h = 67 - 1
panel_i = 147 - 1
panel_j = 226 - 1

panel_width = panel_a * 2

hole_width = 3.5
hole_height = 5.5
hole_segments = 32


access_hole_height = 65
access_hole_width = 36












sd_height = 52.75 # actual 52.5
sd_width = 35.75 # actual 35.5
sd_center_thickness = 5.5
sd_side_thickness = 2.5
sd_top_height = 25


sd_total_thickness = 11.5
sd_total_width = 44.25 # actual 44
sd_adapter_side_gap_width = 3.5
sd_adapter_side_gap_thickness = 5


thin_border = sd_adapter_side_gap_width
thick_border = 10


hex_diameter = 5.8 # actual 5.25
hex_height = 6.3 # actual 6
screw_diameter = 3 # actual 2.5


runway_height = 16
runway_width = 30


def _screw_mount():
    hex_hole = cylinder(h=hex_height, d=hex_diameter, segments=6)

    screw_hole = pipe(
        cylinder(h=sd_total_thickness + thin_border, d=screw_diameter, segments=100),
        translate([0, 0, hex_height]),
    )

    return pipe(hex_hole + screw_hole, hole())


def _lid():
    plateau = pipe(
        cube([
            runway_width,
            sd_top_height,
            sd_center_thickness
        ]),
        translate([
            thin_border + sd_total_width - runway_width,
            sd_height + thin_border + runway_height - sd_top_height,
            0
        ])
    )

    cutout = pipe(
        cube([
            runway_width,
            sd_height + runway_height - sd_top_height,
            panel_thickness * 2
        ]),
        translate([
            thin_border + sd_total_width - runway_width,
            thin_border,
            sd_center_thickness
        ]),
        hole()
    )

    return plateau + cutout


def _sd_mount_screws():
    screw = pipe(
        _screw_mount(),
        translate([
            int((thin_border + sd_total_width - sd_width) / 2),
            int((runway_height + thin_border) / 4),
            0
        ])
    )

    top_screw = pipe(
        _screw_mount(),
        translate([
            int((thin_border + sd_total_width + thin_border) - (thick_border / 2)),
            thin_border + sd_height + int(thick_border / 2) + runway_height,
            0
        ])
    )

    return screw + top_screw










def _screw_hole(x, y):
    """
    Create an oblong screw hole, with x and y representing the left and top.
    """
    a = cylinder(h=panel_thickness * 2, d=hole_width, segments=hole_segments)

    b_center = hole_height - hole_width

    b = pipe(
        cylinder(h=panel_thickness * 2, d=hole_width, segments=hole_segments),
        translate([0, b_center, 0])
    )

    return pipe(
        a + b,
        hull(),
        hole(),
        translate([0, int(b_center / -2), 0]),
        translate([x, y, 0]),
    )


def _debug_cutout():
    border = 20

    body = cube([
        (panel_a * 2) - (border * 2),
        panel_f - (border * 2),
        panel_thickness * 2,
    ])

    return pipe(
        body,
        translate([border, border, 0]),
        hole(),
    )


def _left_panel():
    body = cube([panel_a - right_offset, panel_f, panel_thickness])

    screw_1 = _screw_hole(panel_d, panel_g)
    screw_2 = _screw_hole(panel_e, panel_h)
    screw_3 = _screw_hole(panel_e, panel_i)
    screw_4 = _screw_hole(panel_c, panel_j)

    return body + screw_1 + screw_2 + screw_3 + screw_4


# TODO
right_overlap = 10
right_offset = 10
right_width = panel_a + right_overlap + right_offset


def _right_panel():
    body = cube([
        right_width,
        panel_f,
        panel_thickness * 2
    ])

    body += _screw_hole(right_width - panel_c, panel_g)
    body += _screw_hole(right_width - panel_e, panel_h)
    body += _screw_hole(right_width - panel_e, panel_i)
    body += _screw_hole(right_width - panel_c, panel_j)
    body += _screw_hole(right_overlap + right_offset, panel_g)
    body += _screw_hole(right_overlap + right_offset, panel_j)

    sd_mount_elements = pipe(
        _lid() - pipe(_sd_mount_screws(), translate([0, 0, hex_height * -1])),
        translate([149, 39, sd_center_thickness * -1])
    )

    return pipe(
        body,
        translate([panel_a - right_overlap - right_offset, 0, 0]),
        color("purple")
    ) - _left_panel() +  sd_mount_elements


def main():
    final = _left_panel() + _right_panel() # + _debug_cutout()

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

    final_left = pipe(
        _left_panel(),
        rotate([180, 0, 0]),
        translate([0, 0, panel_thickness]),
    )
    scad_render_to_file(final_left, "build/kaptivator_bottom_left.scad")

    final_right = pipe(
        _right_panel(),
        rotate([180, 0, 0]),
        translate([0, 0, panel_thickness * 2]),
    )
    scad_render_to_file(final_right, "build/kaptivator_bottom_right.scad")


if __name__ == "__main__":
    main()
