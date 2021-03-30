from ursina import *
from ursina.prefabs.button_group import ButtonGroup

main_menu = Entity(scale=Vec2(10,10))
options_menu = Entity(scale=Vec2(10,10))

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
    global main_menu, options_menu
    options_menu.enabled = False
    main_menu.enabled = True

    screen = "menu"
    #gender_selection = ButtonGroup(('Play', 'Settings', 'Quit'))
    #on_off_switch = ButtonGroup(('off', 'on'), min_selection=1, y=-.1, default='on', selected_color=color.red)

    #Text.default_resolution = 1080 * Text.size

    test = Text(parent=main_menu, origin=(0, -10), text="Our Perfect Game")
    print("MainMenu")


    b_play = Button(parent=main_menu, text='Play!', color=color.black10, scale=(0.3,0.08), position=(0, 0.1))
    b_options = Button(parent=main_menu, text='Options', color=color.black10, scale=(0.3,0.08), position=(0, 0))
    b_quit = Button(parent=main_menu, text='Quit!', color=color.black10, scale=(0.3,0.08), position=(0, -0.1))

    b_play.on_click = LoadingWheel(enabled=False)  # assign a function to the button.
    b_play.tooltip = Tooltip('play')

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


def showOptionsMenu():
    global main_menu, options_menu
    main_menu.enabled = False
    options_menu.enabled = True
    screen = "options"
    test = Text(parent=options_menu, origin=(0, -10), text="Options")
    print("OptionsMenu")


    b_o_mouse_keys = Button(parent=options_menu, text='Mouse & Keys', color=color.black10, scale=(0.3, 0.08), position=(0, 0.1))
    b_o_graphics = Button(parent=options_menu, text='Graphics', color=color.black10, scale=(0.3, 0.08), position=(0, -0.1))
    b_o_other = Button(parent=options_menu, text='Other', color=color.black10, scale=(0.3, 0.08), position=(0, 0))
    b_o_back = Button(parent=options_menu, text='Back', color=color.black10, scale=(0.3, 0.08), position=(0, -0.2))

    b_o_mouse_keys.on_click = application.quit  # assign a function to the button.
    b_o_mouse_keys.tooltip = Tooltip('Mouse sensitivity & keybindings')

    b_o_graphics.on_click = application.quit  # assign a function to the button.
    b_o_graphics.tooltip = Tooltip('Graphic settings')

    b_o_other.on_click = application.quit  # assign a function to the button.
    b_o_other.tooltip = Tooltip('Other settings')

    b_o_back.on_click = showMainMenu
    b_o_back.tooltip = Tooltip('Back to Main menu')

    window.color = color._32


if __name__ == '__main__':
    app = Ursina()

    screen = None  # for global statement
    showMainMenu()

    window.exit_button.visible = False
    window.fps_counter.visible = False

    app.run()

