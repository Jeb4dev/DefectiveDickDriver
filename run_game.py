from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs import health_bar

from classes import TheCar, CheckPoint, Lighting, Obstacle, Arrow
from utils import make_walls, make_floor, reset_game
from constants import COLOR_RUST, COLOR_RUST_2X
from menu import Menu
from story import new_story


from sys import argv

import sys

# The major, minor version numbers your require
MIN_VER = (3, 7)

if sys.version_info[:2] < MIN_VER:
    sys.exit(
        "This game requires Python {}.{}.".format(*MIN_VER)
    )


app = Ursina()
window.show_ursina_splash = True
window.icon = "assets/icon/icon.ico"
window.fullscreen_size = (1920, 1080, 32)
window.windowed_size = (1920, 1080, 32)
window.fullscreen = True
window.title = "Defective: Dick Driver"
#window.icon = 'assets/icon/icon'

if len(argv) > 1:
    try:
        scale = int(argv[1])
        resolution = (scale / 9 * 16, scale, 32)
        window.fullscreen_size = resolution
        window.windowed_size = resolution
        if len(argv) > 2:
            window.fullscreen = int(argv[2])

    except exception as e:
        print(
            f'correct usage is ``logic.py height fullscreen`` height should be in pixels, 1 for fullscreen, 0 for windowed')


window.vsync = True

scene.fog_color = COLOR_RUST
scene.fog_density = (10, 60)

player = FirstPersonController(gravity=0)
camera.position = Vec3(0, 1, -20)
camera.rotation = Vec3(15, 0, 0)
player.cursor.enabled = False

walls = make_walls(450)
floor = make_floor(9, 60)


lower_floor = Entity(model='cube', color=COLOR_RUST,  position=(0, -2, 0),
                     scale=(10000, 1, 10000),
                     rotation=(0, 0, 0)
                     )

siren_light = Lighting(player, player.position + Vec3(1, 7, 0), color.black, rotation=player.down)
CheckPoint.init_light(Entity('cube', color=color.rgba(255,5,5,128), scale=(25,25,25)))

city = Entity(model='assets/models/city800', color=COLOR_RUST, position =(0, .1, 0), collider='mesh', reload=True)

car = Entity(model='assets/models/80scop', 
        texture='assets/models/cars', 
        position = (0, 0, 4), 
        scale=1,
        collider='box',
        name='player_car'
        )
CheckPoint.init_car(car)
Obstacle.init_car(car)

CheckPoint.spawn_new()

arrow = Arrow()
player_car = TheCar(car)
menu = Menu(player, player_car)
cars = [player_car]

camera.parent = player_car.ent
speed_text = Text(text=f"", position=(0, -.4), color=color.white66)
pos_text = Text(text=f"", position=(.3, .5), color=color.black)
score_text = Text(text=f"", position=(-.8, -.35), color=COLOR_RUST_2X)
story_text = Text(text=f"", position=(0, 0), color=COLOR_RUST_2X)
health_bar_1 = health_bar.HealthBar(bar_color=COLOR_RUST_2X, roundness=.1, value=100, position=(-.8, -.40), animation_duration=0)
siren_bar_1 = health_bar.HealthBar(bar_color=color.rgb(40, 40, 70), roundness=.1, value=100, position=(-.8, -.4375), animation_duration=0)

ignore_list = [player, car]

inMenu = False
mouse.visible = False

# Audio
music = Audio('assets/music/backaround_music', pitch=1, loop=True, autoplay=True, volume=.1)
siren_audio = Audio('assets/music/siren', pitch=1, loop=True, autoplay=False, volume=.1)

# Lights
driving_light1 = PointLight(shadows=True, color=color.rgb(196, 196, 196))
driving_light2 = PointLight(shadows=True, color=color.rgb(128, 128, 128))
driving_light3 = PointLight(shadows=True, color=color.rgb(64, 64, 64))
menu_light = AmbientLight(position=camera.position, shadows=True)

# ERROR: not creating when u play againg

