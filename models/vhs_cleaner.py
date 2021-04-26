from solid import *
from shared.main import *


RES = 200


def _cleaning_trough(width, depth, height):
    spacing = 3
    thickness = (depth - spacing) / 2
    side_1 = cube([width, thickness, height])
    side_2 = pipe(
        cube([width, thickness, height]),
        translate([0, thickness + spacing, 0])
    )
    return pipe(
        side_1 + side_2,
        translate([width / -2, depth / -2, 0])
    )


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


def main():
    body_width = 188
    body_depth = 102
    body_thickness = 1.25
    body_height = 25
    # body_height = 5
    body_height = 12.5

    spool_hole_diameter = 34
    spool_width = 88.5 + 2 # extra 2 is for amount it can move in the hole
    spool_height = 16.25

    bottom = pipe(
        cube([body_width, body_depth, body_thickness]),
        translate([body_width / -2, 0, 0])
    )

    spool_hole_1 = pipe(
        cylinder(h=10, d=spool_hole_diameter, center=True, segments=RES),
        translate([-46, 54, 0])
    )

    dummy_spool_1 = pipe(
        cylinder(h=spool_height, d=spool_width, center=True, segments=RES),
        translate([-46, 54, spool_height / 2])
    )

    spool_hole_2 = pipe(
        cylinder(h=10, d=spool_hole_diameter, center=True, segments=RES),
        translate([46, 54, 0])
    )

    dummy_spool_2 = pipe(
        cylinder(h=spool_height, d=spool_width, center=True, segments=RES),
        translate([46, 54, spool_height / 2])
    )

    front_wall = pipe(
        cube([body_width, body_thickness, body_height]),
        translate([body_width / -2, 0, 0])
    )

    back_wall = pipe(
        cube([body_width, body_thickness, body_height]),
        translate([body_width / -2, body_depth - body_thickness, 0])
    )

    side_wall_1 = pipe(
        cube([body_thickness, body_depth, body_height]),
        translate([body_width / -2, 0, 0])
    )

    side_wall_2 = pipe(
        cube([body_thickness, body_depth, body_height]),
        translate([(body_width / 2) - body_thickness, 0, 0])
    )

    guide_post_diameter = 8

    # minus 1 for base overhang
    guide_post_from_front = 2

    # minus 1 for base overhang
    guide_post_from_side = 0

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

    cleaning_trough_width = 160
    cleaning_trough_depth = 6
    cleaning_trough = pipe(
        _cleaning_trough(cleaning_trough_width, cleaning_trough_depth, body_height),
        translate([0, guide_post_from_front + 1 + body_thickness, 0])
    )

    support_fill = pipe(
        cube([
            cleaning_trough_width,
            body_depth - cleaning_trough_depth - body_thickness,
            body_height
        ]),
        translate([
            cleaning_trough_width / -2,
            cleaning_trough_depth + body_thickness,
            0
        ])
    )

    # hack
    support_crop_1 = pipe(
        cube([20, 20, 100]),
        translate([70, 16, 0])
    )

    # hack
    support_crop_2 = pipe(
        cube([20, 20, 100]),
        translate([-90, 16, 0])
    )

    support_fill = support_fill \
        - dummy_spool_1 \
        - dummy_spool_2 \
        - support_crop_1 \
        - support_crop_2

    final = bottom \
        - spool_hole_1 \
        - spool_hole_2 \
        + front_wall \
        + back_wall \
        + side_wall_1 \
        + side_wall_2 \
        + guide_post_1 \
        + guide_post_2 \
        + cleaning_trough \
        + support_fill

    scad_render_to_file(final, "build/vhs_cleaner.scad")


if __name__ == "__main__":
    main()
