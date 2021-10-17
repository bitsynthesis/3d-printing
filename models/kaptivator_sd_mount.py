from solid import *
from shared.main import *


sd_height = 52.5
sd_width = 35.5
sd_center_thickness = 5.5
sd_side_thickness = 2.5
sd_top_height = 27


sd_total_thickness = 11.5
sd_total_width = 44
sd_adapter_side_gap_width = 3.5
sd_adapter_side_gap_thickness = 5


thin_border = sd_adapter_side_gap_width
thick_border = 10


hex_diameter = 5.25
hex_height = 6


# TODO
# - 2 screws for stability
# - slightly wider hex holes
# - sd card runway (watch out for front panel pcb)


def main():
    body = cube([
        thin_border + sd_total_width + thick_border,
        thin_border + sd_height + thin_border,
        thin_border + sd_total_thickness
    ])

    primary_gap = pipe(
        cube([
            sd_total_width,
            sd_height,
            sd_total_thickness
        ]),
        translate([thin_border, thin_border, thin_border]),
        hole()
    )

    side_gap = pipe(
        cube([
           thin_border + sd_total_width - sd_width,
           thin_border + sd_height + thin_border,
           sd_total_thickness - sd_adapter_side_gap_thickness
        ]),
        translate([
            0,
            0,
            thin_border + sd_adapter_side_gap_thickness
        ]),
        hole()
    )

    card_gap = pipe(
        cube([sd_width, thin_border, sd_total_thickness]),
        translate([
            thin_border + sd_total_width - sd_width,
            0,
            thin_border + sd_side_thickness
        ]),
        hole()
    )

    screw_mount = pipe(
        cylinder(h=hex_height, d=hex_diameter, segments=6),
        translate([
            thin_border + sd_total_width + int(thick_border / 2),
            thin_border + int(sd_height / 2),
            thin_border + sd_total_thickness - hex_height
        ]),
        hole()
    )

    final = body + primary_gap + side_gap + card_gap + screw_mount

    scad_render_to_file(final, "build/kaptivator_sd_mount.scad")


if __name__ == "__main__":
    main()
