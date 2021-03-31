from ursina import *
import random
import math
from menu import *
from ursina.shaders import colored_lights_shader
from ursina.prefabs.first_person_controller import FirstPersonController

from classes import TheCar, CheckPoint, Lighting, Obstacle
from utils import collide
from ursina.shaders import lit_with_shadows_shader # you have to apply this shader to enties for them to recieve shadows.


from ursina.shaders import *

app = Ursina()

window.fullscreen_size = (1920, 1080, 32)
window.fullscreen = True
window.vsync = True
level = load_blender_scene('flat', reload=True)

score = 0
scene.fog_color = color.rgb(35, 20, 20)
scene.fog_density = (10, 40)
# inCar = False
# Create FP camera/ contorl
player = FirstPersonController(gravity=0)
camera.position = Vec3(0, 0, -20)

#level.start_point.enabled = False

for e in level.children:
    if "terrain" in e.name:
        e.collider = 'mesh'
        e.color = color.gray
        e.texture = 'shore'
    if "Cube" in e.name:
        e.collider = 'box'
        e.shader = lit_with_shadows_shader
        multiplier = random.randint(0,3)
        e.color = color.rgba(196, multiplier*32, multiplier*32, 0)
        e.position += Vec3(random.randint(-5, 5), 0, random.randint(-5, 5))

light = Lighting(player, player.position+Vec3(1, 7, 0), color.blue)

level.terrain.scale = 2000

bank = Vec3(-21, 2, -35)

# basic_lighting_shader - no colored light
# colored_lights_shader -- just white
# fading_shadows_shader -- doesnt exist
# fresnel_shader -- doesnt exist
# lit_with_shadows_shader -- apply color existing white
# matcap_shader -- mirror finish
# normals_shader -- rainbow
# texture_blend_shader -- doesnt exist
# triplanar_shader -- car .png colors
# unlit_shader - no colored light
# __init__
car = Entity(model='cars/80scop', 
        texture='cars/cars', 
        position = (0, 0, 4), 
        scale=1,
        collider='box'
        )
CheckPoint.init_car(car)
Obstacle.init_car(car)
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
        color=color.white66
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
mouse.visible = False
ems_lighting = False
music = Audio('assets/music/backaround_music', pitch=1, loop=True, autoplay=True, volume=.1)
siren_audio = Audio('assets/music/siren', pitch=1, loop=True, autoplay=False, volume=.2)

def update():

    global score
    if held_keys['q'] and held_keys['e']:
        quit()
    global steering, speed, forward, t, car, player_car, cars, game_paused, inMenu, pos_text, speed_text, distance_text

    #  Game loop pause / play
    if game_paused:

        # Entity(billboard=True, scale=Vec3(10, 10, 10), color=color.black, model="plane", rotation=(-90, 0, 0))
        if not inMenu:
            invoke(changePos, player.position)
            invoke(showMainMenu)
            dis_able_menu()
    else:
        if main_menu.enabled:
            main_menu.enabled = False
            dis_able_menu()

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


        if player.camera_pivot.rotation_x < 5:
            player.camera_pivot.rotation_x = 5

        #print(player_car.steering, player_car.speed)


        for checkpoint in CheckPoint.checkpoints:
            if checkpoint.is_cleared([level]):
                score += 1

                Obstacle.shuffle()

                for e in level.children:
                    if "Cube" in e.name:
                        e.position += Vec3()

        player.position = player_car.ent.position
        if ems_lighting:
            #['_STRUCT_TM_ITEMS', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'altzone', 'asctime', 'ctime', 'daylight', 'dt', 'get_clock_info', 'gmtime', 'localtime', 'mktime', 'monotonic', 'monotonic_ns', 'perf_counter', 'perf_counter_ns', 'process_time', 'process_time_ns', 'sleep', 'strftime', 'strptime', 'struct_time', 'thread_time', 'thread_time_ns', 'time', 'time_ns', 'timezone', 'tzname'

            if int(time.time()*5)%2 == 0:
                light.color = color.red

            else:
                light.color = color.blue
        else:
            light.color = color.black33


def dis_able_menu():
    global inMenu
    inMenu = not inMenu
    level.enabled = not level.enabled
    player.enabled = not player.enabled
    mouse.visible = not mouse.visible
    mouse.locked = not mouse.locked
    player_car.ent.visible = not player_car.ent.visible
    pos_text.enabled = not pos_text.enabled
    speed_text.enabled = not speed_text.enabled
    distance_text.enabled = not distance_text.enabled


def status():
    global game_paused
    game_paused = False


def input(key):
    global ems_lighting
    global game_paused
    if key == 'escape':
        game_paused = not game_paused
    if held_keys['control'] and key == 'r':
        player_car.ent.position = Vec3(0, 0, 0)
        player_car.speed = None

    if key == "e":
        ems_lighting = not ems_lighting
        if ems_lighting:
            siren_audio.play()
        else:
            siren_audio.stop()



Sky(texture='night_sky_red_blur')
#EditorCamera()
app.run()
