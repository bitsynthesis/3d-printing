import functools
from solid import *
from solid import screw_thread
from shared.main import *


def _lid(
    inner_diameter,
    outer_diameter,
    wall_height,
    top_thread_padding,
    bottom_thread_padding,
    top_thickness,
    segments,
    grip_segments,
    oring_diameter
):
    thread_height = wall_height - top_thread_padding - bottom_thread_padding

    outline_pts = screw_thread.default_thread_section(
        tooth_height=2.25,
        tooth_depth=1.25
    )

    threads = pipe(
        screw_thread.thread(
            outline_pts=outline_pts,
            inner_rad=inner_diameter / 2,
            pitch=5,
            length=thread_height,
            external=False,
            segments_per_rot=segments,
            neck_in_degrees=6,
            neck_out_degrees=6
        ),
        translate([0, 0, bottom_thread_padding + top_thickness])
    )

    wall = cylinder(
        h=wall_height + top_thickness,
        d=outer_diameter,
        segments=grip_segments
    )

    cutout = pipe(
        cylinder(h=wall_height + 2, d=inner_diameter, segments=segments),
        translate([0, 0, top_thickness])
    )

    oring_gutter = pipe(
        circle(d=oring_diameter, segments=segments),
        translate([(inner_diameter - oring_diameter) / 2, 0, 0]),
        rotate_extrude(convexity=10, segments=segments),
        translate([0, 0, top_thickness])
    )

    return wall - cutout - oring_gutter + threads


def _retaining_wall(inner_diameter, outer_diameter, top_width, segments, outer_segments=None):
    if outer_segments is None:
        outer_segments = segments

    height = outer_diameter - inner_diameter
    bottom_width = height + top_width

    # TODO outer seg
    wall = pipe(
        polygon(
            points=[
                [0, 0],
                [height / 2, height],
                [(height / 2) + top_width, height],
                [bottom_width, 0]
            ]
        ),
        translate([(outer_diameter / 2) - bottom_width, 0, 0]),
        rotate_extrude(convexity=10, segments=segments),
        rotate([180, 0, 0])
    )

    return wall


def main():
    wall_thickness = 2.5
    inner_diameter = 110
    outer_diameter = inner_diameter + (wall_thickness * 2)
    smooth_segments = 200
    grip_segments = 24
    airlock_height = 15
    airlock_top_width = 5

    lid = _lid(
        inner_diameter=inner_diameter,
        outer_diameter=outer_diameter,
        wall_height=12,
        top_thread_padding=2,
        bottom_thread_padding=5,
        top_thickness=wall_thickness,
        segments=smooth_segments,
        grip_segments=grip_segments,
        oring_diameter=4
    )

    ow_id = outer_diameter - airlock_height

    outer_wall = _retaining_wall(
        ow_id,
        outer_diameter,
        airlock_top_width,
        grip_segments
    )

    iw_od = ow_id - (airlock_top_width * 4) - airlock_height
    iw_id = iw_od - airlock_height

    inner_wall = _retaining_wall(iw_id, iw_od, airlock_top_width, smooth_segments)

    airlock_hole = cylinder(
        h=100,
        d=iw_id - (airlock_top_width * 2),
        center=True,
        segments=smooth_segments
    )

    final = lid + outer_wall + inner_wall - airlock_hole

    scad_render_to_file(final, "build/jar_lid_airlock_1_gal_v2.scad")


if __name__ == "__main__":
    main()