def update():
    # Main Loop - Game Paused
    if player_car.paused:
        menu_light.color = color.rgb(100, 50, 50)
        driving_light1.color = color.black
        driving_light2.color = color.black
        driving_light3.color = color.black
        # Entity(billboard=True, scale=Vec3(10, 10, 10), color=color.black, model="plane", rotation=(-90, 0, 0))
        if not inMenu:
            invoke(menu.show_main_menu)
            dis_able_menu()

    # Main Loop - Game Running
    else:
        camera.rotation = Vec3(25, 0, 0)
        camera.position = Vec3(0, 10, -10)
        menu_light.color = color.black
        driving_light1.color = color.rgb(196, 196, 196)
        driving_light2.color = color.rgb(128, 128, 128)
        driving_light3.color = color.rgb(64, 64, 64)
        driving_light1.position = player_car.ent.position
        driving_light1.rotation_x = -90
        driving_light2.rotation_x = -90
        driving_light3.rotation_x = -90
        driving_light2.position = player_car.ent.position + player_car.ent.forward * 15 + Vec3(0, 5, 0)
        driving_light3.position = player_car.ent.position + player_car.ent.forward * 40 + Vec3(0, 5, 0)
        if inMenu:
            dis_able_menu()
            Menu.clear_menu()

        if player_car.new_game:
            while player_car.audio_list:
                print(player_car.audio_list)
                player_car.audio_list.pop().stop(destroy=True)
            player_car.ent.position = Vec3(0, 0, 0)
            player_car.new_game = False
            player_car.story = new_story()
            player_car.story_time = time.time() + 10
            player_car.score = 0

        # HUD
        speed_text.text = f"Speed {round(abs(player_car.speed) * 80, 1)} km/h"
        pos_text.text = f"Pos: {round(player.position[0], 2), round(player.position[1], 2), round(player.position[2], 2)}"
        score_text.text = f"SCORE {round(player_car.score)}"
        if player_car.story:
            if time.time() < player_car.story_time:
                story_text.text = f"Alert: {player_car.story[0]}"
            else:
                story_text.text = ''
        health_bar_1.value = round(player_car.hp)
        siren_bar_1.value = round(player_car.light_time)

        # Arrow
        arrow.position = player.position + Vec3(0, 5, 0)
        arrow.rotation = arrow.look_at(CheckPoint.checkpoints[0], axis="forward")


        if held_keys['w']:
            for car in cars:
                car.w()
        elif held_keys['s']:
            for car in cars:
                car.s()
        if held_keys['space']:
            for car in cars:
                car.brake(False)
        if (held_keys['a'] and held_keys['d']):
            #print('straight ahead!')
            player_car.steering = None
        elif not (held_keys['a'] or held_keys['d']):
            player_car.steering = 0
            #print('magic!')
        elif held_keys['d']:
            for car in cars:
                car.d()
        elif held_keys['a']:
            for car in cars:
                car.a()
        if player_car.lights:
            player_car.light_time -= 1
            if player_car.light_time < 0:
                player_car.lights = False
                siren_audio.stop()
        else:
            if player_car.light_time < 100:
                player_car.light_time += .1
        crash_speed = player_car.move([*ignore_list, *CheckPoint.checkpoints])
        if crash_speed:
            if player_car.hp < 1:
                print("end crash")
                if not player_car.audio_list:
                    if crash_speed < (10 / 80):
                        player_car.audio_list.append(Audio('assets/sfx/slow_crash_end'))
                    else:
                        player_car.audio_list.append(Audio('assets/sfx/fast_crash_end'))
                    player_car.audio_list[-1].play()
            else:
                if crash_speed > (10 / 80):
                    print("big crash", crash_speed)
                    Audio('assets/sfx/short_crash')

        player_car.rotate()
        if not (held_keys['w'] or held_keys['s]']):
            player_car.speed = 0

        for checkpoint in CheckPoint.checkpoints:

            if checkpoint.is_cleared([]):
                player_car.score += checkpoint.lastpoint

                Obstacle.shuffle()

        player.position = player_car.ent.position

        if player_car.lights:

            if int(time.time() * 5) % 2 == 0:
                siren_light.color = color.red

            else:
                siren_light.color = color.blue
        else:
            siren_light.color = color.black33

    if player_car.hp <= 0:
        player_car.paused = True
        reset_game(player_car, Obstacle, CheckPoint, menu)
        siren_audio.stop()
        dis_able_menu()


def dis_able_menu():
    global inMenu
    inMenu = not inMenu
    for i in range(len(floor)):
        floor[i].enabled = not floor[i].enabled
    for i in range(len(walls)):
        walls[i].enabled = not walls[i].enabled
    for i in range(len(Obstacle.obstacles)):
        Obstacle.obstacles[i].enabled = not Obstacle.obstacles[i].enabled
    arrow.enabled = not arrow.enabled
    lower_floor.enabled = not lower_floor.enabled
    # menu_light.visible = not menu_light.visible
    CheckPoint.checkpoints[0].enabled = not CheckPoint.checkpoints[0].enabled

    player.enabled = not player.enabled
    mouse.visible = not mouse.visible
    mouse.locked = not mouse.locked
    player_car.ent.visible = not player_car.ent.visible
    pos_text.enabled = not pos_text.enabled
    speed_text.enabled = not speed_text.enabled
    score_text.enabled = not score_text.enabled
    siren_bar_1.enabled = not siren_bar_1.enabled
    health_bar_1.enabled = not health_bar_1.enabled
    city.enabled = not city.enabled


def input(key):

    # toggle pause menu
    if key == 'escape':
        player_car.paused = not player_car.paused

    # respawn 0, 0
    if held_keys['control'] and key == 'r':
        player_car.ent.position = Vec3(0, 0, 0)
        player_car.speed = None

    # EMS lights toggle
    if key == "e":
        player_car.lights = not player_car.lights
        if player_car.lights:
            siren_audio.play()
        else:
            siren_audio.stop()

    # music toggle
    if key == "m":
        if music.playing:
            music.pause()
        else:
            music.resume()


Sky(texture='night_sky_red_blur')
# EditorCamera()
if __name__ == '__main__':
    app.run()

# basic_lighting_shader   -- no colored light
# colored_lights_shader   -- just white
# fading_shadows_shader   -- doesnt exist
# fresnel_shader          -- doesnt exist
# lit_with_shadows_shader -- apply color existing white
# matcap_shader           -- mirror finish
# normals_shader          -- rainbow
# texture_blend_shader    -- doesnt exist
# triplanar_shader        -- car .png colors
# unlit_shader            -- no colored light
