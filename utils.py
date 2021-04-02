from ursina import *
import json


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
        # traverse_target=scene, ignore=[player, car, level.terrain], debug=False).entity)
        # This is here just avoiding us crashing for None
        pass

    elif boxcast(
            position,
            direction=direction,
            distance=distance + speed * .8,
            thickness=(1.5,2),
            traverse_target=scene,
            ignore=ignore_list,
            debug=True
            ).entity is not None:
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


def reset_game(player_car, obs, chk, menu):
    player_car.new_game = True
    player_car.hp = None
    player_car.speed = 0
    obs.clear_all()
    check = chk.checkpoints.pop()
    destroy(check.light, delay=0)
    destroy(check, delay=0)
    chk.spawn_new()
    
    try:
        with open('scores.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    # print(data)
    data[time.strftime('%X %x')] = player_car.score
    # print(data)
    sorted_scores =  {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    # print(sorted_scores)
    # print(len(data))

    counter = 0
    new_high_score = False
    top_five = {}
    for date, score in sorted_scores.items():
        # print(date, score, counter)
        if counter == 0 and score <= player_car.score:
            new_high_score = True
            # print('new high score')
        top_five[date] = score
        counter += 1
        if counter > 5:
            break
    with open('scores.json', 'w') as f:
        json.dump(top_five, f)

    menu.show_score_menu(new_high_score)


