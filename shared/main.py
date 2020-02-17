import solid


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
