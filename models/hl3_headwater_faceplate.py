from solid import *
from shared.main import *


padding = 1.5


screw_size = 2.5
screw_head_size = 5
screw_head_height = 2.5
screw_resolution = 30
screw_dist = 2.5 + padding


post_height = 6.2
post_size = screw_head_size + 2


face_length = 58 + (padding * 2)
face_width = 32 + (padding * 2)
face_height = screw_head_height + 1


window_length = 32
window_width = 14
window_dugout_length = 45
window_dugout_width = 26.5
window_x = (face_length / 2) - (window_length / 2)
window_y = (face_width / 2) - (window_width / 2)


screw_pos1 = [screw_dist, screw_dist];
screw_pos2 = [screw_dist, face_width - screw_dist];
screw_pos3 = [face_length - screw_dist, face_width - screw_dist];
screw_pos4 = [face_length - screw_dist, screw_dist];


def screw_hole(x, y):
    shaft_hole = cylinder(
        h=face_height + post_height, d=screw_size, segments=screw_resolution
    )

    head_hole = cylinder(
        h=screw_head_height, d=screw_head_size, segments=screw_resolution
    )

    return pipe(shaft_hole + head_hole, hole(), translate([x, y, 0]))


def mount_post(x, y):
    return pipe(
        cylinder(h=post_height, d=post_size, segments=screw_resolution),
        translate([x, y, face_height])
    )


# screen is 8.65mm high


def window():
    cutout = cube([window_length, window_width, face_height])
    dugout = pipe(
        cube([window_dugout_length, window_dugout_width, face_height - 1]),
        translate([
            (window_length - window_dugout_length) / 2,
            (window_width - window_dugout_width) / 2,
            1
        ])
    )

    return pipe(
        cutout + dugout,
        hole(),
        translate([window_x, window_y, 0])
    )


def main():
    base = cube([face_length, face_width, face_height])

    posts = mount_post(*screw_pos1) \
      + mount_post(*screw_pos2) \
      + mount_post(*screw_pos3) \
      + mount_post(*screw_pos4)

    screw_holes = screw_hole(*screw_pos1) \
                    + screw_hole(*screw_pos2) \
                    + screw_hole(*screw_pos3) \
                    + screw_hole(*screw_pos4)

    final = base + posts + window() + screw_holes

    scad_render_to_file(final, "build/hl3_headwater_faceplate.scad")


if __name__ == "__main__":
    main()
