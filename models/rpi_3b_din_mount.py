from solid import *
from shared.main import *


#     C
#      \
#       \
# B-----|--| D
#       |
#       |
#       |--|
# B-----|--| E
#       A


def _spine(cfg):
    body = cube([cfg["length"], cfg["width"], cfg["height"] + 5]) # FIXME magic number

    pulltab_tip = pipe(
        cylinder(h=cfg["width"], d=cfg["length"], segments=RESOLUTION),
        rotate([270, 0, 0]),
        translate([
            cfg["length"] / 2,
            0,
            cfg["pulltab_height"]
        ])
    )

    pulltab = pipe(
        cube([cfg["length"], cfg["width"], cfg["pulltab_height"]]) + pulltab_tip,
        rotate([0, cfg["pulltab_angle"], 0]),
        translate([-6, 0, cfg["height"]]) # FIXME magic number (hook length)
    )

    return body + pulltab


def _arm(cfg):
    body = pipe(
        cube([cfg["length"], cfg["width"], cfg["height"]]),
        translate([cfg["length_offset"], 0, 0])
    )

    screw_hole = pipe(
        cylinder(h=cfg["post_width"], d=cfg["screw_size"], segments=RESOLUTION),
        hole()
    )

    post1 = pipe(
        cylinder(h=cfg["post_width"], d=cfg["height"], segments=RESOLUTION) + screw_hole,
        rotate([270, 0, 0]),
        translate([cfg["post1_pos"] + cfg["length_offset"], 0, cfg["height"] / 2])
    )

    post2 = pipe(post1, translate([cfg["post2_relative_pos"], 0, 0]))

    support1 = pipe(
        triangular_prism(cfg["width"], cfg["height"], cfg["height"]),
        rotate([180, 0, 270]),
        translate([cfg["height"] + cfg["length_offset"], cfg["width"], 0])
    )

    support2 = pipe(
        support1,
        rotate([180, 0, 0]),
        translate([0, cfg["width"], cfg["height"]])
    )

    return body + support1 + support2 + post1 + post2


def _mount(cfg):
    hook_thickness = cfg["hook_length"] - cfg["gap_length"]

    arm = cube([cfg["hook_length"], cfg["width"], hook_thickness])

    hook_tip = pipe(
        cylinder(h=cfg["width"], d=hook_thickness, segments=RESOLUTION),
        rotate([270, 0, 0]),
        translate([
            cfg["gap_length"] + (hook_thickness / 2),
            0,
            (cfg["hook_height"] / 2) + hook_thickness
        ])
    )

    hook = pipe(
        cube([
            hook_thickness,
            cfg["width"],
            (cfg["hook_height"] / 2) + hook_thickness
        ]),
        translate([cfg["gap_length"], 0, 0])
    )

    bumper_height = 10 # FIXME magic number

    bumper = pipe(
        cube([cfg["hook_length"], cfg["width"], bumper_height]),
        translate([0, 0, hook_thickness + cfg["gap_height"]])
    )

    return pipe(
        arm + hook + hook_tip + bumper,
        rotate([0, 180, 0]),
        translate([0, 0, cfg["height_offset"]])
    )


def main():
    spine_base_height = 58
    arm_height = 5.8

    spine_cfg = {
        "length": 5,
        "width": 24,
        "height": spine_base_height + (arm_height * 2),
        "pulltab_height": 30,
        "pulltab_angle": 45
    }

    arm_cfg = {
        "length": 52.5,
        "width": 4,
        "height": arm_height,
        "length_offset": spine_cfg["length"],
        "post_width": 5.8,
        "post1_pos": 3.6,
        "post2_relative_pos": 49,
        "screw_size": 2.5,
        "arm_spacing": 58
    }

    mount_cfg = {
        "height_offset": spine_cfg["height"],
        "width": spine_cfg["width"],
        "hook_length": 6,
        "hook_height": 2.8,
        "gap_length" : 2.25,
        "gap_height": 35.5,
        "arm_spacing": arm_cfg["arm_spacing"],
        "arm_height": arm_cfg["height"]
    }

    arm = pipe(
        _arm(arm_cfg),
        translate([0, 0, spine_cfg["height"] - arm_cfg["height"]])
    )

    arms = arm + pipe(arm, translate([0, 0, arm_cfg["arm_spacing"] * -1]))

    final = pipe(
        _spine(spine_cfg) + arms + _mount(mount_cfg),
        rotate([90, 0, 0])
    )

    scad_render_to_file(final, "build/rpi_3b_din_mount.scad")


if __name__ == "__main__":
    main()
