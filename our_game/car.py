from ursina import *
import random
import math
from ursina.shaders import colored_lights_shader

window.vsync = False
app = Ursina()
level = load_blender_scene('flat', reload=True)
#level = load_blender_scene('flat', reload=True)

scene.fog_color = color.color(6, .1, .85)
inCar = False

# Create FP camera/ contorl
from ursina.prefabs.first_person_controller import FirstPersonController
player = FirstPersonController(gravity=0)
camera.position = Vec3(0, 0, -20)

level.start_point.enabled = False

for e in level.children:
    if not 'terrain' in e.name:
        e.shader = colored_lights_shader
    if "terrain" in e.name:
        e.collider = 'mesh'
    # if "car" in e.name:
    #     e.collider = 'box'
    if "Cube" in e.name:
        e.collider = 'box'
    if "palm" in e.name:
        e.collider = 'mesh'
    if "pebble" in e.name:
        e.collider = 'mesh'



gunshot = Audio(sound_file_name='gunshot', pitch=1, loop=False, autoplay=False)

stearing = 0

speed = 0

bank = Vec3(-21, 2, -35)
speed_text = Text(text=f"Speed {speed}", position=(0, -.4), color=color.black)
pos_text = Text(text=f"Pos {player.position}", position=(.3, .5), color=color.black)
distance_text = Text(text=f"Distance to bank {player.position-bank}", position=(-.5, .5), color=color.black)

arrow = Entity(model='cube', color=color.orange, position=level.car.position, scale=(2, .2, 5), rotation=(0,0,0), texture='shore')
# level.Cylinder.position = bank
# level.Cylinder.texture = "shore"
# level.Cylinder.color = color.rgba(255,255,255,128)
cube2 = Entity(model='circle', color=color.rgba(255, 255, 0, 64), position=bank, billboard=True, scale=(20, 20, 20), double_sided=True)


def update():
    global stearing, speed, forward, t

    speed_text.text = f"Speed {round(speed*80, 0)} km/h"
    pos_text.text = f"Pos: {round(player.position[0],2), round(player.position[1],2), round(player.position[2],2)}"
    distance_text.text = f"Distance to bank {round(distance(player.position,bank), 3)}"
    arrow.position = level.car.position + Vec3(0, 3, 0)
    arrow.rotation = arrow.look_at(bank, axis="forward")

    if abs(speed) < 0.00001:
        speed = 0
        forward = None

    if forward == None:
        if held_keys['w']:
            forward = True

    if forward:
        if held_keys['w']:
            l_time = math.asin(speed)
            speed = getSpeed(l_time + time.dt * .2)
        if held_keys['space'] or held_keys['s']:
            l_time = math.acos(speed)
            speed = breakForce(l_time + time.dt * .6)
    else:
        if held_keys['s']:
            forward = False
            l_time = math.asin(speed)
            speed = getSpeed(l_time + time.dt * .2)
        if held_keys['space'] or held_keys['w']:
            l_time = math.acos(speed)
            speed = breakForce(l_time + time.dt * .6)


    if held_keys['a']:
        stearing = -.20
    elif held_keys['d']:
        stearing = .20
    else:
        stearing = 0


    if forward == None or abs(speed) < 0.1:
        stearing = 0

    player.position = level.car.position
    level.car.rotation += Vec3(0, stearing, 0)
    if forward:
        if not collide(level.car.position, level.car.left, 8):
            speed = 0
        if speed > 0:
            level.car.position += level.car.left * speed / 10
        elif speed < 0:
            level.car.position -= level.car.left * -speed / 10
    else:
        if not collide(level.car.position, level.car.right, 8):
            speed = 0
        if speed > 0:
            level.car.position += level.car.left * -speed / 10
        elif speed < 0:
            level.car.position -= level.car.left * speed / 10
    #camera.position = level.car.position - Vec3(0, 0, 20)

    if not held_keys['s'] and not held_keys['w']:
        if speed > 0.1:
            speed *= .999
        else:
            speed = 0

    if player.camera_pivot.rotation_x < -10:
        player.camera_pivot.rotation_x = -10


def collide(position, direction, distance):
    if boxcast(position, direction=direction, distance=distance, thickness=(5, 3),
               traverse_target=scene, ignore=[player, level.car, level.terrain], debug=False).entity is None:
        pass  # This is here just avoiding us crashing for None
    elif boxcast(position, direction=direction, distance=distance, thickness=(5,3),
                       traverse_target=scene, ignore=[player, level.car, level.terrain], debug=False).entity != None:
        return False
    return True


def getSpeed(time):
    if - 1.6 < time < 1.6:
        speed = math.sin(time)
    else:
        speed = math.sin(math.pi/2)
    return speed


def breakForce(time):
    if time < 1.6:
        speed = math.cos(time)
    else:
        speed = math.cos(math.pi / 2)
    return speed

forward = None


def input(key):
    pass

Sky(texture='castaway_sky')
#EditorCamera()
app.run()
