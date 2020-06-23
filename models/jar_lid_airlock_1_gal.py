import functools
from solid import *
from solid import screw_thread
from shared.main import *


inner_diameter = 110
wall_thickness = 2.5
smooth_segments = 200


wall_height = 11
wall_top_padding = 3
wall_bottom_padding = 3
thread_height = wall_height - wall_top_padding - wall_bottom_padding


airlock_height = 50
airlock_outer_diameter = 35
airlock_inner_diameter = 11


top_height = airlock_height


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
        translate([0, 0, wall_bottom_padding])
    )

    outer_diameter = inner_diameter + (wall_thickness * 2)

    wall = cylinder(
        h=wall_height,
        d=outer_diameter,
        segments=24
    )

    cutout = pipe(
        cylinder(h=wall_height + 2, d=inner_diameter, segments=smooth_segments),
        translate([0, 0, -1])
    )

    top = cylinder(h=top_height, d=outer_diameter, segments=24)

    airlock_hole = pipe(
        cylinder(h=top_height + 2, d=airlock_outer_diameter, segments=smooth_segments),
        translate([0, 0, -1])
    )

    return pipe(wall - cutout + threads, translate([0, 0, top_height])) + top - airlock_hole


# TODO
# - move bottom of airlock chamber up a little for durability
# - thicker center post walls?
def _airlock():
    outer_wall = tube(h=airlock_height, d=airlock_outer_diameter, thickness=wall_thickness, segments=smooth_segments)

    inner_wall = tube(h=airlock_height, d=airlock_inner_diameter, thickness=wall_thickness, segments=smooth_segments)

    bottom_height = (airlock_outer_diameter - airlock_inner_diameter) / 2

    bottom = cylinder(
        h=bottom_height,
        d1=airlock_inner_diameter,
        d2=airlock_outer_diameter,
        segments=smooth_segments
    )

    bottom = pipe(bottom, translate([0, 0, airlock_height - bottom_height]))

    barb_width = 13.5
    barb = cylinder(h=barb_width, d1=airlock_inner_diameter, d2=barb_width, segments=smooth_segments)

    cutout = pipe(
        cylinder(h=airlock_height + 2, d=airlock_inner_diameter-wall_thickness, segments=smooth_segments),
        translate([0, 0, -1])
    )

    return outer_wall + inner_wall + bottom + barb - cutout


def main():
    final = _lid() + _airlock()

    scad_render_to_file(final, "build/jar_lid_airlock_1_gal.scad")


if __name__ == "__main__":
    main()
