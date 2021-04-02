# old keybindings and stuff
def show_keyboard_menu(self):
    self.clear_menu()
    main_menu = Entity(scale=Vec2(12, 12), billboard=True, position=self.player.position)
    self.e(main_menu)

    # sensitivity = get_value("mouse_settings", "sensitivity")
    #
    self.e(Entity(parent=main_menu, model="plane", color=color.gray, scale=10, rotation=(90, 90, 90),
                  position=(2, 2, 2)))

    self.e(Text(parent=main_menu, origin=(0, -10), text="Mouse & Keyboard Settings"))

    # # Mouse Sensitivity
    # self.slider = ThinSlider(parent=main_menu, text="Mouse Sensitivity", min=0, max=10,
    #            default=sensitivity, x=-.4, y=.2, step=0.1, dynamic=True, scale=.5)
    # self.e(self.slider)
    #
    # def on_slider_changed(slider=self.slider):
    #     global sensitivity
    #     sensitivity = slider.value
    #     update_value("mouse_settings", "sensitivity", sensitivity)
    #
    # self.slider.on_value_changed = on_slider_changed
    # self.slider.tooltip = Tooltip('Mouse sensitivity')

    # Keybindings
    # all_keys = ["forward", "left", "backwards", "right", "quit", "car", "escape"]
    #
    # def get_input_and_send(num):
    #     for key, value in held_keys.items():
    #         print(key, value)
    #         if value == 1 and key != "left mouse":
    #             invoke(update_value, "keybindings", all_keys[num], key)
    #             print("key has been updated: " + key)
    #
    # for key in range(len(all_keys)):
    #     Button(parent=main_menu, color=color.black10, scale=(0.15, 0.04), position=(.4, .2 - .05 * key),
    #            on_click=(Func(get_input_and_send, key)))
    #     Text(parent=main_menu, text=all_keys[key], scale=(1, 1), position=(.325, .2125 - .05 * key))
    #     Text(parent=main_menu, text=get_value("keybindings", all_keys[key]), scale=(1, 1),
    #          position=(.5, .2125 - .05 * key))

    # Buttons
    self.e(Button(parent=main_menu, text='Save!', color=color.black10, scale=(0.5, 0.08),
                  position=(0, -0.1), on_click=save_values,
                  tooltip=Tooltip('Save Changes')))
    self.e(Button(parent=main_menu, text='Back!', color=color.black10, scale=(0.5, 0.08),
                  position=(0, -0.2), on_click=self.show_options_menu,
                  tooltip=Tooltip('Back to Options menu')))