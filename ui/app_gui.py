import customtkinter
from fiber_design import *
from tkinter import *

class AppGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scan")
        self.geometry("1280x832") # MacBook Air - 1 frame

    def design_mode(self):
            pass

    def simulation_mode(self):
            pass

    def setting_values(self, master, title):
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.switch_vars = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=0, padx=(10, 10), pady=(30, 10))

        switch_var1 = customtkinter.CTkSwitch(self, text="Light/Dark mode", command=self.mode, onvalue="on",
                                              offvalue="off")
        switch_var1.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
        self.switch_vars.append(switch_var1)

        switch_var2 = customtkinter.CTkSwitch(self, text="Graphic/Console mode", onvalue="on",
                                              offvalue="off")
        switch_var2.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
        self.switch_vars.append(switch_var2)

    def mode(self):
        m = self.switch_vars[0].get()
        if m == "on":
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def output_select_values(self, master, title, values, choice):
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []
        self.labels = []
        self.optionmenus = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=1, padx=40, pady=(10, 0), sticky="w")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text="", corner_radius=0, onvalue="True", offvalue="False")
            checkbox.grid(row=i + 1, column=1, padx=50, pady=(10, 0))
            checkbox.select()
            self.checkboxes.append(checkbox)
            checkbox.configure(state="disabled")

            # labels
            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i + 1, column=0, padx=10, pady=(10, 0))
            self.labels.append(label)

        label = customtkinter.CTkLabel(self, text="Profile:")
        label.grid(row=len(values) + 2, column=0, padx=10, pady=(10, 0))

        optionmenu = customtkinter.CTkOptionMenu(self, values=["Step Index T", "Double-Clad SI", "Triple-Clad SI",
                                                               "Five Layers", "Triangular T", "Graded T",
                                                               "Raised Cosine T"])
        optionmenu.grid(row=len(values) + 2, column=1, padx=0, pady=(10, 0), sticky="w")
        optionmenu.set(choice)
        self.optionmenus.append(optionmenu)

        def get_menu(self):
            out = self.optionmenus[0].get()
            return out
    def input_range_values(self, master, labels, values):
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.labels = labels
        self.checkboxes = []
        self.entriesPamDW = []
        self.entriesPamUP = []
        self.entriesSteps = []
        self.matte_red = ('#FF6666', '#993333')
        self.matte_green = ('#66CC66', '#336633')

        self.title = customtkinter.CTkLabel(self, text="Variable", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=3, padx=0, pady=(10, 0), sticky="w")

        self.title = customtkinter.CTkLabel(self, text="Steps", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=4, padx=0, pady=(10, 0), sticky="w")

        for i, label in enumerate(self.labels):
            # label
            label = customtkinter.CTkLabel(self, text=label)
            label.grid(row=i + 1, column=0, padx=10, pady=(10, 0))

            # entries, lower value
            entry = customtkinter.CTkEntry(self, placeholder_text=str(self.values[i]), fg_color=self.matte_green)
            entry.grid(row=i + 1, column=1, padx=10, pady=(10, 0))
            self.entriesPamDW.append(entry)

            # entries, upper value
            entry = customtkinter.CTkEntry(self, placeholder_text="Enter the value", fg_color=self.matte_red)
            entry.grid(row=i + 1, column=2, padx=10, pady=(10, 0))
            entry.configure(state="disabled")
            self.entriesPamUP.append(entry)

            # check boxes
            checkbox = customtkinter.CTkCheckBox(self, text="", command=self.action_check, corner_radius=0)
            checkbox.grid(row=i + 1, column=3, padx=10, pady=(10, 0))
            self.checkboxes.append(checkbox)

            # number of steps
            entry = customtkinter.CTkEntry(self, placeholder_text="1", fg_color=self.matte_red)
            entry.grid(row=i + 1, column=4, padx=(0, 30), pady=(10, 0), sticky="e")
            entry.configure(state="disabled")
            self.entriesSteps.append(entry)
            entry.configure(width=40)

    def get_entry(self):
        a = [[] for _ in range(9)]
        i = 0
        # default values
        a1_lower = 3
        a1_upper = 6
        a2_lower = 2
        a2_upper = 3.5
        a3_lower = 2.5
        a3_upper = 5
        a4_lower = 15
        a4_upper = 15
        n1_dopant_lower = 0.04
        n1_dopant_upper = 0.06
        n2_dopant_lower = 0
        n2_dopant_upper = 0
        n3_dopant_lower = 0
        n3_dopant_upper = 0
        n4_dopant_lower = 0
        n4_dopant_upper = 0
        alpha_lower = 1
        alpha_upper = 3

        # Assign the lower and upper bounds to the first and second elements of the array respectively
        a[0] = [a1_lower, a1_upper]
        a[1] = [a2_lower, a2_upper]
        a[2] = [a3_lower, a3_upper]
        a[3] = [a4_lower, a4_upper]
        a[4] = [n1_dopant_lower, n1_dopant_upper]
        a[5] = [n2_dopant_lower, n2_dopant_upper]
        a[6] = [n3_dopant_lower, n3_dopant_upper]
        a[7] = [n4_dopant_lower, n4_dopant_upper]
        a[8] = [alpha_lower, alpha_upper]

        for entryDW, entryUP in zip(self.entriesPamDW, self.entriesPamUP):
            if entryDW.get() != '':
                a[i][0] = entryDW.get()
            if entryUP.get() != '':
                a[i][1] = entryUP.get()
            i += 1
        return a

    def get_steps(self):
        a = [1 for _ in range(9)]
        i = 0
        # default values
        a1_steps = '1'
        a2_steps = '1'
        a3_steps = '1'
        a4_steps = '1'
        n1_dopant_steps = '1'
        n2_dopant_steps = '1'
        n3_dopant_steps = '1'
        n4_dopant_steps = '1'
        alpha_steps = '1'

        a[0] = a1_steps
        a[1] = a2_steps
        a[2] = a3_steps
        a[3] = a4_steps
        a[4] = n1_dopant_steps
        a[5] = n2_dopant_steps
        a[6] = n3_dopant_steps
        a[7] = n4_dopant_steps
        a[8] = alpha_steps

        for entrySteps in self.entriesSteps:
            if entrySteps.get() != '':
                a[i] = entrySteps.get()
            i += 1
        return a

    def action_check(self):
        i = 0
        for entry, steps in zip(self.entriesPamUP, self.entriesSteps):
            a = self.checkboxes[i].get()
            if a == 1:
                steps.configure(state="normal", fg_color=self.matte_green)
                entry.configure(state="normal", fg_color=self.matte_green)
            else:
                steps.configure(state="disable", fg_color=self.matte_red)
                entry.configure(state="disable", fg_color=self.matte_red)
            i = i + 1

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()