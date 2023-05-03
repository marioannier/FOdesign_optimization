import customtkinter
from FiberProfile import *
from tkinter import filedialog
from tkinter import *

import numpy as np


class MyFrameleft(customtkinter.CTkFrame):
    def __init__(self, master, labels, values):
        super().__init__(master)
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
            checkbox = customtkinter.CTkCheckBox(self, text="", command=self.action_check)
            checkbox.grid(row=i + 1, column=3, padx=10, pady=(10, 0))
            self.checkboxes.append(checkbox)

            # number of steps
            entry = customtkinter.CTkEntry(self, placeholder_text="1")
            entry.grid(row=i + 1, column=4, padx=(0, 30), pady=(10, 0), sticky="e")
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
        a4_lower = 5
        a4_upper = 5
        n1_dopant_lower = 0.04
        n1_dopant_upper = 0.05
        n2_dopant_lower = 0
        n2_dopant_upper = 0
        n3_dopant_lower = 0.001
        n3_dopant_upper = 0.001
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

    def action_check(self):
        i = 0
        for entry in self.entriesPamUP:
            a = self.checkboxes[i].get()
            if a == 1:
                entry.configure(state="normal", fg_color=self.matte_green)
            else:
                entry.configure(state="disable", fg_color=self.matte_red)
            i = i + 1

    # def get_value(self, TkObject):  # UVYUBHKJNKLYVYVUBUIOUHNIOUHUIOBOIUIOUHIUYBUOBUIGYUIY
    #     value = []
    #     i = 0
    #     for value in TkObject:
    #         value[i] = TkObject.get()
    #         i = i + 1
    #     return value


