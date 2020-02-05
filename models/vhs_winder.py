from solid import *
from shared.main import *


RES = 200


def _tip(w, h):
    return cylinder(h=h, d=w, segments=RES, center=True)


def _tooth(l, w, h, distance, angle):
    core = cube([l, w, h], center=True)
    tip = pipe(_tip(w, h), translate([l / 2, 0, 0]))
    return pipe(
        core + tip,
        translate([distance + (l / 2) - (w / 2), 0, 0]),
        rotate([0, 0, angle]),
    )


def _gear(
    inner_diameter: int,
    outer_diameter: int,
    height: int,
    tooth_count: int,
    tooth_width: int,
):
    core = cylinder(h=height, d=inner_diameter, segments=RES, center=True)

    tooth_length = outer_diameter - inner_diameter
    tooth_angle = 360 / tooth_count

    for i in range(tooth_count):
        angle = i * tooth_angle
        core += _tooth(tooth_length, tooth_width, height, inner_diameter / 2, angle)

    return core


def _handle(
    base_z: int,
    base_diameter: int,
    base_height: int,
    diameter: int,
    width: int
):
    base = cylinder(h=base_height, d=base_diameter, segments=RES, center=True)
    fan = pipe(
        cylinder(h=width, d=diameter, segments=RES, center=True),
        rotate([90, 0, 0]),
        translate([0, 0, diameter / 2])
    )

    return pipe(base + fan, translate([0, 0, base_z]))


def main():
    gear_inner_diameter = 15.25
    gear_outer_diameter = 17.5
    gear_height = 15
    tooth_count = 9
    tooth_width = 3

    base_height = 5
    base_diameter = gear_inner_diameter
    handle_diameter = gear_outer_diameter * 1.5
    handle_width = 2

    slop_scaling = 0.875

    gear = _gear(
        gear_inner_diameter, gear_outer_diameter, gear_height, tooth_count, tooth_width
    )

    handle = _handle(
        gear_height / 2,
        base_diameter,
        base_height,
        handle_diameter,
        handle_width
    )

    final = pipe(
        gear + handle,
        scale([slop_scaling, slop_scaling, slop_scaling])
    )

    scad_render_to_file(final, "build/vhs_winder.scad")


# TODO make one with dremel handle too
if __name__ == "__main__":
    main()
