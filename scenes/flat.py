from ursina import *
from time import perf_counter

scene_parent = Entity()

if __name__ == '__main__':
    app = Ursina()

t = perf_counter()

# unique meshes
meshes = {

'Plane_001' : Mesh(
    vertices=[(1.0, 0.0, -1.0), (-1.0, 0.0, 1.0), (-1.0, 0.0, -1.0), (1.0, 0.0, -1.0), (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0)],
    normals=[(0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0)],
    colors=[],
    uvs=[(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
),
}
print('loaded models:', perf_counter() - t)
t = perf_counter()

scene_parent.terrain = Entity(
    name='terrain',
    parent=scene_parent,
    position=Vec3(0.0, 0.0, 0.0),
    rotation=(-0.0, -0.0, -0.0),
    scale=Vec3(120.00003, 120.00003, 120.00003),
    model=deepcopy(meshes['Plane_001']),
    ignore=True,
    )
print('created entities:', perf_counter() - t)
if __name__ == '__main__':
    EditorCamera()
    app.run()
