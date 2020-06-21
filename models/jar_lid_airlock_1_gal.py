import functools
from solid import *
from solid import screw_thread
from shared.main import *


inner_diameter = 109
wall_thickness = 2.5
smooth_segments = 200

wall_height = 11
wall_top_padding = 2
wall_bottom_padding = 2
thread_height = wall_height - wall_top_padding - wall_bottom_padding


def main():
    threads = pipe(
        screw_thread.thread(
            outline_pts=screw_thread.default_thread_section(tooth_height=2.25, tooth_depth=1.25),
            inner_rad=inner_diameter / 2,
            pitch=5,
            length=thread_height,
            external=False,
            segments_per_rot=smooth_segments,
            neck_in_degrees=6,
            neck_out_degrees=6
        ),
        translate([0, 0, wall_bottom_padding])
    )

    wall = cylinder(
        h=wall_height,
        d=inner_diameter + (wall_thickness * 2),
        segments=24
    )

    wall = wall - cylinder(
        h=wall_height,
        d=inner_diameter,
        segments=smooth_segments
    )

    final = wall + threads

    scad_render_to_file(final, "build/jar_lid_airlock_1_gal.scad")


if __name__ == "__main__":
    main()
