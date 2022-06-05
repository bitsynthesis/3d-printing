from abc import ABC
import operator

import solid
import solid_state


RESOLUTION=50


def pipe(target, *fns):
    for fn in fns:
        target = fn(target)
    return target


def pipe_noop(x):
    return x


def triangular_prism(l, w, h):
    return solid.polyhedron(
       points=[[0, 0, 0], [l, 0, 0], [l, w, 0], [0, w, 0], [0, w, h], [l, w, h]],
       faces=[[0, 1, 2, 3], [5, 4, 3, 2], [0, 4, 5, 1], [0, 3, 4], [5, 2, 1]]
    )


def tube(h, d, thickness, **kwargs):
    positive = solid.cylinder(h=h, d=d, **kwargs)
    negative = pipe(
        solid.cylinder(h=h + 2, d=d - thickness, **kwargs),
        solid.translate([0, 0, -1])
    )
    return positive - negative


def center(axis, length):
    """
    axis: 0 (x), 1 (y), 2 (z)
    """
    adjustment = length / -2
    translation = [0, 0, 0]
    translation[axis] = adjustment
    return solid.translate(translation)


def in_to_mm(inches):
    return inches * 25.4


# TODO move to solid_state
def sub(element):
    return lambda x: x - element


# TODO move to solid_state
def add(element):
    return lambda x: x + element


# # TODO hold state of the object? ex. position and actual solid object
# class ModelComponent(ABC):
#     combiner = operator.add
#
#     def generate(self, state):
#         raise NotImplementedError("ModelComponent must implement render method")
#
#
# class SceneComponent(ABC):
#     def render(self, path, component_keys):
#         alpha = 0.65
#
#         # TODO more...
#         colors = [
#             "maroon",
#             "olive",
#             "green",
#             "teal",
#             "navy",
#             "purple",
#         ]
#
#         combined = pipe(
#             self.components[component_keys[0]].generate(self),
#             solid.color(colors[0], alpha=alpha),
#         )
#         for i, k in enumerate(component_keys[1:]):
#             component = self.components[k]
#             generated = pipe(
#                 component.generate(self), color(colors[i + 1], alpha=alpha)
#             )
#             combined = component.combiner(combined, generated)
#
#         solid.scad_render_to_file(combined, path)
#
#
# # TODO
# # - get child component by name
# # - get attributes of child component by name
#
#
# # TODO rename save_state?
# def save_state(name, attributes):
#     """
#     Add solid_state metadata to an object.
#     """
#     def _solid_state(scad_obj):
#         scad_obj.add_trait("solid_state", dict(name=name, attributes=attributes))
#         return scad_obj
#     return _solid_state
#
#
# # TODO
# # rename get_state
# # attribute optional (returns all attributes by default)
# # take name argument so you don't have to look up the scad_obj first
# # or...
# # rename get_attributes and let the user look up in the dict
# def get_attribute(scad_obj, attribute):
#     """
#     Get the solid_state attribute of an object, if it has one.
#     """
#     if state := scad_obj.get_trait("solid_state"):
#         return state["attributes"].get(attribute)
#
#     return None
#
#
# def get_name(scad_obj):
#     """
#     Get the solid_state name of an object, if it has one.
#     """
#     if state := scad_obj.get_trait("solid_state"):
#         return state["name"]
#
#     return None
#
#
# # TODO instead of building up list of objs directly,
# # build up objs and any transformations found on the path to them.
# # return like... {"objs": [], "transformations": []}
# def get_objects(scad_obj, name, objs = None):
#     """
#     Get all objects with the given solid_state name.
#     """
#     if objs is None:
#         objs = []
#
#     if get_name(scad_obj) == name:
#         objs.append(scad_obj)
#
#     for child in scad_obj.children:
#         objs = get_objects(child, name, objs)
#
#     return objs
#
#
# def get_object(scad_obj, name):
#     """
#     Get a single object with a given solid_state name. Throws an exception
#     if a single match is not found.
#     """
#     objects = get_objects(scad_obj, name)
#     num_objects = len(objects)
#     if num_objects == 1:
#         return objects[0]
#
#     raise Exception(f"{num_objects} found when 1 was expected")
#
#
# # TODO get objects by name path (specific parent / child relationships)
# # ex. get_object_by_path(scad_obj, "body", "tape_path", "guide_post")
# #     get_object_by_path(scad_obj, "body.tape_path.guide_post")
# #
# # maybe best to allow name _or_ path wherever name is used
# # ex. get_object("guide_post")
# #     get_object("body.tape_path.guide_post")


# TODO
# - move to solid_state
# - could allow rendering in place (how it currently works)
#   OR rendering selected states with transformations applied
#   to get them to their location in final state (scad_obj)
# - names should really be a single query (or at least a list
#   of queries, but given that queries already support lists
#   of paths that seems odd. this has some implications for
#   how groups of objects are colored
def render_objects(scad_obj, names, file_path, transform=True, colorize=True):
    """
    Render all objects with matching solid_state names to file.
    """
    # TODO support color schemes, also cycle to not overflow
    colors = [
        "maroon",
        "olive",
        "green",
        "teal",
        "navy",
        "purple",
    ]

    combined = solid.cube([0, 0, 0])
    for i, name in enumerate(names):
        objects = solid_state.get_objects(scad_obj, name)
        if transform is True:
            # TODO should get_transformations just return composed already?
            # will i ever want to do anything but apply them as a whole?
            transformations = map(
                lambda t: solid_state.compose(*t),
                solid_state.get_transformations(scad_obj, name)
            )

            objects = [
                func(obj) for func, obj in zip(transformations, objects)
            ]

        if colorize is True:
            objects = map(solid.color(colors[i]), objects)

        for obj in objects:
            combined += obj

    print(combined)

    solid.scad_render_to_file(combined, file_path)


# # TODO
# # - get all transformations that happened to an object after a given state.
# #   so like... find matching object, record any transformations encountered
# #   along the way (translate, rotate, mirror...) and compose them into a new
# #   function
#
#
# def get_transformations(scad_obj, name):
#
