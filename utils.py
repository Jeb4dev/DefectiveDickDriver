from ursina import *

def collide(position, direction, distance, ignore_list):
    if boxcast(position, direction=direction, 
               distance=distance, 
               thickness=(2, 2),
               traverse_target=scene, 
               ignore=ignore_list,
               debug=True
               ).entity is None:
        # print(boxcast(position, direction=direction, distance=distance, thickness=(2, 2),
               #traverse_target=scene, ignore=[player, car, level.terrain], debug=False).entity)
        pass  # This is here just avoiding us crashing for None

    elif boxcast(position, 
            direction=direction, 
            distance=distance, 
            thickness=(2,2),
            traverse_target=scene, 
            ignore=ignore_list,
            debug=True
            ).entity != None:
        return False
    return True



# IGNORE LIST = [player, car, level.terrain]
