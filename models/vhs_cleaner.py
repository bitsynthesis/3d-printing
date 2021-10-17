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





def _outside_pad(gap_width, total_width, body_height, body_thickness, pad_height):

    tab_width = 10
    tab_middle_overhang = 6
    tab_height = pad_height
    full_tab_width = tab_width + tab_middle_overhang

    tab_1 = pipe(
        cube([full_tab_width, 1, tab_height]),
        translate([
            ((gap_width / 2) + tab_width) * -1,
            body_thickness,
            body_thickness
        ])
    )

    tab_2 = pipe(
        cube([full_tab_width, 1, tab_height]),
        translate([
            (gap_width / 2) - tab_middle_overhang,
            body_thickness,
            body_thickness
        ])
    )

    middle = pipe(
        cube([gap_width, body_thickness, body_height]),
        translate([gap_width / -2, 0, 0])
    )

    return tab_1 + middle + tab_2


def _inside_pad(pad_width, body_thickness, tab_width, tab_height, body_height, pad_height):
    pad = pipe(
        cube([
            pad_width,
            body_thickness,
            pad_height
        ]),
        translate([pad_width / -2, 0, tab_height])
    )

    bottom_tab_1 = pipe(
        cube([tab_width, body_thickness, tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / 4, 0, 0])
    )

    bottom_tab_2 = pipe(
        cube([tab_width, body_thickness, tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / -4, 0, 0])
    )

    top_tab_height = body_height - body_thickness - pad_height
    top_tab_1 = pipe(
        cube([tab_width, body_thickness, top_tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / 4, 0, body_thickness + pad_height])
    )

    top_tab_2 = pipe(
        cube([tab_width, body_thickness, top_tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / -4, 0, body_thickness + pad_height])
    )

    return pad + bottom_tab_1 + bottom_tab_2 + top_tab_1 + top_tab_2


def main():
    body_width = 188
    body_depth = 102
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
        cube([body_width, body_thickness, bottom_height]),
        translate([body_width / -2, 0, 0])
    )

    outside_pad_gap_width = 70
    outside_pad_gap = pipe(
        cube([outside_pad_gap_width, 10, body_height * 2]),
        translate([outside_pad_gap_width / -2, -5, body_height / -2])
    )

    front_wall -= outside_pad_gap

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

    # cleaning_trough_width = 160
    # cleaning_trough_depth = 6
    # cleaning_trough = pipe(
    #     _cleaning_trough(cleaning_trough_width, cleaning_trough_depth, body_height),
    #     translate([0, guide_post_from_front + 1 + body_thickness, 0])
    # )
    #
    # support_fill = pipe(
    #     cube([
    #         cleaning_trough_width,
    #         body_depth - cleaning_trough_depth - body_thickness,
    #         body_height
    #     ]),
    #     translate([
    #         cleaning_trough_width / -2,
    #         cleaning_trough_depth + body_thickness,
    #         0
    #     ])
    # )
    #
    # # hack
    # support_crop_1 = pipe(
    #     cube([20, 20, 100]),
    #     translate([70, 16, 0])
    # )
    #
    # # hack
    # support_crop_2 = pipe(
    #     cube([20, 20, 100]),
    #     translate([-90, 16, 0])
    # )

    outside_pad = _pad(
        outside_pad_gap_width,
        5,
        tape_plane_height,
        body_height - body_thickness - tape_plane_height,
        body_thickness,
        body_thickness,
        body_thickness * 2
    )

    inside_pad_width = outside_pad_gap_width - 12
    inside_pad_tab_width = 20
    inside_pad = pipe(
        _inside_pad(
            inside_pad_width,
            body_thickness,
            inside_pad_tab_width,
            body_thickness,
            body_height,
            tape_plane_height
        ),
        translate([0, 6, 0])
    )

    # support_fill = support_fill \
    #     - dummy_spool_1 \
    #     - dummy_spool_2 \
    #     - support_crop_1 \
    #     - support_crop_2

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

        # + cleaning_trough \
        # + support_fill

    final = outside_pad + inside_pad
    final = outside_pad

    scad_render_to_file(final, "build/vhs_cleaner.scad")


if __name__ == "__main__":
    main()
