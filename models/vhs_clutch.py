from solid import *
from shared.main import *


#     B
# --------
# |      |A
# |C
# |
# ---D


def main():
    width = 6.5
    half_width = width / 2
    thickness = 1.5

    a_height = 12
    b_length = 22.50
    c_height = 25.25
    d_length = 6
    nub_diameter = 2

    seg_a = pipe(
        sphere(d=width, segments=RESOLUTION) +
        cylinder(h=a_height + thickness - half_width, d=width, segments=RESOLUTION),
        translate([width / 2, 0, half_width + c_height - a_height + thickness])
    )

    seg_b = pipe(
        cube(
            [b_length + thickness, width, thickness],
            center=True
        ),
        translate([
            ((b_length + thickness) / 2) + half_width,
            0,
            c_height + thickness + (thickness / 2)
        ])
    )

    seg_c = pipe(
        cube([thickness, width, c_height], center=True),
        translate([
            (thickness / 2) + half_width + b_length,
            0,
            (c_height / 2) + thickness
        ])
    )

    seg_d = pipe(
        cube([d_length + thickness, width, thickness], center=True),
        translate([
            ((d_length + thickness) / 2) + b_length - d_length + half_width,
            0,
            thickness / 2
        ])
    )

    nub = pipe(
        cylinder(h=width, d=nub_diameter, segments=RESOLUTION),
        rotate([90, 0, 0]),
        translate([
            b_length - d_length + half_width + (nub_diameter / 2),
            width / 2,
            thickness
        ])
    )

    final = pipe(
        seg_a + seg_b + seg_c + seg_d + nub,
        rotate([90, 0, 0]),
        translate([0, 0, width / 2])
    )

    scad_render_to_file(final, "build/vhs_clutch.scad")


if __name__ == "__main__":
    main()
