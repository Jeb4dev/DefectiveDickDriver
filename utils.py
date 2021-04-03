from ursina import *
from story import *
import json


# 'distance', 'entities', 'entity', 'hit', 'hits', 'normal', 'point', 'world_normal', 'world_point' BOXCAST METHODS
def collide(position, direction, distance, ignore_list, speed):
    if boxcast(position, direction=direction,
               distance=distance,  # + speed,
               thickness=(1.5, 2),
               traverse_target=scene,
               ignore=ignore_list,
               debug=False
               ).entity is None:
         pass

    elif boxcast(
            position,
            direction=direction,
            distance=distance + speed * .8,
            thickness=(1.5, 2),
            traverse_target=scene,
            ignore=ignore_list,

            debug=False
            ).entity is not None:
        return True
    return False


def make_walls(width):
    walls = []
    for pos in [(width, 0, 0), (-width, 0, 0), (0, 0, width), (0, 0, -width)]:
        walls.append(Entity(
            model='cube',
            color=color.rgba(66, 26, 26, 66),
            position=pos,
            scale=(abs(pos[2]) * 2 + 1, 5, abs(pos[0]) * 2 + 1),
            collider='box'
        ))
    return walls


def make_floor(tiles, size):
    floor = []
    for x in range(-tiles, tiles):
        for z in range(-tiles, tiles):
            floor.append(Entity(model='cube',
                                color=color.rgb(140, 60, 44),
                                position=(x * size, -1, z * size),
                                scale=(size, 1, size),
                                texture='assets/textures/dirt'
                                ))
    return floor


def reset_game(player_car, obs, chk, menu):
    player_car.lights = False
    player_car.light_time = 100
    player_car.new_game = True
    player_car.hp = None
    player_car.speed = 0
    player_car.story_time = time.time() + 10
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
    data[time.strftime('%X %x')] = player_car.score
    sorted_scores = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

    counter = 0
    new_high_score = False
    top_five = {}
    for date, score in sorted_scores.items():
        if counter == 0 and score <= player_car.score:
            new_high_score = True
        top_five[date] = score
        counter += 1
        if counter > 5:
            break
    with open('scores.json', 'w') as f:
        json.dump(top_five, f)

    menu.show_score_menu(new_high_score, get_story()[-1])
    new_story()

