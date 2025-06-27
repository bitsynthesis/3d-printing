from solid import *
from shared.main import *


def main():
    base_diameter = 120.5
    cable_height = 5
    cable_width = 10
    cutout_buffer = 1
    segments = 200

    cutout_height = cable_height + cutout_buffer
    cutout_width = cable_width + cutout_buffer
    base_height = cutout_height

    base = cylinder(d=base_diameter, h=base_height, segments=segments)

    inner_cutout = cylinder(d=47, h=base_height, segments=segments)

    # BEGIN GROOVE

    groove_inner_diameter = 65
    groove_outer_diameter = 76

    groove_outer = cylinder(d=groove_outer_diameter, h=base_height, segments=segments)
    groove_inner = cylinder(d=groove_inner_diameter, h=base_height, segments=segments)

    ring_connector_width = 24

    ring_connector_1 = pipe(
        cube([base_diameter + 2, ring_connector_width, base_height], center=True),
        translate([0, 0, base_height / 2]),
        rotate([0, 0, 45]),
    )

    ring_connector_2 = pipe(
        cube([base_diameter + 2, ring_connector_width, base_height], center=True),
        translate([0, 0, base_height / 2]),
        rotate([0, 0, -45]),
    )

    ground_cutout_distance = 32.5
    ground_cutout_angle = 45
    ground_cutout_diameter = 8

    ground_cutout_1 = pipe(
        cylinder(d=ground_cutout_diameter, h=base_height, segments=segments),
        translate([0, ground_cutout_distance, 0]),
        rotate([0, 0, 45]),
    )

    ground_cutout_2 = pipe(
        cylinder(d=ground_cutout_diameter, h=base_height, segments=segments),
        translate([0, ground_cutout_distance, 0]),
        rotate([0, 0, 225]),
    )

    ground_cutout = ground_cutout_1 + ground_cutout_2

    groove = (
        groove_outer
        - groove_inner
        - ring_connector_1
        - ring_connector_2
        + ground_cutout
    )

    # END GROOVE

    # BEGIN REGISTRATION PINS

    pin_diameter = 3
    pin_height = 4

    pin_1 = pipe(
        cylinder(d=pin_diameter, h=pin_height, segments=segments),
        translate([0, 45, base_height]),
    )

    pin_2 = pipe(
        cylinder(d=pin_diameter, h=pin_height, segments=segments),
        translate([0, -45, base_height]),
    )

    registration_pins = pin_1 + pin_2

    # END REGISTRATION PINS

    cable_channel = pipe(
        cube([base_diameter / 2, cutout_width, cutout_height]),
        translate([0, cutout_width / -2, 0]),
    )

    final = pipe(base - inner_cutout - groove - cable_channel + registration_pins)

    scad_render_to_file(final, "build/art_spotlight_base.scad")


if __name__ == "__main__":
    main()
