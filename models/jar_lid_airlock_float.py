import functools
from solid import *
from solid import screw_thread
from shared.main import *


float_height = 40
float_bottom_diameter = 27
float_top_diameter = 24
segments = 200
thickness = 1.25
window_width = 5
window_height = 9
window_offset = 3.25
num_windows = 6
window_degrees_per = 360 / num_windows * 2


def _window_cutout(index):
    return pipe(
        cube([window_width, 100, window_height], center=True),
        rotate([0, 0, window_degrees_per * index]),
        translate([0, 0, window_offset + (window_height / 2)])
    )


def main():
    body = cylinder(
        h=float_height,
        d1=float_bottom_diameter,
        d2=float_top_diameter,
        segments=segments
    )

    cutout = pipe(
        cylinder(
            h=float_height + 2,
            d1=float_bottom_diameter - thickness,
            d2=float_top_diameter - thickness,
            segments=segments
        ),
        translate([0, 0, -1])
    )

    body -= cutout

    for i in range(int(num_windows / 2)):
        body -= _window_cutout(i)

    cap = sphere(d=float_top_diameter, segments=segments)

    cap_cutout = sphere(
        d=float_top_diameter - (thickness * 2),
        segments=segments
    )

    cap_crop = pipe(cube(100, center=True), translate([0, 0, -50]))

    cap = pipe(cap - cap_cutout - cap_crop, translate([0, 0, float_height]))

    final = body + cap

    scad_render_to_file(final, "build/jar_lid_airlock_float.scad")


if __name__ == "__main__":
    main()
