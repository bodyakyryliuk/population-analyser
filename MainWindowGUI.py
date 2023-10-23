import textwrap
import tkinter as tk
from tkinter import ttk, messagebox
from DataBaseManager import DataBaseManager
from Statistics import Aggregation
from MenuGUI import MenuGUI


class MainWindowGUI:

    def __init__(self):
        self.objects = []
        self.main_window = tk.Tk()
        self.db_manager = DataBaseManager("my_table", self)
        self.aggregation = Aggregation(self.db_manager)
        self.main_canvas = tk.Canvas(self.main_window, width=765, height=560, bg="#e6e6e6")
        self.main_canvas_text = ""
        self.status_line_canvas = tk.Canvas(self.main_window, width=764, height=110, bg="#cccccc")
        self.status_line_canvas.place(x=215, y=580)
        self.status_line_text = ""
        self.theme = "light"
        self.font_size = 11
        self.status_line_scrollbar = tk.Scrollbar(self.status_line_canvas, command=self.status_line_canvas.yview)
        self.main_canvas_scrollbar = tk.Scrollbar(self.main_canvas, command=self.main_canvas.yview)

        self.configure_main_window()

    def configure_main_window(self):
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        main_window_x = (screen_width - 1000) // 2
        main_window_y = (screen_height - 700) // 2
        self.main_window.geometry(f"{1000}x{700}+{main_window_x}+{main_window_y - 50}")
        selected_checkboxes = []
        self.main_window.title("Chart")
        self.main_window.resizable(False, False)

        def create_statistics_combo_box():
            combo = tk.ttk.Combobox(self.main_window, state="readonly")
            combo_items = ['General'] + self.db_manager.select_countries()
            combo['values'] = combo_items
            combo.place(x=30, y=45)
            combo.current(0)  # Set the default selected option
            global selected_country
            selected_country = "General"
            create_year_combo_box(True)

            def on_chart_select(event):
                global selected_country
                selected_country = combo.get()
                if selected_country == "General":
                    create_year_combo_box(True)
                else:
                    create_year_combo_box(False)

            combo.bind('<<ComboboxSelected>>', on_chart_select)

        def configure_scroll_bar():
            self.status_line_scrollbar.place(x=750, y=0, height=110)
            self.status_line_canvas.configure(yscrollcommand=self.status_line_scrollbar.set)

            self.main_canvas_scrollbar.place(x=750, y=0, height=560)
            self.main_canvas.configure(yscrollcommand=self.main_canvas_scrollbar.set)

        def create_chart_type_combo_box():
            combo = tk.ttk.Combobox(self.main_window, state="readonly")
            combo['values'] = ["Bar chart", "Line chart", "Pie chart", "Geo plot"]
            combo.place(x=30, y=105)
            combo.current(0)  # Set the default selected option
            global selected_plot_type
            selected_plot_type = "Bar chart"

            # Function to handle the chart selection
            def on_chart_select(event):
                global selected_plot_type
                selected_plot_type = combo.get()

            combo.bind('<<ComboboxSelected>>', on_chart_select)

        def create_year_combo_box(enabled):
            combo = tk.ttk.Combobox(self.main_window, state="readonly")
            combo['values'] = ["1980", "2000", "2010", "2022", "2023", "2030", "2050"]
            combo.place(x=30, y=165)
            combo.current(0)  # Set the default selected option
            if enabled:
                combo["state"] = "enabled"
            else:
                combo["state"] = "disabled"
            global selected_year
            selected_year = "1980"

            # Function to handle the chart selection
            def on_chart_select(event):
                global selected_year
                selected_year = combo.get()

            combo.bind('<<ComboboxSelected>>', on_chart_select)

        def create_labels():
            global label_combo, label_chart_type, label_year, label_filename
            label_combo = tk.Label(self.main_window, text="Choose chart statistics")
            label_combo.place(x=30, y=15)

            label_chart_type = tk.Label(self.main_window, text="Choose chart type")
            label_chart_type.place(x=30, y=75)

            label_year = tk.Label(self.main_window, text="Choose year")
            label_year.place(x=30, y=135)

            label_filename = tk.Label(self.main_window, text="Enter report name")
            label_filename.place(x=30, y=527)
            self.objects.append(label_combo)
            self.objects.append(label_filename)
            self.objects.append(label_chart_type)
            self.objects.append(label_year)

        def create_buttons():
            global button_aggregation, button_chart, button_generate_report, button_menu
            button_aggregation = tk.Button(self.main_window, text="Display aggregation",
                                           command=on_button_aggregation_clicked,
                                           width=19, height=1)
            button_aggregation.place(x=30, y=493)

            button_chart = tk.Button(self.main_window, text="Draw chart", command=on_button_chart_clicked, width=19,
                                     height=1)
            button_chart.place(x=30, y=195)

            button_generate_report = tk.Button(self.main_window, text="Generate report",
                                               command=on_button_generate_report_clicked, width=19, height=1)
            button_generate_report.place(x=30, y=583)

            button_menu = tk.Button(self.main_window, text="Settings", command=on_button_menu_clicked, width=19,
                                    height=1)
            button_menu.place(x=30, y=613)

            self.objects.append(button_aggregation)
            self.objects.append(button_chart)
            self.objects.append(button_generate_report)

        def create_text_fields():
            global filename_text_field
            filename_text_field = tk.Entry(self.main_window, width=23, bg='white')
            filename_text_field.place(x=30, y=557)
            self.objects.append(filename_text_field)

        def on_button_chart_clicked():
            if selected_country != "General":
                self.update_status_line(
                    f"{selected_plot_type} about {selected_country} population has been generated successfully!")
                self.aggregation.draw_chart(self.db_manager.get_plot_dict(selected_country), selected_country,
                                            selected_plot_type)
            else:
                self.update_status_line(
                    f"General {selected_plot_type} of population in {selected_year} has been generated successfully!")

                if selected_plot_type == "Geo plot":
                    self.aggregation.create_geoplot(self.db_manager.get_general_plot_dict(int(selected_year)))
                else:
                    self.aggregation.draw_general_plot(self.db_manager.get_general_plot_dict(int(selected_year)),
                                                       selected_plot_type, int(selected_year))


            global image
            image = self.aggregation.resize_image("plot.png", 766, 560)
            self.main_canvas.delete("all")
            self.main_canvas.create_image(0, 0, anchor=tk.NW, image=image)

        def on_button_aggregation_clicked():
            global selected_checkboxes
            x_coordinate, y_coordinate = 10, 10
            self.main_canvas.delete("all")
            try:
                self.main_canvas_text = self.aggregation.calculate_aggregation(selected_checkboxes)
                self.update_status_line(f"Aggregation about {selected_checkboxes} has been generated successfully!")
                self.main_canvas_text = self.main_canvas.create_text(x_coordinate + 10, y_coordinate, text=self.main_canvas_text, anchor=tk.NW, font=("Tahoma", self.font_size))
            except NameError:
                print("Selected checkboxes are not defined")

        def on_button_generate_report_clicked():
            global filename_text, selected_checkboxes
            if filename_text_field.get() == "":
                filename_text = "report.docx"
            else:
                filename_text = filename_text_field.get() + ".docx"

            try:
                self.aggregation.generate_report(filename_text,
                                                 self.aggregation.calculate_aggregation(selected_checkboxes))
            except NameError:
                print("Selected checkboxes are not defined")
            self.update_status_line(f"Report {filename_text} has been generated successfully!")

        def on_button_menu_clicked():
            print(self.theme)
            menu = MenuGUI(self, self.theme, self.font_size, self.db_manager)

        def create_checkboxes():
            checkboxes = {}
            y_coordinate = 225
            # Create the checkboxes
            checkbox_texts = ["Maximal population by year", "Minimal population by year", "Average population by year",
                              "Maximal area", "Minimal area", "Maximal density", "Minimal density",
                              "Maximal growthRate",
                              "Minimal growthRate"]

            def update_selected_checkboxes():
                global selected_checkboxes
                selected_checkboxes = [text for text, checkbox_var in checkboxes.items() if checkbox_var.get()]
                self.update_status_line(f"User selected {selected_checkboxes}")

            for text in checkbox_texts:
                checkbox_var = tk.BooleanVar()
                checkbox = tk.Checkbutton(self.main_window, text=text, variable=checkbox_var,
                                          command=update_selected_checkboxes)
                checkbox.place(x=30, y=y_coordinate)
                y_coordinate += 30
                checkboxes[text] = checkbox_var
                self.objects.append(checkbox)

        def configure_main_canvas():
            global splash_screen
            self.main_canvas.place(x=215, y=15)
            splash_screen = self.aggregation.resize_image("population_analyser.png", 766, 560)
            self.main_canvas.create_image(0, 0, anchor=tk.NW, image=splash_screen)


        def run(self):
            create_statistics_combo_box()
            create_chart_type_combo_box()
            create_text_fields()
            create_checkboxes()
            create_buttons()
            create_labels()
            configure_scroll_bar()
            configure_main_canvas()
            if self.theme == "dark":
                self.switch_to_dark()
            else:
                self.switch_to_light()
            self.main_window.update()
            self.main_window.mainloop()

        run(self)

    def update_status_line(self, string):
        self.status_line_canvas.delete("all")
        divided_string = textwrap.fill(string, width=(int(1100 / int(self.font_size))))
        self.status_line_text = self.status_line_canvas.create_text(10, 10, anchor="nw", text=divided_string,
                                                                    font=("Tahoma", self.font_size))

    def switch_to_light(self):
        self.main_window.configure(bg="SystemButtonFace")
        self.status_line_canvas.configure(bg="#cccccc")
        self.main_canvas.configure(bg="#e6e6e6")
        button_menu.configure(bg="SystemButtonFace", fg="#171717")

        for object in self.objects:
            object.configure(bg="SystemButtonFace", fg="#171717")
        self.theme = "light"

    def switch_to_dark(self):
        self.main_window.configure(bg="#2f302f")
        self.status_line_canvas.configure(bg="#2f302f")
        self.main_canvas.configure(bg="#2f302f")
        button_menu.configure(bg="#2f302f", fg="#a8ada8")

        for object in self.objects:
            object.configure(bg="#2f302f", fg="#a8ada8")
        self.theme = "dark"

    def change_font(self, size):
        self.font_size = size
        self.main_canvas.itemconfig(self.main_canvas_text, font=("Times New Roman", size))
        self.main_canvas.config(scrollregion=self.main_canvas.bbox("all"))  # Update the scroll region
        self.main_canvas.yview_moveto(0)

        divided_string = textwrap.fill(self.status_line_canvas.itemcget(self.status_line_text, "text"), width=(int(1200 /int(self.font_size))))
        self.status_line_canvas.itemconfig(self.status_line_text, font=("Times New Roman", size))
        self.status_line_canvas.delete("all")
        self.status_line_text = self.status_line_canvas.create_text(10, 10, anchor="nw", text=divided_string,
                                                                    font=("Tahoma", self.font_size))
        self.status_line_canvas.config(scrollregion=self.status_line_canvas.bbox("all"))  # Update the scroll region
        self.status_line_canvas.yview_moveto(0)

    def get_objects(self):
        return self.objects

    def create_confirmation_window(self, text):
        result = messagebox.askyesno("Confirmation window", text)
        if result:
            return True
        else:
            return False


def main():
    mainWindowGUI = MainWindowGUI()


if __name__ == '__main__':
    main()
