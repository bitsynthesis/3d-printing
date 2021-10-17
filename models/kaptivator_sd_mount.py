from solid import *
from shared.main import *


sd_height = 52.75 # padded .25
sd_width = 35.75 # padded .25
sd_center_thickness = 5.5
sd_side_thickness = 2.5
sd_top_height = 27


sd_total_thickness = 11.5
sd_total_width = 44.25 # padded .25
sd_adapter_side_gap_width = 3.5
sd_adapter_side_gap_thickness = 5


thin_border = sd_adapter_side_gap_width
thick_border = 10


hex_diameter = 5.5
hex_height = 6
screw_diameter = 2.5

runway_height = 30


# TODO
# - 2 screws for stability
# - slightly wider hex holes
# - sd card runway (watch out for front panel pcb)


def _screw_mount():
    hex_hole = cylinder(h=hex_height, d=hex_diameter, segments=6)

    screw_hole = pipe(
        cylinder(h=sd_total_thickness, d=screw_diameter, segments=100),
        translate([0, 0, hex_height]),
    )

    return pipe(hex_hole + screw_hole, hole())


def _runway():
    body = cube([
        thin_border + sd_total_width + thin_border,
        runway_height + thin_border,
        thin_border + sd_total_thickness
    ])

    card_gap = pipe(
        cube([
            sd_width,
            runway_height,
            sd_total_thickness
        ]),
        translate([
            thin_border + sd_total_width - sd_width,
            thin_border,
            thin_border + sd_side_thickness
        ]),
        hole()
    )

    side_gap = pipe(
        cube([
           thin_border + sd_total_width - sd_width,
           thick_border + sd_height + thin_border,
           sd_total_thickness - sd_adapter_side_gap_thickness
        ]),
        translate([
            0,
            thin_border + runway_height - thick_border,
            thin_border + sd_adapter_side_gap_thickness
        ]),
        hole()
    )

    screw = pipe(
        _screw_mount(),
        translate([
            int((thin_border + sd_total_width - sd_width) / 2),
            int((runway_height + thin_border) / 4),
            0
        ])
    )

    return pipe(
        body + card_gap + side_gap + screw,
        translate([
            0,
            runway_height * -1,
            0
        ])
    )


def main():
    body = cube([
        thin_border + sd_total_width + thin_border,
        thick_border + sd_height + thin_border,
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
           thick_border + sd_height + thin_border,
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

    top_screw = pipe(
        _screw_mount(),
        translate([
            int((thin_border + sd_total_width + thin_border) / 2),
            thin_border + sd_height + int(thick_border / 2),
            0
        ])
    )

    final = body + primary_gap + side_gap + card_gap + top_screw + _runway()

    scad_render_to_file(final, "build/kaptivator_sd_mount.scad")


if __name__ == "__main__":
    main()
