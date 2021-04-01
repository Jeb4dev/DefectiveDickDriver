from ursina import *
from read_key_bindings import getValue, updateValue, saveValues

main_menu = Entity(scale=Vec2(12, 12), billboard=True)
options_menu = Entity(scale=Vec2(12, 12), billboard=True)
mouse_keyboard_menu = Entity(scale=Vec2(12, 12), billboard=True)
scoreboard_menu = Entity(scale=Vec2(12, 12), billboard=True)
other_options_menu = Entity(scale=Vec2(12, 12), billboard=True)
graphic_options_menu = Entity(scale=Vec2(12, 12), billboard=True)


class LoadingWheel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.point = Entity(
            parent=self,
            model=Circle(24, mode='point', thickness=3),
            color=color.light_gray,
            y=.75,
            scale=2
            )
        self.point2 = Entity(
            parent=self,
            model=Circle(12, mode='point', thickness=3),
            color=color.light_gray,
            y=.75,
            scale=1
            )
        self.scale = .025
        self.text_entity = Text(
            world_parent = self,
            text = '  loading...',
            origin = (0,1.5),
            color = color.light_gray,
            )
        self.y = -.25

        self.bg = Entity(parent=self, model='quad', scale_x=camera.aspect_ratio, color=color.black, z=1)
        self.bg.scale *= 400

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def update(self):
        self.point.rotation_y += 5
        self.point2.rotation_y += 3


def showMainMenu():

    options_menu.enabled, mouse_keyboard_menu.enabled, scoreboard_menu.enabled = False, False, False
    main_menu.enabled = True
    Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2))

    Text(parent=main_menu, origin=(0, -10), text="Our Perfect Game")

    # fix the play button
    b_play = Button(parent=main_menu, text='Press ESC!', color=color.black10, scale=(0.5, 0.08), position=(0, 0.1))
    b_scoreboard = Button(parent=main_menu, text='Scoreboard', color=color.black10, scale=(0.5, 0.08), position=(0, 0))
    b_options = Button(parent=main_menu, text='Options', color=color.black10, scale=(0.5, 0.08), position=(0, -0.1))
    b_quit = Button(parent=main_menu, text='Quit!', color=color.black10, scale=(0.5, 0.08), position=(0, -0.2))

    b_play.on_click = LoadingWheel(enabled=False)  # assign a function to the button.
    b_play.tooltip = Tooltip('press [ESC] pls !!!')

    b_scoreboard.on_click = showScoreboardMenu
    b_scoreboard.tooltip = Tooltip('Show Scoreboard')

    b_options.on_click = showOptionsMenu
    b_options.tooltip = Tooltip('options')

    b_quit.on_click = application.quit  # assign a function to the button.
    b_quit.tooltip = Tooltip('exit')


    #  def on_value_changed():
    #         if gender_selection.value==['Buttonlist']:
    #             invoke(showButtonListMenu)
    #         elif gender_selection.value==['Radial menu']:
    #             invoke(showRadialMenu)
    #         elif gender_selection.value==['Dropdown menu']:
    #             invoke(showDropDownMenu)

    # gender_selection.on_value_changed = on_value_changed

    #     def on_value_changed():
    #         print('turn:', on_off_switch.value)
    #
    #     on_off_switch.on_value_changed = on_value_changed

    window.color = color._32


def showGraphicOptionsMenu():
    options_menu.enabled = False
    graphic_options_menu.enabled = True
    Entity(parent=graphic_options_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2))

    Text(parent=graphic_options_menu, origin=(0, -10), text="Graphic Settings")

    b_oo_back = Button(parent=graphic_options_menu, text='Back', color=color.black10, scale=(0.5, 0.08), position=(0, -0.2))

    b_oo_back.on_click = showOptionsMenu  # assign a function to the button.
    b_oo_back.tooltip = Tooltip('Back to Options menu')


def showOtherOptionsMenu():
    other_options_menu = Entity(scale=Vec2(12, 12), billboard=True)
    options_menu.enabled = False
    other_options_menu.enabled = True
    Entity(parent=other_options_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2))

    Text(parent=other_options_menu, origin=(0, -10), text="Other Settings")
    if getValue("settings", "hints") == 'off':
        hints = 'off'
    else:
        hints = 'on'


    Text(parent=other_options_menu, position=(.05, .2), scale=1, text="Tips")
    on_off_switch = ButtonGroup(('off', 'on'), parent=other_options_menu, min_selection=1, position=(.05, .2), default=f"{hints}", selected_color=color.red)

    def on_value_changed():
        global hints
        updateValue("settings", "hints", "".join(on_off_switch.value))
        saveValues()

    on_off_switch.on_value_changed = on_value_changed

    def goback():
        saveValues()
        showOptionsMenu()
        destroy(other_options_menu)



    #     on_off_switch.on_value_changed = on_value_changed

    b_oo_back = Button(parent=other_options_menu, text='Back', color=color.black10, scale=(0.5, 0.08), position=(0, -0.2))

    b_oo_back.on_click = goback  # assign a function to the button.
    b_oo_back.tooltip = Tooltip('Back to Options menu')




