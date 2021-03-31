from ursina import *
import random
import math
from menu import *
from ursina.shaders import colored_lights_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from classes import TheCar, CheckPoint
from utils import collide 

window.vsync = False
app = Ursina()
level = load_blender_scene('flatland', reload=True)
score = 0
scene.fog_color = color.color(6, .1, .85)
inCar = False
# Create FP camera/ contorl
player = FirstPersonController(gravity=0)
camera.position = Vec3(0, 0, -20)

#level.start_point.enabled = False

for e in level.children:
    if not 'terrain' in e.name:
        e.shader = colored_lights_shader
    else:
        e.color = color.gray
        e.texture = 'shore'
    if "terrain" in e.name:
        e.collider = 'mesh'
    if "Cube" in e.name:
        e.collider = 'box'



bank = Vec3(-21, 2, -35)

car = Entity(model='cars/80scop', 
        texture='cars/cars', 
        position = (0, 0, 4), 
        scale=1,
        collider='box'
        )
CheckPoint.init_car(car)
CheckPoint.spawn_new()
arrow = Entity(model='cube', 
        color=color.orange, 
        position=car.position, 
        scale=(.2, .2, .5), 
        rotation=(0,0,0), 
        texture='shore'
        )

for pos in [(120,0,0), (-120,0,0), (0,0,120),(0,0,-120)]:
    Entity(
        model='cube',
        color=color.rgba(66,66,66,66),
        position=pos,
        scale=(abs(pos[2])*2+1, 5, abs(pos[0])*2+1),
        collider='box'
        )

cars = []
player_car = TheCar(0, 0, car)
cars.append(player_car)

speed_text = Text(text=f"Speed {player_car.speed}", 
        position=(0, -.4), 
        color=color.black
        )

pos_text = Text(text=f"Pos {player.position}", 
        position=(.3, .5), 
        color=color.black
        )

distance_text = Text(text=f"SCORE {score}", 
        position=(-.5, .5), 
        color=color.black
        )
ignore_list = [player, car, level.terrain]


def draw_scene():
    return


game_paused = True
inMenu = False


def update():
    global score
    if held_keys['q'] and held_keys['e']:
        quit()
    global steering, speed, forward, t, car, player_car, cars, game_paused, inMenu

    #  Game loop pause / play
    if game_paused:
        if not inMenu:
            invoke(showMainMenu)
            inMenu = True
    else:
        if main_menu.enabled:
            main_menu.enabled = False
            inMenu = False


        speed_text.text = f"Speed {round(player_car.speed*80, 1)} km/h"
        pos_text.text = f"Pos: {round(player.position[0],2), round(player.position[1],2), round(player.position[2],2)}"
        distance_text.text = f"SCORE {score}"
        #arrow.position = car.position + Vec3(0, 3, 0)
        arrow.rotation = arrow.look_at(bank, axis="forward")



        if held_keys['w']:
            for car in cars:
                car.w()
        if held_keys['a']:
            for car in cars:
                car.a()
        if held_keys['s']:
            for car in cars:
                car.s()
        if held_keys['d']:
            for car in cars:
                car.d()
        if held_keys['space']:
            for car in cars:
                car.brake(False)
        if not (held_keys['a'] or held_keys['d']):
            car.steering = 0
        player_car.move([*ignore_list, *CheckPoint.checkpoints])
        player_car.rotate()

        if not (held_keys['s'] or held_keys['w']):
            if player_car.speed > 0.001:
                player_car.brake(True)
            else:
                player_car.speed = None

        if player.camera_pivot.rotation_x < -10:
            player.camera_pivot.rotation_x = -10
        #print(player_car.steering, player_car.speed)


        for checkpoint in CheckPoint.checkpoints:
            if checkpoint.is_cleared([level]):
                score += 1
    player.position = player_car.ent.position


def input(key):
    global game_paused
    if key == 'escape':
        game_paused = not game_paused
    if held_keys['control'] and key == 'r':
        player_car.ent.position = Vec3(0, 0, 0)
        player_car.speed = None



Sky(texture='castaway_sky')
#EditorCamera()
app.run()
