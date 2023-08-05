### Cube ###

from tiny_3d_engine import (Engine3D, Scene3D, Part3D)

points = [
    [-1., -1., -1.],
    [-1., -1., 1.],
    [-1., 1., 1.],
    [-1., 1., -1.],
    [1., -1., -1.],
    [1., -1., 1.],
    [1., 1., 1.],
    [1., 1., -1.]
]
triangles = [
    [0, 1, 2],
    [0, 2, 3],
    [2, 3, 7],
    [2, 7, 6],
    [1, 2, 5],
    [2, 5, 6],
    [0, 1, 4],
    [1, 4, 5],
    [4, 5, 6],
    [4, 6, 7],
    [3, 7, 4],
    [4, 3, 0]
]

scene = Scene3D()
scene.add_or_update_part("cube", points, triangles, color="#0000ff")

scene.add_axes()

test = Engine3D(scene, title="The cube example")

test.clear()
test.rotate('y', 0.1)
test.rotate('x', 0.1)
test.render()
test.mainloop()
