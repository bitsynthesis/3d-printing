import math
from solid import *
from shared.main import *


def lock_plug_follower(body_height, body_diameter, cut_depth, mid_cut_width, res):
    body = cylinder(
        h=body_height,
        d=body_diameter,
        segments=res
    )

    half_cut = pipe(
        cube([body_diameter, body_diameter, cut_depth]),
        translate([0, -1 * (body_diameter / 2), body_height - cut_depth]),
        rotate([0, 0, 90]),
        hole()
    )

    mid_cut = pipe(
        cube([body_diameter, mid_cut_width, cut_depth], center=True),
        translate([0, 0, cut_depth / 2]),
        hole()
    )

    mid_cut_arm = mid_cut_width / math.sqrt(2.0)
    mid_wedge_height = (math.sqrt(2.0) * mid_cut_arm) / 2

    mid_wedge_cut = pipe(
        triangular_prism(body_diameter, mid_cut_arm, mid_cut_arm),
        translate([0, -1 * mid_cut_arm, 0]),
        rotate([135, 0, 0]),
        translate([-1 * (body_diameter / 2), 0, mid_wedge_height + cut_depth]),
        hole()
    )

    return body + half_cut + mid_cut + mid_wedge_cut
