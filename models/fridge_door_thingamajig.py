import functools
from solid import *
from shared.main import *


def main():
    segments = 200

    wall_w_top = 5.5
    wall_h_top = 9.75

    wall_w_bot = 3
    wall_h_bot = 6.75

    arm_length = 6

    bot_w = 19.25
    bot_h = 1.75
    bot_extension = 8
    bot_hole_d = 4.5
    bot_hole_from_edge = 3.5
    bot_hole_from_center = arm_length + bot_extension - bot_hole_from_edge

    wall_profile = polygon(
        points=[
            [0, 0],
            [0, wall_h_top],
            [wall_w_top, wall_h_top],
            [wall_w_bot, wall_h_bot],
            [wall_w_bot, bot_h],
            [bot_w / 2, bot_h],
            [bot_w / 2, 0]
        ]
    )

    wall_curve = pipe(
        wall_profile,
        rotate([0, 180, 0]),
        translate([bot_w / 2, 0, 0]),
        rotate_extrude(convexity=10, segments=segments)
    )

    wall_curve -= pipe(cube([50, 50, 50]), translate([0, -25, -25]))

    left_arm_offset = bot_w / -2

    left_arm = pipe(
        wall_profile,
        linear_extrude(height=arm_length, convexity=10),
        rotate([90, 0, 90]),
        translate([0, left_arm_offset, 0])
    )

    right_arm_offset = bot_w / 2

    right_arm = pipe(
        wall_profile,
        linear_extrude(height=arm_length, convexity=10),
        rotate([90, 0, -90]),
        translate([arm_length, right_arm_offset, 0])
    )

    extension = pipe(
        polygon(
            points=[
                [0, 0],
                [(bot_w - 16) / 2, bot_extension],
                [((bot_w - 16) / 2) + 16, bot_extension],
                [bot_w, 0]
            ]
        ),
        linear_extrude(height=bot_h, convexity=10),
        rotate([0, 0, -90]),
        translate([arm_length, bot_w / 2, 0])
    )

    screw_hole = pipe(
        cylinder(d=bot_hole_d, h=10, center=True, segments=segments),
        translate([bot_hole_from_center, 0, 0])
    )

    final = wall_curve + left_arm + right_arm + extension - screw_hole

    scad_render_to_file(final, "build/fridge_door_thingamajig.scad")


if __name__ == "__main__":
    main()
