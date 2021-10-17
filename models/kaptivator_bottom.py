from solid import *
from shared.main import *


body_width = 296
body_height = 230
body_thickness = 2.5


hole_width = 3.5
hole_height = 5.5
hole_segments = 32


access_hole_height = 65
access_hole_width = 36


def screw_hole(x, y):
    """
    Create an oblong screw hole, with x and y representing the left and top.
    """
    a = cylinder(h=body_thickness, d=hole_width, segments=hole_segments)

    b = pipe(
        cylinder(h=body_thickness, d=hole_width, segments=hole_segments),
        translate([0, hole_height - hole_width, 0])
    )

    return pipe(
        a + b,
        hull(),
        hole(),
        translate([x, y, 0]),
        translate([hole_width / 2, hole_width / 2, 0]),
        translate([0, hole_height * -1, 0])
    )


def access_hole():
  return pipe(
      cube([access_hole_width, access_hole_height, body_thickness]),
      translate([body_width - 116, 25, 0]),
      hole()
  )


def debug_holes():
  debug_1 = pipe(
      cube([116, 190, body_thickness]),
      translate([20, 20, 0]),
      hole()
  )

  debug_2 = pipe(
      cube([body_width - 20 - 146 - 3.5 - 10, body_height - 20 - 110, body_thickness]),
      translate([146 + 3.5 + 10, 110, 0]),
      hole()
  )


  return debug_1 + debug_2


def main():
    body = cube([body_width, body_height, body_thickness])

    #  0      1      2
    #
    #
    # 3               4
    #
    # 5               6
    # 7       8       9

    hole_0 = screw_hole(14.5, body_height - hole_height - 4)
    hole_1 = screw_hole(146.5, body_height - hole_height - 4)
    hole_2 = screw_hole(body_width - hole_width - 14.5, body_height - hole_height - 4)
    hole_3 = screw_hole(3.75, body_height - 82.75)
    hole_4 = screw_hole(body_width - hole_width - 3.75, body_height - 82.75)
    hole_5 = screw_hole(3.75, hole_height + 63.25)
    hole_6 = screw_hole(body_width - hole_width - 3.75, hole_height + 63.25)
    hole_7 = screw_hole(3.75, hole_height + 3.75)
    hole_8 = screw_hole(146.5, hole_height + 3.75)
    hole_9 = screw_hole(body_width - hole_width - 3.75, hole_height + 3.75)

    final = body \
        + hole_0 \
        + hole_1 \
        + hole_2 \
        + hole_3 \
        + hole_4 \
        + hole_5 \
        + hole_6 \
        + hole_7 \
        + hole_8 \
        + hole_9 \
        + access_hole() \
        + debug_holes()

    # final = cube([10, 10, 1], center=True) + screw_hole(0, 0)

    scad_render_to_file(final, "build/kaptivator_bottom.scad")


if __name__ == "__main__":
    main()
