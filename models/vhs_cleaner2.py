from solid import *
from shared.main import *


RES = 200


def _guide_post(base_diameter):
    """
    Create a post for mounting metal guide tube salvaged from a commercial VHS
    tape. Minimum base_diameter is 6 (mm).
    """
    base_height = 1
    foot_height = 2.5
    neck_height = 5.5

    base = pipe(
        cylinder(h=base_height, d=base_diameter, center=True, segments=RES),
        translate([0, 0, base_height / 2])
    )

    foot = pipe(
        cylinder(h=foot_height, d=5, center=True, segments=RES),
        translate([0, 0, (foot_height / 2) + base_height])
    )

    neck = pipe(
        cylinder(h=neck_height, d=4.5, center=True, segments=RES),
        translate([0, 0, (neck_height / 2) + base_height + foot_height])
    )

    return base + foot + neck


def _pad(
    width,
    wing_width,
    tape_height,
    top_tab_height,
    bottom_tab_height,
    thickness,
    tab_thickness
):
    pad_depth = 1

    # bottom tab
    bottom_tab = pipe(
        cube([width, tab_thickness, bottom_tab_height]),
        center(0, width),
        translate([0, pad_depth, 0])
    )

    # bottom tab pad connector
    bottom_tab_pad_connector = pipe(
        cube([width, pad_depth, thickness]),
        center(0, width),
        translate([0, thickness, bottom_tab_height])
    )

    # pad
    pad_height = tape_height + (thickness * 2)
    pad_width = width
    pad = pipe(
        cube([pad_width, thickness, pad_height]),
        center(0, pad_width),
        translate([0, 0, bottom_tab_height])
    )

    # top tab pad connector
    top_tab_pad_connector = pipe(
        cube([width, pad_depth, thickness]),
        center(0, width),
        translate([0, thickness, bottom_tab_height + pad_height - thickness])
    )

    # top tab
    top_tab = pipe(
        cube([width, tab_thickness, top_tab_height]),
        center(0, width),
        translate([0, pad_depth, bottom_tab_height + pad_height])
    )

    # left wing


    # right wing

    return bottom_tab \
            + bottom_tab_pad_connector \
            + pad \
            + top_tab_pad_connector \
            + top_tab


# TODO this works great... except that the bottom doesn't respect the gaps.
# could instead implement the gaps as holes?
def _front_wall(body_width, body_thickness, bottom_height):
    # |                      |
    # | |--|              |-||
    # ---  ---------------- --
    #
    #  123 4       5      6789

    left_gap_offset = 6
    left_gap_width = 10.5
    right_gap_offset = 2.25
    right_gap_width = 4
    gap_depth = 2
    seg5_width = body_width \
            - left_gap_offset \
            - left_gap_width \
            - right_gap_width \
            - right_gap_offset

    # layer 1
    seg1 = cube([left_gap_offset, body_thickness, bottom_height])
    seg5 = cube([seg5_width, body_thickness, bottom_height])
    seg9 = cube([right_gap_offset, body_thickness, bottom_height])

    layer1 = pipe(
        seg9,
        translate([right_gap_width + seg5_width, 0, 0]),
        add(seg5),
        translate([left_gap_width + left_gap_offset, 0, 0]),
        add(seg1),
    )

    # layer 2
    seg2 = cube([body_thickness, gap_depth, bottom_height])
    seg4 = cube([body_thickness, gap_depth, bottom_height])
    seg6 = cube([body_thickness, gap_depth, bottom_height])
    seg8 = cube([body_thickness, gap_depth, bottom_height])

    layer2 = pipe(
        seg8,
        translate([right_gap_width + body_thickness, 0, 0]),
        add(seg6),
        translate([seg5_width - body_thickness, 0, 0]),
        add(seg4),
        translate([left_gap_width + body_thickness, 0, 0]),
        add(seg2),
        translate([left_gap_offset - body_thickness, 0, 0]),
        translate([0, body_thickness, 0]),
    )

    # layer 3
    seg3 = cube([left_gap_width, body_thickness, bottom_height])
    seg7 = cube([right_gap_width, body_thickness, bottom_height])

    layer3 = pipe(
        seg7,
        translate([left_gap_width + seg5_width, 0, 0]),
        add(seg3),
        translate([left_gap_offset, 0, 0]),
        translate([0, gap_depth, 0]),
    )

    return pipe(
        layer1 + layer2 + layer3,
        center(0, body_width),
    )


def main():
    body_width = 188
    body_depth = 104
    body_thickness = 1.25
    body_height = 25
    # body_height = 5
    # body_height = 12.5
    bottom_height = body_height / 2
    top_height = body_height / 2
    tape_plane_height = 16

    spool_hole_diameter = 34
    spool_width = 88.5 + 2 # extra 2 is for amount it can move in the hole
    spool_height = 16.25

    bottom = pipe(
        cube([body_width, body_depth, body_thickness]),
        translate([body_width / -2, 0, 0])
    )

    spool_hole_1 = pipe(
        cylinder(h=10, d=spool_hole_diameter, center=True, segments=RES),
        translate([-46, 56, 0])
    )

    dummy_spool_1 = pipe(
        cylinder(h=spool_height, d=spool_width, center=True, segments=RES),
        translate([-46, 56, spool_height / 2])
    )

    spool_hole_2 = pipe(
        cylinder(h=10, d=spool_hole_diameter, center=True, segments=RES),
        translate([46, 56, 0])
    )

    dummy_spool_2 = pipe(
        cylinder(h=spool_height, d=spool_width, center=True, segments=RES),
        translate([46, 56, spool_height / 2])
    )

    front_wall = _front_wall(body_width, body_thickness, bottom_height)

    back_wall = pipe(
        cube([body_width, body_thickness, bottom_height]),
        translate([body_width / -2, body_depth - body_thickness, 0])
    )

    side_wall_1 = pipe(
        cube([body_thickness, body_depth, bottom_height]),
        translate([body_width / -2, 0, 0])
    )

    side_wall_2 = pipe(
        cube([body_thickness, body_depth, bottom_height]),
        translate([(body_width / 2) - body_thickness, 0, 0])
    )

    guide_post_diameter = 8

    # minus 1 for base overhang
    guide_post_from_front = 3

    # minus 1 for base overhang
    guide_post_from_side = 20

    guide_post_1 = pipe(
        _guide_post(guide_post_diameter),
        translate([
            guide_post_diameter / -2,
            guide_post_diameter / 2,
            body_thickness
        ]),
        translate([
            (body_width / 2) - body_thickness - guide_post_from_side,
            guide_post_from_front + body_thickness,
            0
        ])
    )

    guide_post_2 = pipe(
        _guide_post(guide_post_diameter),
        translate([
            guide_post_diameter / 2,
            guide_post_diameter / 2,
            body_thickness
        ]),
        translate([
            ((body_width / 2) - body_thickness - guide_post_from_side) * -1,
            guide_post_from_front + body_thickness,
            0
        ])
    )

    final_bottom = bottom \
        - spool_hole_1 \
        - spool_hole_2 \
        + front_wall \
        + back_wall \
        + side_wall_1 \
        + side_wall_2 \
        + guide_post_1 \
        + guide_post_2

    final = final_bottom \
        + dummy_spool_1 \
        + dummy_spool_2

    # final = front_wall

    scad_render_to_file(final, "build/vhs_cleaner2.scad")


if __name__ == "__main__":
    main()
