import functools
from solid import *
from shared.main import *


body_height = 5
body_outer_diameter = 90
body_inner_diameter = 65
body_segment_width = 8


support_height = 20


handle_height = 200
handle_diameter = 20
handle_segments = 8

smooth_segments = 200


def _spoke():
    spoke_length = (body_outer_diameter / 2) - (body_segment_width / 4)

    center_offset = -1 * body_segment_width / 2

    body = pipe(
        cube([spoke_length, body_segment_width, body_height]),
        translate([0, center_offset, 0])
    )

    support = pipe(
        triangular_prism(body_segment_width, spoke_length, support_height),
        translate([center_offset, 0, body_height]),
        rotate([0, 0, 180]),
        translate([0, spoke_length, 0])
    )

    return body + support


def main():
    outer_ring = cylinder(
        h=body_height,
        d=body_outer_diameter,
        segments=smooth_segments
    )

    outer_ring = outer_ring - cylinder(
        h=body_height,
        d=body_outer_diameter - (body_segment_width * 2),
        segments=smooth_segments
    )

    inner_ring = cylinder(
        h=body_height,
        d=body_inner_diameter,
        segments=smooth_segments
    )

    inner_ring = inner_ring - cylinder(
        h=body_height,
        d=body_inner_diameter - (body_segment_width * 2),
        segments=smooth_segments
    )

    spokes = [
        pipe(
            _spoke(),
            rotate([0, 0, (360 / handle_segments) * i])
        )
        for i in range(handle_segments)
    ]

    spokes = functools.reduce(lambda x, y: x + y, spokes)

    handle = pipe(
        cylinder(
            h=handle_height,
            d=handle_diameter,
            segments=handle_segments
        ),
        rotate([0, 0, 180 / handle_segments])
    )

    final = outer_ring + inner_ring + spokes + handle

    scad_render_to_file(final, "build/kraut_masher.scad")


if __name__ == "__main__":
    main()
