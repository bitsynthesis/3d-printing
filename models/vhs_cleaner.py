from abc import ABC
from dataclasses import dataclass
import functools
import operator

from solid import *
from shared.main import *


RES = 200


def _cleaning_trough(width, depth, height):
    spacing = 3
    thickness = (depth - spacing) / 2
    side_1 = cube([width, thickness, height])
    side_2 = pipe(
        cube([width, thickness, height]), translate([0, thickness + spacing, 0])
    )
    return pipe(side_1 + side_2, translate([width / -2, depth / -2, 0]))


def _guide_post(base_diameter, base_height, foot_height, neck_height):
    """
    Create a post for mounting metal guide tube salvaged from a commercial VHS
    tape. Minimum base_diameter is 6 (mm).
    """
    base = pipe(
        cylinder(h=base_height, d=base_diameter, center=True, segments=RES),
        translate([0, 0, base_height / 2]),
    )

    foot = pipe(
        cylinder(h=foot_height, d=5, center=True, segments=RES),
        translate([0, 0, (foot_height / 2) + base_height]),
    )

    neck = pipe(
        cylinder(h=neck_height, d=4.5, center=True, segments=RES),
        translate([0, 0, (neck_height / 2) + base_height + foot_height]),
    )

    return base + foot + neck


def _pad(
    width,
    wing_width,
    tape_height,
    top_tab_height,
    bottom_tab_height,
    thickness,
    tab_thickness,
):
    pad_depth = 1

    # bottom tab
    bottom_tab = pipe(
        cube([width, tab_thickness, bottom_tab_height]),
        center(0, width),
        translate([0, pad_depth, 0]),
    )

    # bottom tab pad connector
    bottom_tab_pad_connector = pipe(
        cube([width, pad_depth, thickness]),
        center(0, width),
        translate([0, thickness, bottom_tab_height]),
    )

    # pad
    pad_height = tape_height + (thickness * 2)
    pad_width = width
    pad = pipe(
        cube([pad_width, thickness, pad_height]),
        center(0, pad_width),
        translate([0, 0, bottom_tab_height]),
    )

    # top tab pad connector
    top_tab_pad_connector = pipe(
        cube([width, pad_depth, thickness]),
        center(0, width),
        translate([0, thickness, bottom_tab_height + pad_height - thickness]),
    )

    # top tab
    top_tab = pipe(
        cube([width, tab_thickness, top_tab_height]),
        center(0, width),
        translate([0, pad_depth, bottom_tab_height + pad_height]),
    )

    # left wing

    # right wing

    return bottom_tab + bottom_tab_pad_connector + pad + top_tab_pad_connector + top_tab


def _outside_pad(gap_width, total_width, body_height, body_thickness, pad_height):

    tab_width = 10
    tab_middle_overhang = 6
    tab_height = pad_height
    full_tab_width = tab_width + tab_middle_overhang

    tab_1 = pipe(
        cube([full_tab_width, 1, tab_height]),
        translate([((gap_width / 2) + tab_width) * -1, body_thickness, body_thickness]),
    )

    tab_2 = pipe(
        cube([full_tab_width, 1, tab_height]),
        translate(
            [(gap_width / 2) - tab_middle_overhang, body_thickness, body_thickness]
        ),
    )

    middle = pipe(
        cube([gap_width, body_thickness, body_height]),
        translate([gap_width / -2, 0, 0]),
    )

    return tab_1 + middle + tab_2


def _inside_pad(
    pad_width, body_thickness, tab_width, tab_height, body_height, pad_height
):
    pad = pipe(
        cube([pad_width, body_thickness, pad_height]),
        translate([pad_width / -2, 0, tab_height]),
    )

    bottom_tab_1 = pipe(
        cube([tab_width, body_thickness, tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / 4, 0, 0]),
    )

    bottom_tab_2 = pipe(
        cube([tab_width, body_thickness, tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / -4, 0, 0]),
    )

    top_tab_height = body_height - body_thickness - pad_height
    top_tab_1 = pipe(
        cube([tab_width, body_thickness, top_tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / 4, 0, body_thickness + pad_height]),
    )

    top_tab_2 = pipe(
        cube([tab_width, body_thickness, top_tab_height]),
        translate([tab_width / -2, 0, 0]),
        translate([pad_width / -4, 0, body_thickness + pad_height]),
    )

    return pad + bottom_tab_1 + bottom_tab_2 + top_tab_1 + top_tab_2


class ModelComponent(ABC):
    combiner = operator.add

    def generate(self, state):
        raise NotImplementedError("ModelComponent must implement render method")


