import functools
from solid import *
from shared.main import *


clamp_height = 60
clamp_thickness = 5
clamp_inner_diameter = 35.5
clamp_outer_diameter = clamp_inner_diameter + (clamp_thickness * 2)
clamp_gap = 2

tab_thickness = 5
tab_height = 43
tab_node_diameter = 15

hook_bed_usable_width = 75
hook_bed_width = hook_bed_usable_width + (clamp_outer_diameter / 2)
hook_height = 15
hook_nub_height = 10
hook_thickness = (clamp_inner_diameter + (clamp_thickness * 2)) / 2

smooth_segments = 250


def tab(is_nut=True):
    base = cube([0.1, tab_thickness, tab_height])

    shaft_hole_diameter = 3.5
    nut_hole_diameter = 6.75
    head_hole_diameter = 8
    nut_or_head_depth = 2.5 # 3

    shaft_hole = cylinder(
        h=tab_thickness,
        d=shaft_hole_diameter,
        segments=smooth_segments
    )

    if is_nut:
        nut_or_head_hole = pipe(
            cylinder(
                h=nut_or_head_depth,
                d=nut_hole_diameter,
                segments=6,
            ),
            translate([0, 0, tab_thickness - nut_or_head_depth]),
        )

    else:
        nut_or_head_hole = cylinder(
            h=nut_or_head_depth,
            d=head_hole_diameter,
            segments=smooth_segments
        )

    combined_hole = pipe(
        shaft_hole + nut_or_head_hole,
        rotate([270, 0, 0]),
        translate([
            (tab_node_diameter / 2) + (clamp_thickness / 2) + 2,
            0,
            tab_height / 3 * 2
        ]),
    )

    node = cylinder(h=tab_thickness, d=tab_node_diameter, segments=smooth_segments)
    node = pipe(
        node,
        rotate([270, 0, 0]),
        translate([
            (tab_node_diameter / 2) + (clamp_thickness / 2),
            0,
            tab_height / 3 * 2
        ]),
    )

    # TODO hull base and node together to form triangle tab

    return pipe(base + node, hull()) - combined_hole


def main():
    # hook bed 75mm


    # \------/

    inner = cylinder(
        h=clamp_height,
        d=clamp_inner_diameter,
        segments=smooth_segments,
    )

    outer = cylinder(
        h=clamp_height,
        d=clamp_outer_diameter,
        segments=smooth_segments,
    )

    gap = pipe(
        cube([clamp_outer_diameter, clamp_gap, clamp_height]),
        translate([0, clamp_gap / -2, 0])
    )

    tab_gap_offset = clamp_gap / 2

    tab1 = pipe(
        tab(is_nut=True),
        translate([
            clamp_inner_diameter / 2,
            tab_gap_offset,
            (clamp_height - tab_height) / 2
        ])
    )

    tab2 = pipe(
        tab(is_nut=False),
        translate([
            clamp_inner_diameter / 2,
            0 - tab_thickness - tab_gap_offset,
            (clamp_height - tab_height) / 2
        ])
    )

    hook = pipe(
        polygon(points=[
            [0, 0],
            [hook_bed_width - hook_height, 0],
            [hook_bed_width, hook_height],
            [hook_bed_width, hook_height + hook_nub_height],
            [hook_bed_width - hook_nub_height, hook_height],
            [hook_nub_height + (clamp_outer_diameter / 2), hook_height],
            [0, hook_height + hook_nub_height + (clamp_outer_diameter / 2)],
        ]),
        linear_extrude(height=hook_thickness),
        rotate([90, 0, 180]),
        translate([0, hook_thickness / -2, 0]),
    )

    final = outer + hook - inner - gap + tab1 + tab2

    scad_render_to_file(final, "build/pipe_clamp_headphone_hook.scad")


if __name__ == "__main__":
    main()
