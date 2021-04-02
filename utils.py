from ursina import *

# 'distance', 'entities', 'entity', 'hit', 'hits', 'normal', 'point', 'world_normal', 'world_point' BOXCAST METHODS
def collide(position, direction, distance, ignore_list, speed):
    if boxcast(position, direction=direction, 
               distance=distance,  # + speed,
               thickness=(1.5, 2),
               traverse_target=scene, 
               ignore=ignore_list,
               debug=True
               ).entity is None:
        # print(boxcast(position, direction=direction, distance=distance, thickness=(2, 2),
        #traverse_target=scene, ignore=[player, car, level.terrain], debug=False).entity)
        # This is here just avoiding us crashing for None
        pass

    elif boxcast(position, 
            direction=direction, 
            distance=distance + speed * .8, 
            thickness=(1.5,2),
            traverse_target=scene, 
            ignore=ignore_list,
            debug=True
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
                                 color=color.rgb(140,60,44),
                                 position=(x*size, -1, z*size),
                                 scale=(size, 1, size),
                                 texture='assets/textures/dirt'
                                 ))
    return floor


def reset_game(player_car, obs, chk):
    player_car.hp = None
    player_car.speed = 0
    obs.clear_all()
    check = chk.checkpoints.pop()
    destroy(check.light, delay=0)
    destroy(check, delay=0)
    chk.spawn_new()
    

# ---------------------------------------------------------------------------- #

# IGNORE LIST = [player, car, level.terrain]
