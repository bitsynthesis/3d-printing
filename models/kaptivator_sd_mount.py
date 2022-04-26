from solid import *
from shared.main import *


sd_height = 52.75 # actual 52.5
sd_width = 35.75 # actual 35.5
sd_center_thickness = 5.5
sd_side_thickness = 2.5
sd_top_height = 25


sd_total_thickness = 11.5
sd_total_width = 44.25 # actual 44
sd_adapter_side_gap_width = 3.5
sd_adapter_side_gap_thickness = 5


thin_border = sd_adapter_side_gap_width
thick_border = 10


hex_diameter = 5.8 # actual 5.25
hex_height = 6.3 # actual 6
screw_diameter = 3 # actual 2.5


runway_height = 16
runway_width = 30


# TODO
# - 2 screws for stability
# - slightly wider hex holes
# - sd card runway (watch out for front panel pcb)


def _screw_mount():
    hex_hole = cylinder(h=hex_height, d=hex_diameter, segments=6)

    screw_hole = pipe(
        cylinder(h=sd_total_thickness + thin_border, d=screw_diameter, segments=100),
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
            runway_width,
            runway_height,
            sd_total_thickness
        ]),
        translate([
            thin_border + sd_total_width - runway_width,
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

    # pcb_gap = pipe(
    #     cube([
    #         thin_border,
    #         thin_border + runway_height - thick_border,
    #         thin_border + sd_total_thickness
    #     ]),
    #     translate([
    #         thin_border + sd_total_width,
    #         0,
    #         0
    #     ]),
    #     hole()
    # )

    pos_slope = triangular_prism(runway_width, runway_height - thin_border, sd_side_thickness)

    neg_slope = pipe(
        cube([runway_width, runway_height, sd_side_thickness + thin_border]) - pos_slope,
        translate([thin_border + sd_total_width - runway_width, thin_border, thin_border]),
    )

    return body - neg_slope + card_gap + side_gap


def _lid():
    body = pipe(
        cube([
            thin_border + sd_total_width + thin_border,
            thick_border + sd_height + thin_border + runway_height,
            thin_border
        ]),
        translate([0, 0, sd_center_thickness])
    )

    plateau = pipe(
        cube([
            runway_width,
            sd_top_height,
            sd_center_thickness
        ]),
        translate([
            thin_border + sd_total_width - runway_width,
            sd_height + thin_border + runway_height - sd_top_height,
            0
        ])
    )

    cutout = pipe(
        cube([
            runway_width,
            sd_height + runway_height - sd_top_height,
            thin_border
        ]),
        translate([
            thin_border + sd_total_width - runway_width,
            thin_border,
            sd_center_thickness
        ])
    )

    return body + plateau - cutout


def _body():
    body = cube([
        thin_border + sd_total_width + thin_border,
        thick_border + sd_height + thin_border,
        thin_border + sd_total_thickness
    ])

    retainer_1 = pipe(
        cube([
            sd_total_width - sd_width,
            thin_border,
            thin_border + sd_adapter_side_gap_thickness
        ]),
        translate([
            0,
            sd_height - thin_border,
            0
        ])
    )

    retainer_2 = cube([
        sd_total_width - sd_width,
        thin_border,
        thin_border + sd_adapter_side_gap_thickness
    ])

    primary_gap = pipe(
        cube([sd_total_width, sd_height, sd_total_thickness]) - retainer_1 - retainer_2,
        translate([thin_border, thin_border, thin_border]),
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
        ])
    )

    card_gap = pipe(
        cube([sd_width, thin_border, sd_total_thickness]),
        translate([
            thin_border + sd_total_width - sd_width,
            0,
            thin_border + sd_side_thickness
        ])
    )

    return body - primary_gap - side_gap - card_gap


def _sd_mount_screws():
    screw = pipe(
        _screw_mount(),
        translate([
            int((thin_border + sd_total_width - sd_width) / 2),
            int((runway_height + thin_border) / 4),
            0
        ])
    )

    top_screw = pipe(
        _screw_mount(),
        translate([
            int((thin_border + sd_total_width + thin_border) - (thick_border / 2)),
            thin_border + sd_height + int(thick_border / 2) + runway_height,
            0
        ])
    )

    return screw + top_screw


def _sd_mount():
    body = pipe(
        _body(),
        translate([0, runway_height, 0])
    )

    return body + _runway() - _sd_mount_screws()


def _sd_lid():
    lid = pipe(
        _lid(),
        translate([0, 0, thin_border + sd_center_thickness])
    )

    return lid - _sd_mount_screws()


# def _left_panel():
#     body = pipe(
#         cube(
#     )


def main():
    # final = _sd_mount() + _sd_lid()
    final = _sd_mount()

    scad_render_to_file(final, "build/kaptivator_sd_mount.scad")


if __name__ == "__main__":
    main()
