from ursina import *

# 'distance', 'entities', 'entity', 'hit', 'hits', 'normal', 'point', 'world_normal', 'world_point' BOXCAST METHODS

def collide(position, direction, distance, ignore_list, speed):
    if boxcast(position, direction=direction, 
               distance=distance + speed, 
               thickness=(1.5, 2),
               traverse_target=scene, 
               ignore=ignore_list,
               debug=False
               ).entity is None:
        # print(boxcast(position, direction=direction, distance=distance, thickness=(2, 2),
               #traverse_target=scene, ignore=[player, car, level.terrain], debug=False).entity)
        pass  # This is here just avoiding us crashing for None

    elif boxcast(position, 
            direction=direction, 
            distance=distance + speed, 
            thickness=(1.5,2),
            traverse_target=scene, 
            ignore=ignore_list,
            debug=False
            ).entity != None:
        return True
    return False

def make_walls(width):
    walls = []
    for pos in [(width, 0, 0), (-width, 0, 0), (0, 0, width),(0, 0, -width)]:
        walls.append(Entity(
            model='cube',
            color=color.rgba(66,26,26,66),
            position=pos,
            scale=(abs(pos[2])*2+1, 5, abs(pos[0])*2+1),
            collider='box'
            ))
    return walls

def make_floor(tiles, size):
    floor = []
    for x in range(-tiles, tiles):
        for z in range(-tiles, tiles):
            floor.append(Entity(model='cube',
                                 color=color.rgb(70,40,40),
                                 position=(x*size, -1, z*size),
                                 scale=(size, 1, size),
                                 texture='assets/textures/gravel'
                                 ))
    return floor
# ---------------------------------------------------------------------------- #

# IGNORE LIST = [player, car, level.terrain]
