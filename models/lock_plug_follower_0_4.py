from solid import *
from shared.lock_plug_follower import lock_plug_follower


def main():
    final = lock_plug_follower(
        res=300,
        body_height=85,
        body_diameter=10.1,
        cut_depth=5,
        mid_cut_width=5.5
    )

    scad_render_to_file(final, "build/lock_plug_follower_0_4.scad")


if __name__ == "__main__":
    main()