class MyFrameright(customtkinter.CTkFrame):
    def __init__(self, master, title, values, choice):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []
        self.labels = []
        self.optionmenus = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=2, padx=0, pady=(10, 0), sticky="w")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text="")
            checkbox.grid(row=i + 1, column=2, padx=10, pady=(10, 0))
            self.checkboxes.append(checkbox)

            # labels
            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i + 1, column=0, padx=10, pady=(10, 0))
            self.labels.append(label)

        label = customtkinter.CTkLabel(self, text="Profile:")
        label.grid(row=len(values) + 2, column=0, padx=10, pady=(10, 0))

        optionmenu = customtkinter.CTkOptionMenu(self, values=["Step Index", "Triangular", "Graded"])
        optionmenu.grid(row=len(values) + 3, column=0, padx=10, pady=(10, 0), sticky="w")
        optionmenu.set(choice)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        labels_input = ["a1(um)", "a2(um)", "a3(um)", "a4(um)", "n1(%)", "n2(%)", "n3(%)", "n4(%)", "alpha"]
        values_input = [3, 5, 2.5, 5, 0.05, 0, 0.01, 0, 1]
        values_output = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]

        self.title("Scan")
        self.geometry("900x500")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = MyFrameleft(self, labels_input, values_input)
        self.frame_left.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        choice = "Step Index"
        self.frame_right = MyFrameright(self, "Output", values_output, choice)
        self.frame_right.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="RUN", command=self.buttonRUN_callback)
        self.button.grid(row=3, column=1, padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self, text="Estimated simulation time", fg_color="transparent")
        self.label.grid(row=3, column=0, padx=100, pady=(10, 0), sticky="w")

        time = '--:--:-- (not available yet)'
        self.label = customtkinter.CTkLabel(self, text=time, fg_color="transparent")
        self.label.grid(row=3, column=0, padx=100, pady=(10, 0), sticky="e")

    def buttonRUN_callback(self):
        # get the project directory (project)
        root = Tk()
        root.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("all files", "*.*"), ("Text files", "*.txt")))
        root.destroy()  # Close the window

        # Establishes connection and open the project and open the file to save the data
        f = open('result.csv', 'w')
        fimmap = pdApp()
        fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
        fimmap.Exec("app.openproject(" + root.filename + ")")
        # create the object
        fiber_profile = FiberProfile(fimmap)

        values = self.frame_left.get_entry()
        print(values)
        values_f = np.array(values).astype(float)
        print(values_f)

        a1_lower = values_f[0][0]
        a1_upper = values_f[0][1]
        # Define the ranges for each parameter
        a1_steps = 5
        a1 = np.linspace(a1_lower, a1_upper, a1_steps)  # for a1_steps = 1 , a1 = a1_lower

        a2_lower = values_f[1][0]
        a2_upper = values_f[1][1]
        # Define the ranges for each parameter
        a2_steps = 1
        a2 = np.linspace(a2_lower, a2_upper, a2_steps)

        a3_lower = values_f[2][0]
        a3_upper = values_f[2][1]
        # Define the ranges for each parameter
        a3_steps = 1
        a3 = np.linspace(a3_lower, a3_upper, a3_steps)

        a4 = values_f[5][0]

        n1 = None
        n1_dopant_lower = values_f[4][0]
        n1_dopant_upper = values_f[4][1]
        # Define the ranges for each parameter
        n1_dopant_steps = 5
        n1_dopant = np.linspace(n1_dopant_lower, n1_dopant_upper, n1_dopant_steps)

        n2 = None
        n2_dopant_lower = values_f[5][0]
        n2_dopant_upper = values_f[5][1]
        # Define the ranges for each parameter
        n2_dopant_steps = 1
        n2_dopant = np.linspace(n2_dopant_lower, n2_dopant_upper, n2_dopant_steps)

        n3 = None
        n3_dopant_lower = values_f[6][0]
        n3_dopant_upper = values_f[6][1]
        # Define the ranges for each parameter
        n3_dopant_steps = 1
        n3_dopant = np.linspace(n3_dopant_lower, n3_dopant_upper, n3_dopant_steps)

        n4 = None
        n4_dopant_lower = values_f[7][0]
        n4_dopant_upper = values_f[7][1]
        # Define the ranges for each parameter
        n4_dopant_steps = 1
        n4_dopant = np.linspace(n4_dopant_lower, n4_dopant_upper, n4_dopant_steps)

        alpha_lower = values_f[8][0]
        alpha_upper = values_f[8][1]
        # Define the ranges for each parameter
        alpha_steps = 1
        alpha = np.linspace(alpha_lower, alpha_upper, alpha_steps)

        # creating variable to store the result
        steps = a1_steps * a2_steps * a3_steps * n1_dopant_steps * n2_dopant_steps * n3_dopant_steps * n4_dopant_steps * alpha_steps
        data_scan = np.zeros(
            (steps, 7 + 9))  # 7-> max output of fiber_profile.mode_data() and 9 -> number of fiber parameters
        i = 0

        param_Scan = {"beta": False, "neff": False, "a_eff": False, "alpha": False, "dispersion": True, "isLeaky": True,
                      "neffg": False}
        header = (
            ['a1(um)', 'a2(um)', 'a3(um)', 'a4(um)', 'n1 dopant(%)', 'n2 dopant(%)', 'n3 dopant(%)', 'n4 dopant(%)',
             'alpha',
             "beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"])

        dev = "app.subnodes[1].subnodes[2]"

        # Iterate over all combinations of parameters
        for a1_val in a1:
            for a2_val in a2:
                for a3_val in a3:
                    for n1_dopant_val in n1_dopant:
                        for n2_dopant_val in n2_dopant:
                            for n3_dopant_val in n3_dopant:
                                for n4_dopant_val in n4_dopant:
                                    for alpha_val in alpha:
                                        print(
                                            f"Scanning for a1 = {a1_val}, a2 = {a2_val}, a3 = {a3_val}, a4 = {a4}, n1_dopant ="
                                            f" {n1_dopant_val}, n2_dopant = {n2_dopant_val}, n3_dopant = {n3_dopant_val}, "
                                            f"n4_dopant = {n4_dopant_val}, alpha = {alpha_val}")
                                        print("and extracting: " + ", ".join(
                                            [key for key, val in param_Scan.items() if val]))
                                        # running the simulation
                                        fiber_profile.update_profile(dev, a1_val, a2_val, a3_val, a4, n1_dopant_val,
                                                                     n2_dopant_val, n3_dopant_val, n4_dopant_val,
                                                                     "Step Index", alpha_val)
                                        data_scan[i, 9:] = list(fiber_profile.mode_data(dev, param_Scan))
                                        data_scan[i, 0:9] = [a1_val, a2_val, a3_val, a4, n1_dopant_val,
                                                             n2_dopant_val, n3_dopant_val, n4_dopant_val,
                                                             alpha_val]
                                        i = i + 1
        data_scan = data_scan.astype('str')
        # add the new row to the top of the array
        data_scan = np.vstack((header, data_scan))

        for element in data_scan:
            f.write(','.join(element) + '\n')

        f.close()
        del fimmap


app = App()
app.mainloop()
