from ursina import *
import json


class Menu:
    entities = []

    def __init__(self, player, player_car):
        self.player = player
        self.player_car = player_car
        self.e = self.entities.append

        self.show_main_menu()

    @classmethod
    def clear_menu(cls):
        while cls.entities:
            destroy(cls.entities.pop(), delay=0)

    def show_main_menu(self):
        camera.rotation = Vec3(0, 0, 0)
        camera.position = Vec3(0, 0, -20)

        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12),
                           billboard=True,
                           position=self.player.position)
        self.e(main_menu)
        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                      position=(2, 2, 2)))

        self.e(Text(parent=main_menu, position=(-.2, .5), text="Defective:", scale=4.4))
        self.e(Text(parent=main_menu, position=(-.1, .4), text="Dick", scale=4.4*.67))
        self.e(Text(parent=main_menu, position=(-.03, .33), text="Driver", scale=4.4*.67))

        self.e(Button(parent=main_menu, text='Play', color=color.black10, scale=(0.5, 0.08),
                      position=(0, 0.1), on_click=self.player_car.pause, tooltip=Tooltip('to game')))
        self.e(Button(parent=main_menu, text='Scoreboard', color=color.black10, scale=(0.5, 0.08),
                      position=(0, 0), on_click=self.show_scoreboard_menu, tooltip=Tooltip('Show High Scores')))
        self.e(Button(parent=main_menu, text='Controls', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.1), on_click=self.show_keyboard_menu, tooltip=Tooltip('Show Controls')))
        self.e(Button(parent=main_menu, text='Quit!', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.2), on_click=application.quit, tooltip=Tooltip('exit')))
        self.e(Button(parent=main_menu, text='Story', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.4), on_click=self.show_story_menu, tooltip=Tooltip('Read story')))

    def show_scoreboard_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)

        def delete_scores():
            with open('scores.json', 'w') as f:
                f.write("")
            self.show_main_menu()

        try:
            with open('scores.json', 'r') as f:
                data = json.load(f)
        except:
            data = {}

        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                      position=(2, 2, 2)))

        self.e(Button(parent=main_menu, text=f'High Scores', scale=(0.5, 0.08),
                      position=(0, .35), highlight_color=color.rgba(0, 0, 0, 0),
                      color=color.rgba(0, 0, 0, 0), pressed_color=color.rgba(0, 0, 0, 0)))

        for idx, (date, score) in enumerate(data.items()):
            if idx == 5:
                break
            temp = time.strptime(date, "%X %x")
            self.e(Button(parent=main_menu, text=f'{time.strftime("%x", temp)}          {round(score)}',
                          color=color.black10, scale=(0.5, 0.08),
                          position=(0, 0.2 - idx * 0.1), on_click=self._pass,
                          tooltip=Tooltip(time.strftime("%X on %A %B %d %Y", temp))))

        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.35), on_click=self.show_main_menu, tooltip=Tooltip('Back to Main menu')))
        self.e(Button(parent=main_menu, text='Clear', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.50), on_click=delete_scores,
                      tooltip=Tooltip('Clear all High Scored, cannot be undone.')))

    def show_keyboard_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)

        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                      position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -8), text="Controls", scale=(1.5, 1.5)))

        # Keybindings
        all_keys = ["forward", "siren", "backwards", "brake", "left", "Menu", "Right", "Quit"]
        key_bindings = ["W", "E", "S", "SPACE", "A", "Esc", "D", "Shift+q"]

        for key in range(len(all_keys)):
            if key % 2 == 0:
                Button(parent=main_menu, color=color.black10, scale=(0.2, 0.08), position=(-.3, .175 - .05 * key))
                # on_click=(Func(get_input_and_send, key)))
                Text(parent=main_menu, text=key_bindings[key].upper(), scale=(1, 1),
                     position=(.325 - .7, .1875 - .05 * key))
                Text(parent=main_menu, text=all_keys[key].lower(), scale=(1.2, 1.2),
                     position=(-0.07 - 0.1, .1875 - .05 * key))
            else:
                Button(parent=main_menu, color=color.black10, scale=(0.2, 0.08), position=(+.2, .225 - .05 * key))
                # on_click=(Func(get_input_and_send, key)))
                Text(parent=main_menu, text=key_bindings[key].upper(), scale=(1, 1), position=((.13), .23 - .05 * key))
                Text(parent=main_menu, text=all_keys[key].lower(), scale=(1.2, 1.2),
                     position=(+0.33, .23 - .05 * key))

        # Buttons
        # self.e(Button(parent=main_menu, text='Save!', color=color.black10, scale=(0.5, 0.08),
        #                             position=(0, -0.2), on_click=save_values,
        #                             tooltip=Tooltip('Save Changes')))
        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.6, 0.08),
                      position=(0, -0.3), on_click=self.show_main_menu,
                      tooltip=Tooltip('Back to main menu')))

    def show_score_menu(self, new_hs, txt):
        camera.rotation = Vec3(0, 0, 0)
        camera.position = Vec3(0, 0, -20)

        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12),
                           billboard=True,
                           position=self.player.position)
        self.e(main_menu)
        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                      position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -8), scale=2, text=txt[:], color=color.black33))
        if new_hs:
            score_text = f'New High Score!\n           {round(self.player_car.score)}\nNew High Score!'
        else:
            score_text = f"Final Score: {round(self.player_car.score)}"

        self.e(Text(parent=main_menu, origin=(0, 0), scale=4, text=score_text))

        self.e(Button(parent=main_menu, text='Back', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.40), on_click=self.show_main_menu,
                      tooltip=Tooltip('Back to Main menu or just press [ESC] to replay')))

    def show_story_menu(self):
        camera.rotation = Vec3(0, 0, 0)
        camera.position = Vec3(0, 0, -20)

        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12),
                           billboard=True,
                           position=self.player.position)
        self.e(main_menu)
        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                      position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -6.0), scale=2,
                    text="Richard Driver always knew he was destined for greatness."))
        self.e(Text(parent=main_menu, origin=(0, -4.8), scale=2,
                    text="Having quickly climbed the ranks to Detective in the Shitty City Police Department,"))
        self.e(Text(parent=main_menu, origin=(0, -3.6), scale=2,
                    text="Richard thought he could change the world."))
        self.e(Text(parent=main_menu, origin=(0, -2.4), scale=2,
                    text="Unfortunately for Richard, the city had other plans."))
        self.e(Text(parent=main_menu, origin=(0, -1.2), scale=2,
                    text="20 years of Detective work for the SCPD took its toll,"))
        self.e(Text(parent=main_menu, origin=(0, 0), scale=2,
                    text="and it wasn't long before Dick emerged, hardened by the streets."))
        self.e(Text(parent=main_menu, origin=(0, 1.2), scale=2,
                    text="Until one fateful morning when the Chief came by with a file,"))
        self.e(Text(parent=main_menu, origin=(0, 2.4), scale=2,
                    text='"Close this case and you earn your stripes," he said with a grin'))
        self.e(Text(parent=main_menu, origin=(0, 3.6), scale=2,
                    text="Help Dick fulfill his destiny."))

        self.e(Button(parent=main_menu, text='Drive!', color=color.black10, scale=(0.5, 0.08),
                      position=(0, -0.40), on_click=self.player_car.pause,
                      tooltip=Tooltip('Back to Main menu or just press [ESC] to replay')))

    def _pass(self):
        pass
