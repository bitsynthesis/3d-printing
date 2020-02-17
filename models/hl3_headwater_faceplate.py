from solid import *
from shared.main import *


# configurable values


padding = 2

screw_size = 2.5
screw_head_size = 5
screw_head_height = 2.5
screw_resolution = 30
screw_dist = 2.5 + padding
post_height = 5.2
post_size = screw_size + 3.5

face_length = 58 + (padding * 2)
face_width = 32 + (padding * 2)
face_height = screw_head_height + 1

window_length = 32
window_width = 14

window_x = (face_length / 2) - (window_length / 2)
window_y = (face_width / 2) - (window_width / 2)

resolution = 30


# calculated values


screw_pos_1 = [screw_dist, screw_dist]
screw_pos_2 = [screw_dist, face_width - screw_dist]
screw_pos_3 = [face_length - screw_dist, face_width - screw_dist]
screw_pos_4 = [face_length - screw_dist, screw_dist]


def _screw_head_hole():
    return cylinder(
        h=screw_head_height,
        d=screw_head_size,
        segments=resolution
    )


def _screw_shaft_hole():
    return cylinder(
        h=face_height + post_height,
        d=screw_size,
        segments=resolution
    )


def _screw_hole(position):
    return pipe(
        _screw_shaft_hole() + _screw_head_hole(),
        translate([position[0], position[1], 0])
    )


def _lcd_mount_post(position):
    post = pipe(
        cylinder(
            h=post_height,
            d=post_size,
            segments=resolution
        ),
        translate([position[0], position[1], face_height])
    )
    return post - _screw_hole(position)


def _lcd_window():
    return pipe(
        cube([window_length, window_width, face_height]),
        translate([window_x, window_y, 0])
    )


def _body():
    return cube([face_length, face_width, face_height])


def main():
    lcd_mount_1 = _lcd_mount_post(screw_pos_1)
    lcd_mount_2 = _lcd_mount_post(screw_pos_2)
    lcd_mount_3 = _lcd_mount_post(screw_pos_3)
    lcd_mount_4 = _lcd_mount_post(screw_pos_4)

    final = lcd_mount_1

    final = _body() \
        + lcd_mount_1 \
        + lcd_mount_2 \
        + lcd_mount_3 \
        + lcd_mount_4 \
        - _lcd_window()

    scad_render_to_file(final, "build/hl3_headwater_faceplate.scad")


if __name__ == "__main__":
    main()