class BottomComponent(ModelComponent):
    def generate(self, state):
        bottom = pipe(
            cube(
                [
                    state.body_width,
                    state.body_depth,
                    state.body_thickness,
                ]
            ),
            translate([state.body_width / -2, 0, 0]),
        )

        front_wall = pipe(
            cube(
                [
                    state.body_width,
                    state.body_thickness,
                    state.bottom_height,
                ]
            ),
            translate([state.body_width / -2, 0, 0]),
        )

        back_wall = pipe(
            cube(
                [
                    state.body_width,
                    state.body_thickness,
                    state.bottom_height,
                ]
            ),
            translate(
                [
                    state.body_width / -2,
                    state.body_depth - state.body_thickness,
                    0,
                ]
            ),
        )

        side_wall_1 = pipe(
            cube(
                [
                    state.body_thickness,
                    state.body_depth,
                    state.bottom_height,
                ]
            ),
            translate([state.body_width / -2, 0, 0]),
        )

        side_wall_2 = pipe(
            cube(
                [
                    state.body_thickness,
                    state.body_depth,
                    state.bottom_height,
                ]
            ),
            translate([(state.body_width / 2) - state.body_thickness, 0, 0]),
        )

        spool_hole_1 = pipe(
            cylinder(h=10, d=state.spool_hole_diameter, center=True, segments=RES),
            translate([-46, 54, 0]),
        )

        spool_hole_2 = pipe(
            cylinder(h=10, d=state.spool_hole_diameter, center=True, segments=RES),
            translate([46, 54, 0]),
        )

        # TODO override here...
        bottom = pipe(
            cube([state.body_width, state.body_depth, state.bottom_height]),
            translate([state.body_width / -2, 0, 0]),
        )

        return (
            bottom
            - spool_hole_1
            - spool_hole_2
            - state.components["dummy_spools"].generate(state)
            # + front_wall
            # + back_wall
            # + side_wall_1
            # + side_wall_2
        )


class TapePathComponent(ModelComponent):
    base_height = 1
    foot_height = 2.5
    neck_height = 5.5
    guide_post_diameter = 8

    # minus 1 for base overhang
    guide_post_from_front = 6

    # minus 1 for base overhang
    guide_post_from_side = 20

    def translate_post(self, state, post, side="right"):
        x1 = self.guide_post_diameter / 2
        x2 = (state.body_width / 2) - state.body_thickness - self.guide_post_from_side

        if side == "left":
            x1 *= -1
            x2 *= -1

        return pipe(
            post,
            translate([
                x1,
                self.guide_post_diameter / 2,
                state.body_thickness,
            ]),
            translate([
                x2,
                self.guide_post_from_front + state.body_thickness,
                0,
            ])
        )

    def generate(self, state):

        guide_post_left = self.translate_post(
            state,
            _guide_post(
                self.guide_post_diameter,
                self.base_height,
                self.foot_height,
                self.neck_height,
            ),
            "left",
        )

        guide_post_right = self.translate_post(
            state,
            _guide_post(
                self.guide_post_diameter,
                self.base_height,
                self.foot_height,
                self.neck_height,
            ),
            "right",
        )

        return guide_post_left + guide_post_right


class TapePath2Component(ModelComponent):
    combiner = operator.sub

    clearance_width = 5

    def new_clearance(self, state, side="right"):
        tp = state.components["tape_path"]

        full_height = tp.base_height + tp.foot_height + tp.neck_height
        clearance = pipe(
            cylinder(
                h=full_height,
                d=tp.guide_post_diameter + (self.clearance_width * 2),
                center=True,
                segments=RES,
            ),
            translate([0, 0, full_height / 2]),
        )
        clearance -= tp.generate(state)

        return tp.translate_post(state, clearance, side)

    def generate(self, state):
        tp = state.components["tape_path"]

        clearance_left = self.new_clearance(state, "left")
        clearance_right = self.new_clearance(state, "right")

        return clearance_left + clearance_right


class DummySpoolsComponent(ModelComponent):
    def generate(self, state):
        dummy_spool_1 = pipe(
            cylinder(
                h=state.spool_height, d=state.spool_width, center=True, segments=RES
            ),
            translate([-46, 0, 0]),
        )

        dummy_spool_2 = pipe(
            cylinder(
                h=state.spool_height, d=state.spool_width, center=True, segments=RES
            ),
            translate([46, 0, 0]),
        )

        return pipe(
            dummy_spool_1 + dummy_spool_2,
            translate([0, 54, (state.spool_height / 2) + state.body_thickness]),
        )


class VHSCleaner(SceneComponent):
    def __init__(self):
        self.body_width = 188
        self.body_depth = 102
        self.body_thickness = 1.25
        self.body_height = 25
        self.spool_hole_diameter = 34
        # extra 2 is for amount it can move in the hole
        self.spool_width = 88.5 + 2
        self.spool_height = 16.25
        self.bottom_height = self.body_height / 2
        self.top_height = self.body_height / 2
        self.tape_plane_height = 16

        # self.cleaning_trough_width = 160
        # self.cleaning_trough_depth = 6

        # DEBUG
        # self.body_height = 5

        self.components = {
            "bottom": BottomComponent(),
            "tape_path": TapePathComponent(),
            "tape_path_2": TapePath2Component(),
            "dummy_spools": DummySpoolsComponent(),
        }


def main():
    # TODO
    # - establish tape path / plane
    #   - move posts toward center in both dimensions
    # - fill for structure and spool retention
    # - cleaning pads
    # - top / case
    # - cutouts on front required to insert in VCR

    VHSCleaner().render(
        path="build/vhs_cleaner.scad",
        component_keys=[
            # "bottom",
            "tape_path",
            "tape_path_2",
            # "dummy_spools",
        ],
    )


if __name__ == "__main__":
    main()
