import tkinter as tk


class MenuGUI:
    aggregation = None

    def __init__(self, main_window, theme, font_size, db_manager):
        self.db_manager = db_manager
        self.menu_window = tk.Toplevel()
        self.main_window = main_window
        self.theme = theme
        self.font_size = font_size
        self.create_menu()

    def create_menu(self):
        screen_width = self.menu_window.winfo_screenwidth()
        screen_height = self.menu_window.winfo_screenheight()
        menu_window_x = (screen_width - 500) // 2
        menu_window_y = (screen_height - 400) // 2
        self.menu_window.geometry(f"{500}x{400}+{menu_window_x}+{menu_window_y - 50}")
        self.menu_window.title("Settings")
        self.menu_window.resizable(False, False)
        self.menu_window.grab_set()


        def create_buttons():
            global button_db_clear, button_db_fill
            global radio_button1, radio_button2, radio_var

            button_db_clear = tk.Button(self.menu_window, text="Clear the database", command=self.clear_db, width=19,
                                        height=1)
            button_db_clear.place(x=170, y=70)

            button_db_fill = tk.Button(self.menu_window, text="Fill the database", command=self.fill_db, width=19,
                                       height=1)
            button_db_fill.place(x=170, y=110)

            self.radio_var = tk.StringVar()
            self.radio_var.set("light")

            # Create the radio buttons
            radio_button1 = tk.Radiobutton(self.menu_window, text="Light mode", variable=self.radio_var, value="light",
                                           command=self.switch_to_light)
            radio_button1.place(x=190, y=150)

            radio_button2 = tk.Radiobutton(self.menu_window, text="Dark mode", variable=self.radio_var, value="dark",
                                           command=self.switch_to_dark)
            radio_button2.place(x=190, y=180)

        def create_labels():
            global label_font_size
            label_font_size = tk.Label(self.menu_window, text="Aggregation font size")
            label_font_size.place(x=180, y=210)

        def create_slider():
            global slider
            self.slider_var = tk.DoubleVar()
            slider = tk.Scale(self.menu_window, variable=self.slider_var, from_=1, to=30, orient=tk.HORIZONTAL,
                              command=self.set_font)
            slider.place(x=190, y=240)
            slider.set(self.font_size)

        create_buttons()
        create_labels()
        create_slider()
        if self.theme == "dark":
            self.switch_to_dark()
        else:
            self.switch_to_light()
        self.menu_window.update()
        self.menu_window.mainloop()

    def switch_to_light(self):
        self.menu_window.configure(bg="#FFFFFF")
        button_db_clear.configure(bg="#FFFFFF", fg="#2a2b2a")  # Update button color and text color
        button_db_fill.configure(bg="#FFFFFF", fg="#2a2b2a")
        radio_button1.configure(bg="#FFFFFF", fg="#2a2b2a")
        radio_button2.configure(bg="#FFFFFF", fg="#171717")
        label_font_size.configure(bg="#FFFFFF", fg="#171717")
        slider.configure(bg="#b5b3b3", fg="#171717")

        self.main_window.switch_to_light()

    def switch_to_dark(self):
        self.menu_window.configure(bg="#282C34")
        button_db_clear.configure(bg="#2f302f", fg="#a8ada8")  # Update button color and text color
        button_db_fill.configure(bg="#2f302f", fg="#a8ada8")
        radio_button1.configure(bg="#282C34", fg="#a8ada8")
        radio_button2.configure(bg="#282C34", fg="#a8ada8")
        label_font_size.configure(bg="#282C34", fg="#a8ada8")
        slider.configure(bg="#2f302f", fg="#a8ada8")

        self.main_window.switch_to_dark()

    def set_font(self, value):
        self.main_window.change_font(value)

    def clear_db(self):
        self.db_manager.delete_table()

    def fill_db(self):
        self.db_manager.fill_db()


def main():
    menu = MenuGUI()


if __name__ == '__main__':
    main()