def showOptionsMenu():
    global main_menu, options_menu, mouse_keyboard_menu, other_options_menu, graphic_options_menu
    main_menu.enabled, mouse_keyboard_menu.enabled, other_options_menu.enabled, graphic_options_menu.enabled = False, False, False, False
    options_menu.enabled = True
    Entity(parent=options_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2))
    Text(parent=options_menu, origin=(0, -7), scale=1.8, text="Options")


    b_o_mouse_keys = Button(parent=options_menu, text='Mouse & Keys', color=color.black10, scale=(0.5, 0.08), position=(0, 0.1))
    b_o_graphics = Button(parent=options_menu, text='Graphics', color=color.black10, scale=(0.5, 0.08), position=(0, 0))
    b_o_other = Button(parent=options_menu, text='Other', color=color.black10, scale=(0.5, 0.08), position=(0, -0.1))
    b_o_back = Button(parent=options_menu, text='Back', color=color.black10, scale=(0.5, 0.08), position=(0, -0.2))

    b_o_mouse_keys.on_click = showMouseKeyboardMenu  # assign a function to the button.
    b_o_mouse_keys.tooltip = Tooltip('Mouse sensitivity & keybindings')

    b_o_graphics.on_click = showGraphicOptionsMenu  # assign a function to the button.
    b_o_graphics.tooltip = Tooltip('Graphic settings')

    b_o_other.on_click = showOtherOptionsMenu  # assign a function to the button.
    b_o_other.tooltip = Tooltip('Other settings')

    b_o_back.on_click = showMainMenu
    b_o_back.tooltip = Tooltip('Back to Main menu')

    window.color = color._32

# Keys
allkeys = ["forward", "left", "backwards", "right", "quit", "car", "escape"]


def showScoreboardMenu():
    main_menu.enabled, options_menu.enabled, mouse_keyboard_menu.enabled = False, False, False
    scoreboard_menu.enabled = True
    Entity(parent=scoreboard_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2))

    Text(parent=scoreboard_menu, origin=(0, -7), scale=1.8, text="Scoreboard")
    scoreboard = getValue("scoreboard", "*")
    s = 0
    for i in range(len(scoreboard)):
        for j in scoreboard[i]:
            s += 1  # just here chilling, don't touch
            Text(parent=scoreboard_menu, position=(-.1, .17-s*.05), text=j)  # font="courier"
            Text(parent=scoreboard_menu, position=(0, .17-s*.05), text=f"{scoreboard[i][j]}".center(8))
    Text(parent=scoreboard_menu, position=(-.1, .2), text=f"Name")
    Text(parent=scoreboard_menu, position=(0, .2), text=f"Score")


    b_sb_back = Button(parent=scoreboard_menu, text='Back', color=color.black10, scale=(0.3, 0.08), position=(0, -0.3))

    b_sb_back.on_click = showMainMenu
    b_sb_back.tooltip = Tooltip('Back to Main menu')

    window.color = color._32


def showMouseKeyboardMenu():
    global main_menu, options_menu, mouse_keyboard_menu
    main_menu.enabled, options_menu.enabled, scoreboard_menu.enabled = False, False, False
    mouse_keyboard_menu.enabled = True
    Entity(parent=mouse_keyboard_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90), position=(2, 2, 2))

    Text(parent=mouse_keyboard_menu, origin=(0, -7), scale=1.8, text="Mouse & Keyboard Settings")

    # Mouse Sensitivity
    sensitivity = getValue("mouse_settings", "sensitivity")
    slider = ThinSlider(parent=mouse_keyboard_menu, text="Mouse Sensitivity", min=0, max=10, default=sensitivity, x=-.5,
                        y=.2, step=0.1, dynamic=True)
    slider.scale *= .5

    def on_slider_changed(slider=slider):
        global sensitivity
        sensitivity = slider.value
        updateValue("mouse_settings", "sensitivity", sensitivity)

    slider.on_value_changed = on_slider_changed
    slider.tooltip = Tooltip('Mouse sensitivity')

    b_km_save = Button(parent=mouse_keyboard_menu, text='Save', color=color.black10, scale=(0.3, 0.08), position=(0, -0.2))
    b_km_back = Button(parent=mouse_keyboard_menu, text='Back', color=color.black10, scale=(0.3, 0.08), position=(0, -0.3))

    b_km_save.on_click = saveValues
    b_km_save.tooltip = Tooltip('Save settings')

    b_km_back.on_click = showOptionsMenu
    b_km_back.tooltip = Tooltip('Back to Main menu')

    for key in range(len(allkeys)):
        Button(parent=mouse_keyboard_menu, color=color.black10, scale=(0.15, 0.04), position=(.4, .2-.05*key), on_click=(Func(get_input_and_send, key)))
        Text(parent=mouse_keyboard_menu, text=allkeys[key], scale=(1, 1), position=(.325, .2125-.05*key))
        Text(parent=mouse_keyboard_menu, text=getValue("keybindings", allkeys[key]), scale=(1, 1), position=(.5, .2125 - .05 * key))


    window.color = color._32


def get_input_and_send(num):
    for key, value in held_keys.items():
        print(key, value)
        if value == 1 and key != "left mouse":
            invoke(updateValue, "keybindings", allkeys[num], key)
            print("key has been updated: "+key)



quit_key = getValue("keybindings", "quit")
print("quit_key",quit_key)


def input(key):
    if key == quit_key:
        invoke(application.quit)

def changePos(pos):
    main_menu.position = pos


if __name__ == '__main__':
    app = Ursina()

    screen = None  # for global statement
    showMainMenu()

    window.exit_button.visible = False
    window.fps_counter.visible = False

    app.run()

