from ursina import *
from read_key_bindings import *


class Menu:
    entities = []

    def __init__(self, player, player_car):
        self.hints = get_value("settings", "hints")
        self.player = player
        self.player_car = player_car
        self.e = self.entities.append

        self.show_main_menu()

    @classmethod
    def clear_menu(cls):
        while cls.entities:
            destroy(cls.entities.pop(), delay=0)

    def show_main_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), 
                           billboard=True, 
                           position=self.player.position)
        self.e(main_menu)
        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -10), text="Our Perfect Game"))

        self.e(Button(parent=main_menu, text='Play', color=color.black10, scale=(0.5, 0.08),
                        position=(0, 0.1), on_click=self.player_car.pause, tooltip=Tooltip('PLAY')))
        self.e(Button(parent=main_menu, text='Scoreboard', color=color.black10, scale=(0.5, 0.08),
                        position=(0, 0), on_click=self.show_scoreboard_menu, tooltip=Tooltip('Show Scoreboard')))
        self.e(Button(parent=main_menu, text='Options', color=color.black10, scale=(0.5, 0.08),
                        position=(0, -0.1), on_click=self.show_options_menu, tooltip=Tooltip('options')))
        self.e(Button(parent=main_menu, text='Quit!', color=color.black10, scale=(0.5, 0.08),
                        position=(0, -0.2), on_click=application.quit, tooltip=Tooltip('exit')))

    def show_scoreboard_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)

        scoreboard = get_value("scoreboard", "*")

        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2)))

        self.e(Text(parent=main_menu, position=(0, .25), text="Scoreboard"))

        s = 0
        for i in range(len(scoreboard)):
            for j in scoreboard[i]:
                s += 1  # just here chilling, don't touch
                self.e(Text(parent=main_menu, position=(0, .17 - s * .05), text=f"{scoreboard[i][j]}".center(8)))

        self.e(Text(parent=main_menu, position=(0, .17), text="Score"))
        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                        position=(0, -0.2), on_click=self.show_main_menu, tooltip=Tooltip('Back to Main menu')))

    def show_options_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)
        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -10), text="Options"))

        self.e(Button(parent=main_menu, text='Mouse & Keys', color=color.black10, scale=(0.5, 0.08),
                        position=(0, 0.1), on_click=self.show_keyboard_menu, tooltip=Tooltip('Mouse sensitivity & keybindings')))
        self.e(Button(parent=main_menu, text='Graphics', color=color.black10, scale=(0.5, 0.08),
                        position=(0, 0), on_click=self.show_graphic_options_menu, tooltip=Tooltip('Graphic settings')))
        self.e(Button(parent=main_menu, text='Other', color=color.black10, scale=(0.5, 0.08),
                        position=(0, -0.1), on_click=self.show_other_options_menu, tooltip=Tooltip('Other settings')))
        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                        position=(0, -0.2), on_click=self.show_main_menu, tooltip=Tooltip('Back to Main menu')))

    def show_keyboard_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)

        sensitivity = get_value("mouse_settings", "sensitivity")

        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                                    position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -10), text="Mouse & Keyboard Settings"))

        # Mouse Sensitivity
        self.slider = ThinSlider(parent=main_menu, text="Mouse Sensitivity", min=0, max=10,
                   default=sensitivity, x=-.4, y=.2, step=0.1, dynamic=True, scale=.5)
        self.e(self.slider)

        def on_slider_changed(slider=self.slider):
            global sensitivity
            sensitivity = slider.value
            update_value("mouse_settings", "sensitivity", sensitivity)

        self.slider.on_value_changed = on_slider_changed
        self.slider.tooltip = Tooltip('Mouse sensitivity')

        # Keybindings
        all_keys = ["forward", "left", "backwards", "right", "quit", "car", "escape"]

        def get_input_and_send(num):
            for key, value in held_keys.items():
                print(key, value)
                if value == 1 and key != "left mouse":
                    invoke(update_value, "keybindings", all_keys[num], key)
                    print("key has been updated: " + key)

        for key in range(len(all_keys)):
            Button(parent=main_menu, color=color.black10, scale=(0.15, 0.04), position=(.4, .2 - .05 * key),
                   on_click=(Func(get_input_and_send, key)))
            Text(parent=main_menu, text=all_keys[key], scale=(1, 1), position=(.325, .2125 - .05 * key))
            Text(parent=main_menu, text=get_value("keybindings", all_keys[key]), scale=(1, 1),
                 position=(.5, .2125 - .05 * key))

        # Buttons
        self.e(Button(parent=main_menu, text='Save!', color=color.black10, scale=(0.5, 0.08),
                                    position=(0, -0.1), on_click=save_values,
                                    tooltip=Tooltip('Save Changes')))
        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                                    position=(0, -0.2), on_click=self.show_options_menu,
                                    tooltip=Tooltip('Back to Options menu')))

    def show_other_options_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)

        def goback():
            save_values()
            self.show_options_menu()

        def on_value_changed():
            global hints
            update_value("settings", "hints", "".join(on_off_switch.value))
            save_values()

        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -10), text="Other Settings"))

        # Hints
        self.e(Text(parent=main_menu, position=(-.025, .19), scale=1, text="Tips"))
        on_off_switch = ButtonGroup(('off', 'on'), parent=main_menu, min_selection=1, position=(.05, .2),
                                    default=f"{self.hints}", selected_color=color.red)
        self.e(on_off_switch)
        on_off_switch.on_value_changed = on_value_changed

        # Buttons
        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                        position=(0, -0.2), on_click=goback, tooltip=Tooltip('Back to Options menu')))

    def show_graphic_options_menu(self):
        self.clear_menu()
        main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
        self.e(main_menu)

        self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                                    position=(2, 2, 2)))

        self.e(Text(parent=main_menu, origin=(0, -10), text="Graphic Settings"))

        # Buttons
        self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                                    position=(0, -0.2), on_click=self.show_options_menu, tooltip=Tooltip('Back to Options menu')))

    def _pass(self):
        pass



if __name__ == '__main__':
    app = Ursina()

    screen = None  # for global statement
    menu = Menu()
    menu.show_main_menu()

    window.exit_button.visible = True
    window.fps_counter.visible = True

    app.run()


