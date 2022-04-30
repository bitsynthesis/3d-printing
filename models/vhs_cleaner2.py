import math

from solid import *

from shared.main import *


RES = 200
PAD_COLOR = "#00FF00"
DUMMY_COLOR = "#FF0000"


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
        translate([0, 0, base_height / 2]),
    )

    foot = pipe(
        cylinder(h=foot_height, d=5, center=True, segments=RES),
        translate([0, 0, (foot_height / 2) + base_height]),
    )

    neck = pipe(
        cylinder(h=neck_height, d=4.5, center=True, segments=RES),
        translate([0, 0, (neck_height / 2) + base_height + foot_height]),
    )

    return base + foot + neck


# TODO this works great... except that the bottom doesn't respect the gaps.
# could instead implement the gaps as holes?
def _front_wall(body_width, body_thickness, bottom_height):
    # |                      |
    # | |--|              |-||
    # ---  ---------------- --
    #
    #  a  b        c       d e

    # ------              ----
    # |    |              |  |
    # ------------------------
    #
    # plus gap holes

    a_width = 6
    b_width = 10.5
    d_width = 4
    e_width = 2.25
    c_width = body_width - a_width - b_width - d_width - e_width

    gap_depth = 2

    left_wall = cube(
        [a_width + b_width + body_thickness, gap_depth + body_thickness, bottom_height]
    )

    left_gap = pipe(
        cube([b_width, gap_depth, bottom_height]), translate([a_width, 0, 0]), hole()
    )

    middle_wall = cube([c_width, body_thickness, bottom_height])
    # translate([a_width + b_width, 0, 0])

    right_wall = cube(
        [d_width + e_width + body_thickness, gap_depth + body_thickness, bottom_height]
    )

    right_gap = pipe(
        cube([d_width, gap_depth, bottom_height]),
        translate([body_thickness, 0, 0]),
        hole(),
    )

    result = pipe(
        right_wall,
        add(right_gap),
        translate([c_width - body_thickness, 0, 0]),
        add(middle_wall),
        translate([a_width + b_width, 0, 0]),
        add(left_wall),
        add(left_gap),
    )

    return pipe(result, center(0, body_width))


# TODO use cylinders instead of cubes for rounded edges
def _pad(pad_width, body_thickness, body_height, pad_depth, is_gap=False):
    pad_height = body_height - (body_thickness * 2)
    leg_width = 14

    if is_gap:
        body_thickness += 0.4
        pad_depth += 0.4
        pad_width += -0.4
        leg_width += 0.4

    leg_depth = pad_depth - body_thickness

    # diagonal = body_thickness * math.sqrt(2)
    # leg_offset = diagonal + 0.2

    leg_1a = pipe(
        cube([body_thickness, leg_depth, pad_height]),
        translate([leg_width - body_thickness, 0, 0]),
    )
    leg_1b = pipe(
        cube([leg_width, body_thickness, pad_height]),
        translate([0, leg_depth, 0]),
    )

    leg_1 = pipe(
        leg_1a + leg_1b,
        translate([(pad_width / 2) - leg_width, 0, 0]),
    )

    leg_2 = pipe(leg_1.copy(), mirror([1, 0, 0]))

    middle = pipe(cube([pad_width, body_thickness, pad_height]), center(0, pad_width))

    return leg_1 + middle  + leg_2


def _back_pad(pad_width, body_thickness, body_height, pad_depth, pad_gap, is_gap=False):
    return pipe(
        _pad(pad_width, body_thickness, body_height, pad_depth, is_gap),
        translate([0, pad_depth + body_thickness + pad_gap, 0]),
        color(PAD_COLOR),
    )


def _front_pad(
    pad_width, body_thickness, body_height, pad_depth, pad_gap, is_gap=False
):
    return pipe(
        _pad(pad_width, body_thickness, body_height, pad_depth, is_gap),
        rotate([0, 0, 180]),
        translate([0, pad_depth + body_thickness, 0]),
        color(PAD_COLOR),
    )

