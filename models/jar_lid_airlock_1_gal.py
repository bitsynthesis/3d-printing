import functools
from solid import *
from solid import screw_thread
from shared.main import *


inner_diameter = 110
wall_thickness = 2.5
smooth_segments = 200


wall_height = 12
wall_top_padding = 2
wall_bottom_padding = 5
thread_height = wall_height - wall_top_padding - wall_bottom_padding


airlock_height = 50
airlock_outer_diameter = 35
airlock_inner_diameter = 11


outer_diameter = inner_diameter + (wall_thickness * 2)
chamf_padding = 20
chamf_height = (outer_diameter - airlock_outer_diameter - chamf_padding) / 2

skirt_height = airlock_height - chamf_height
grip_segments = 24
oring_diameter = 4
barb_width = 13.5


def _lid():
    threads = pipe(
        screw_thread.thread(
            outline_pts=screw_thread.default_thread_section(tooth_height=2.25, tooth_depth=1.25), inner_rad=inner_diameter / 2,
            pitch=5,
            length=thread_height,
            external=False,
            segments_per_rot=smooth_segments,
            neck_in_degrees=6,
            neck_out_degrees=6
        ),
        translate([0, 0, wall_bottom_padding + skirt_height])
    )

    wall = cylinder(
        h=wall_height + skirt_height,
        d=outer_diameter,
        segments=grip_segments
    )

    cutout = pipe(
        cylinder(h=wall_height + 2, d=inner_diameter, segments=smooth_segments),
        translate([0, 0, skirt_height])
    )

    cap = pipe(
        wall - cutout + threads,
        translate([0, 0, chamf_height])
    )

    airlock_hole = pipe(
        cylinder(h=airlock_height + 2, d=airlock_outer_diameter, segments=smooth_segments),
        translate([0, 0, -1])
    )

    chamf = cylinder(
        h=chamf_height,
        d1=airlock_outer_diameter + (chamf_padding * 2),
        d2=outer_diameter,
        segments=grip_segments
    )

    oring_gutter = pipe(
        circle(d=oring_diameter, segments=smooth_segments),
        translate([(inner_diameter - oring_diameter) / 2, 0, 0]),
        rotate_extrude(convexity=10, segments=smooth_segments),
        translate([0, 0, airlock_height])
    )

    return cap + chamf - airlock_hole - oring_gutter


# TODO
# - thicker center post walls?
def _airlock():
    outer_wall = tube(
        h=airlock_height,
        d=airlock_outer_diameter,
        thickness=wall_thickness,
        segments=smooth_segments
    )

    inner_wall = tube(
        h=airlock_height,
        d=airlock_inner_diameter,
        thickness=wall_thickness,
        segments=smooth_segments
    )

    gutter_diameter = (airlock_outer_diameter - airlock_inner_diameter - wall_thickness) / 2
    gutter_center = (airlock_inner_diameter + gutter_diameter) / 2

    bottom = pipe(
        cylinder(
            h=gutter_diameter / 2,
            d=airlock_outer_diameter,
            segments=smooth_segments
        ),
        translate([0, 0, airlock_height - (gutter_diameter / 2) - wall_thickness])
    )

    bottom += pipe(
        cylinder(
            h=wall_thickness,
            d=airlock_outer_diameter,
            segments=smooth_segments
        ),
        translate([0, 0, airlock_height - wall_thickness])
    )

    gutter = pipe(
        circle(d=gutter_diameter, segments=smooth_segments),
        translate([gutter_center, 0, 0]),
        rotate_extrude(convexity=10, segments=smooth_segments),
        translate([0, 0, airlock_height - (gutter_diameter / 2) - wall_thickness])
    )

    bottom -= gutter

    barb = cylinder(
        h=barb_width,
        d1=airlock_inner_diameter,
        d2=barb_width,
        segments=smooth_segments
    )

    cutout = pipe(
        cylinder(
            h=airlock_height + 2,
            d=airlock_inner_diameter-wall_thickness,
            segments=smooth_segments
        ),
        translate([0, 0, -1])
    )

    return outer_wall + inner_wall + bottom + barb - cutout


def main():
    final = _lid() + _airlock()

    scad_render_to_file(final, "build/jar_lid_airlock_1_gal.scad")


if __name__ == "__main__":
    main()
