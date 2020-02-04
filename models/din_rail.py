from solid import *
from shared.main import *


def main():
    length = 7.5
    width = 100
    height = 35
    spine_height = 27
    edge_length = 2
    trough_length = 3
    trough_height = 10 # TODO base on screw size
    trough_padding = 3

    spine = pipe(
        cube([length, width, spine_height]),
        translate([0, 0, (height - spine_height) / 2])
    )

    edge = pipe(
        cube([edge_length, width, height]),
        translate([length - edge_length, 0, 0])
    )

    # trough = pipe(
    #     cube([length, width, trough_height]),
    #     hole(),
    #     translate([trough_length, 0, (height - trough_height) / 2])
    # )
    #
    # trough_edge = pipe(
    #     triangular_prism(
    #         width, length - trough_length, ((spine_height - trough_height) / 2) - trough_padding
    #     ),
    #     rotate([0, 0, 90]),
    #     translate([length, 0, ((spine_height - trough_height) / 2) - trough_padding])
    # )
    #
    # final = spine + edge + trough + trough_edge

    screw_shaft = 5
    screw_head = 10
    screw_head_depth = 4
    screw_count = 4
    screw_edge_padding = 15

    screw_head_hole = pipe(
        cylinder(h=screw_head_depth, d1=screw_shaft, d2=screw_head, segments=RESOLUTION),
        translate([0, 0, length - screw_head_depth])
    )

    screw_hole = pipe(
        cylinder(h=length, d=screw_shaft, segments=RESOLUTION) + screw_head_hole,
        hole(),
        rotate([0, 90, 0]),
        translate([0, 0, height / 2])
    )

    screw_spacing = (width - screw_edge_padding - screw_edge_padding) / (screw_count - 1)

    screw_pos = screw_edge_padding
    screws = []
    while(screw_pos < width):
        screws += pipe(screw_hole, translate([0, screw_pos, 0]))
        screw_pos += screw_spacing

    left_stop = cube([length, edge_length, height])
    right_stop = pipe(left_stop, translate([0, width, 0]))

    final = pipe(
        spine + edge + left_stop + right_stop + screws,
        rotate([0, 90, 0])
    )

    scad_render_to_file(final, "build/din_rail.scad")


if __name__ == "__main__":
    main()