def _hacky_round_corner_patches(bottom_height, body_thickness):
    diameter_1 = 4
    patch_1 = pipe(
        cylinder(h=bottom_height, d=diameter_1, segments=RES),
    )

    slice_1 = pipe(
        cube([diameter_1, 16, bottom_height]),
        translate([diameter_1 / -2, 0, 0]),
        sub(patch_1),
        rotate([0, 0, 268]),
        translate([25.92, 13.4, 0]),
    )

    slice_2 = pipe(
        cube([diameter_1, 16, bottom_height]),
        translate([diameter_1 / -2, 0, 0]),
        sub(patch_1),
        rotate([0, 0, 92]),
        translate([66.1, 13.40, 0]),
    )

    slice_3 = pipe(
        cube([diameter_1, 16, bottom_height]),
        translate([diameter_1 / -2, 0, 0]),
        sub(patch_1),
        rotate([0, 0, 327.5]),
        translate([72.1, 16.8, 0]),
    )

    right_side = pipe(
        slice_1 + slice_2 + slice_3,
        translate([0, 0, body_thickness]),
        color("violet"),
    )

    left_side = pipe(right_side.copy(), mirror([1, 0, 0]))

    return right_side + left_side

def main():
    body_width = 188
    body_depth = 104
    body_thickness = 1.20
    body_height = 25
    # body_height = 5
    # body_height = 12.5
    bottom_height = body_height / 2
    top_height = body_height / 2
    tape_plane_height = 16

    spool_hole_diameter = 34
    spool_width = 88.5 + 2  # extra 2 is for amount it can move in the hole
    spool_height = 16.25

    # TODO FIXME DEBUG
    bottom_height = spool_height

    clutch_hole_diameter = 7
    clutch_hole_from_back = 19.5
    clutch_hole = pipe(
        cylinder(h=10, d=clutch_hole_diameter, center=True, segments=RES),
        translate(
            [0, body_depth - (clutch_hole_diameter / 2) - clutch_hole_from_back, 0]
        ),
    )

    spool_hole_1 = pipe(
        cylinder(h=10, d=spool_hole_diameter, center=True, segments=RES),
        translate([-46, 56, 0]),
    )

    dummy_spool_1 = pipe(
        cylinder(h=spool_height, d=spool_width, center=True, segments=RES),
        translate([-46, 56, spool_height / 2]),
        color(DUMMY_COLOR),
    )

    spool_hole_2 = pipe(
        cylinder(h=10, d=spool_hole_diameter, center=True, segments=RES),
        translate([46, 56, 0]),
    )

    dummy_spool_2 = pipe(
        cylinder(h=spool_height, d=spool_width, center=True, segments=RES),
        translate([46, 56, spool_height / 2]),
        color(DUMMY_COLOR),
    )

    bottom = pipe(
        cube([body_width, body_depth, body_thickness]),
        translate([body_width / -2, 0, 0]),
        sub(clutch_hole),
        sub(spool_hole_1),
        sub(spool_hole_2),
    )

    front_wall = _front_wall(body_width, body_thickness, bottom_height)

    back_wall = pipe(
        cube([body_width, body_thickness, bottom_height]),
        translate([body_width / -2, body_depth - body_thickness, 0]),
    )

    side_wall_1 = pipe(
        cube([body_thickness, body_depth, bottom_height]),
        translate([body_width / -2, 0, 0]),
    )

    side_wall_2 = pipe(
        cube([body_thickness, body_depth, bottom_height]),
        translate([(body_width / 2) - body_thickness, 0, 0]),
    )

    guide_post_diameter = 8

    # minus 1 for base overhang
    guide_post_from_front = 6

    # minus 1 for base overhang
    guide_post_from_side = 6

    guide_post_1 = pipe(
        _guide_post(guide_post_diameter),
        translate([guide_post_diameter / -2, guide_post_diameter / 2, body_thickness]),
        translate(
            [
                (body_width / 2) - body_thickness - guide_post_from_side,
                guide_post_from_front + body_thickness,
                0,
            ]
        ),
    )

    guide_post_2 = pipe(
        _guide_post(guide_post_diameter),
        translate([guide_post_diameter / 2, guide_post_diameter / 2, body_thickness]),
        translate(
            [
                ((body_width / 2) - body_thickness - guide_post_from_side) * -1,
                guide_post_from_front + body_thickness,
                0,
            ]
        ),
    )

    pad_width = 44 # 48
    pad_gap = 4
    pad_depth = guide_post_from_front + 1 - (pad_gap / 2)

    front_pad = _front_pad(pad_width, body_thickness, body_height, pad_depth, pad_gap)
    back_pad = _back_pad(pad_width, body_thickness, body_height, pad_depth, pad_gap)

    back_pad_retainer_offset = (
        body_thickness + guide_post_from_front + 1 + (pad_gap / 2) + body_thickness
    )

    back_pad_retainer_width = (
        body_width
        - (guide_post_from_side * 2)
        - (body_thickness * 2)
        - (guide_post_diameter * 2)
        - 10
    )

    back_pad_retainer_depth = body_depth - back_pad_retainer_offset

    back_pad_retainer = pipe(
        cube([back_pad_retainer_width, back_pad_retainer_depth, bottom_height]),
        center(0, back_pad_retainer_width),
        translate([0, back_pad_retainer_offset, 0]),
        sub(dummy_spool_1),
        sub(dummy_spool_2),
        sub(
            _back_pad(
                pad_width, body_thickness, body_height, pad_depth, pad_gap, is_gap=True
            )
        ),
    )

    front_pad_retainer = pipe(
        cube([pad_width - 0.4, pad_depth + body_thickness, bottom_height]),
        center(0, pad_width - 0.4),
        sub(
            _front_pad(
                pad_width, body_thickness, body_height, pad_depth, pad_gap, is_gap=True
            )
        ),
    )

    back_corner_fill_left = pipe(
        cube([48, 48, bottom_height]),
        center(0, body_width),
        translate([0, body_depth - 48, 0]),
        sub(dummy_spool_1),
    )

    back_corner_fill_left_roundoff = pipe(
        cylinder(h=bottom_height, d=2, segments=RES),
        translate([(body_width / 2) - body_thickness - 0.55, body_depth - 48, 0]),
        color("pink"),
    )

    back_corner_fill_left += back_corner_fill_left_roundoff

    back_corner_fill_right = pipe(back_corner_fill_left, mirror([1, 0, 0]))

    hacky_round_corner_patches = _hacky_round_corner_patches(bottom_height, body_thickness)

    final_bottom = cube([0, 0, 0])  # dummy starter
    final_bottom += bottom
    final_bottom += front_wall
    final_bottom += back_wall
    final_bottom += side_wall_1
    final_bottom += side_wall_2
    final_bottom += guide_post_1
    final_bottom += guide_post_2
    final_bottom += front_pad_retainer
    final_bottom += back_pad_retainer
    final_bottom += back_corner_fill_left
    final_bottom += back_corner_fill_right
    final_bottom -= hacky_round_corner_patches

    # TODO
    # - modify top and bottom to connect together (connectors, registration pegs)
    # - top should allow for metal spring from vhs case to hold down spools
    # - top should fill pad gap down to film plane height (post height)
    # - base of posts seems hard to clean. maybe a more general 1mm bottom fill of film path?
    final_top = pipe(
        final_bottom,
        mirror([0, 0, 1]),
        translate([0, 0, bottom_height * 2]),
        color("#990099"),
    )

    final = cube([0, 0, 0])  # dummy starter
    final += final_bottom
    # final += final_top

    final += pipe(front_pad + back_pad, rotate([0, 0, 180]), translate([0, -5, 0]))

    # final += front_pad
    # final += back_pad
    # final += dummy_spool_1
    # final += dummy_spool_2

    # final = _pad(body_thickness, body_height, pad_depth)

    scad_render_to_file(final, "build/vhs_cleaner2.scad")


if __name__ == "__main__":
    main()
