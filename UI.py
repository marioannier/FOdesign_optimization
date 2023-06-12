import customtkinter
from FiberProfile import *
from tkinter import filedialog
from tkinter import *

import numpy as np
import time


# This file was created to run simulations in terms of finding the best dimension and dopant values for certain output
# value (values_output = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]). These values are storge
# in a .csv file. The user can select the upper and lower value for each variable involved and how many incremental
# steps to take. TDefault values were defined.


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


class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, title, values, choice):
        super().__init__(master)
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

        optionmenu = customtkinter.CTkOptionMenu(self, values=["Step Index", "Triangular", "Graded"])
        optionmenu.grid(row=len(values) + 2, column=1, padx=0, pady=(10, 0), sticky="w")
        optionmenu.set(choice)
        self.optionmenus.append(optionmenu)

    def get_menu(self):
        out = self.optionmenus[0].get()
        return out

    def get_output(self):
        # ON PROGRESS
        A = 1


class MyFrame3(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        labels_input = ["a1(um)", "a2(um)", "a3(um)", "a4(um)", "n1(%)", "n2(%)", "n3(%)", "n4(%)", "alpha"]
        values_input = [3, 2, 2.5, 15, 0.05, 0, 0, 0, 1]
        values_output = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]

        self.title("Scan")
        self.geometry("1200x500")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = MyFrameleft(self, labels_input, values_input)
        self.frame_left.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        choice = "Step Index"
        self.frame_2 = MyFrame2(self, "Output", values_output, choice)
        self.frame_2.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="RUN", command=self.buttonRUN_callback)
        self.button.grid(row=3, column=1, padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self, text="Estimated simulation time", fg_color="transparent")
        self.label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        time = '--:--:--'
        self.label_t = customtkinter.CTkLabel(self, text=time, fg_color="transparent")
        self.label_t.grid(row=3, column=0, padx=180, pady=(10, 0), sticky="w")

        self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
        self.progressbar.configure(height=15, corner_radius=4, progress_color='green')

        self.frame_3 = MyFrame3(self, "Settings")
        self.frame_3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    def buttonRUN_callback(self):
        # get the project directory (project)
        global dev
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
        values_f = np.array(values).astype(float)
        steps = self.frame_left.get_steps()
        steps_f = np.array(steps).astype(int)
        fiber_p = self.frame_2.get_menu()

        a1_lower = values_f[0][0]
        a1_upper = values_f[0][1]
        # Define the ranges for each parameter
        a1_steps = steps_f[0]
        a1 = np.linspace(a1_lower, a1_upper, a1_steps)  # for a1_steps = 1 , a1 = a1_lower

        a2_lower = values_f[1][0]
        a2_upper = values_f[1][1]
        # Define the ranges for each parameter
        a2_steps = steps_f[1]
        a2 = np.linspace(a2_lower, a2_upper, a2_steps)

        a3_lower = values_f[2][0]
        a3_upper = values_f[2][1]
        # Define the ranges for each parameter
        a3_steps = steps_f[2]
        a3 = np.linspace(a3_lower, a3_upper, a3_steps)

        a4_lower = values_f[3][0]
        a4_upper = values_f[3][1]
        # Define the ranges for each parameter
        a4_steps = steps_f[3]
        a4 = np.linspace(a4_lower, a4_upper, a4_steps)

        n1 = None
        n1_dopant_lower = values_f[4][0]
        n1_dopant_upper = values_f[4][1]
        # Define the ranges for each parameter
        n1_dopant_steps = steps_f[4]
        n1_dopant = np.linspace(n1_dopant_lower, n1_dopant_upper, n1_dopant_steps)

        n2 = None
        n2_dopant_lower = values_f[5][0]
        n2_dopant_upper = values_f[5][1]
        # Define the ranges for each parameter
        n2_dopant_steps = steps_f[5]
        n2_dopant = np.linspace(n2_dopant_lower, n2_dopant_upper, n2_dopant_steps)

        n3 = None
        n3_dopant_lower = values_f[6][0]
        n3_dopant_upper = values_f[6][1]
        # Define the ranges for each parameter
        n3_dopant_steps = steps_f[6]
        n3_dopant = np.linspace(n3_dopant_lower, n3_dopant_upper, n3_dopant_steps)

        n4 = None
        n4_dopant_lower = values_f[7][0]
        n4_dopant_upper = values_f[7][1]
        # Define the ranges for each parameter
        n4_dopant_steps = steps_f[7]
        n4_dopant = np.linspace(n4_dopant_lower, n4_dopant_upper, n4_dopant_steps)

        alpha_lower = values_f[8][0]
        alpha_upper = values_f[8][1]
        # Define the ranges for each parameter
        alpha_steps = steps_f[8]
        alpha = np.linspace(alpha_lower, alpha_upper, alpha_steps)

        # creating variable to store the result
        steps = a1_steps * a2_steps * a3_steps * a4_steps * n1_dopant_steps * n2_dopant_steps * n3_dopant_steps * n4_dopant_steps * alpha_steps
        data_scan = np.zeros(
            (steps, 9 + 9))  # 9-> max output of fiber_profile.mode_data() and 9 -> number of fiber parameters
        i = 0

        param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
                      "neffg": True, "fillFac": True, "gammaE": True}
        header = (
            ['a1(um)', 'a2(um)', 'a3(um)', 'a4(um)', 'n1 dopant(%)', 'n2 dopant(%)', 'n3 dopant(%)', 'n4 dopant(%)',
             'alpha',
             "beta (Real)", "neff (Real)", "a_eff", "alpha", "dispersion", "isLeaky", "neffg", "fillFac", "gammaE"])

        if fiber_p == 'Step Index':
            dev = "app.subnodes[1].subnodes[1]"
            one_sim = 13
        if fiber_p == 'Triangular':
            dev = "app.subnodes[1].subnodes[2]"
            one_sim = 7
        if fiber_p == 'Graded':
            dev = "app.subnodes[1].subnodes[3]"
            one_sim = 7
        time_sim = str(one_sim * steps) + ' seg = ' + str(np.around((one_sim * steps) / 60, decimals=5)) + ' min = ' \
                   + str(np.around((one_sim * steps) / 3600, decimals=3)) + ' h'
        elapsed_time = np.zeros(steps)
        self.label_t.configure(text=time_sim)
        print('Simulation estimeted time: ' + time_sim)

        # Iterate over all combinations of parameters
        for a1_val in a1:
            for a2_val in a2:
                for a3_val in a3:
                    for a4_val in a4:
                        for n1_dopant_val in n1_dopant:
                            for n2_dopant_val in n2_dopant:
                                for n3_dopant_val in n3_dopant:
                                    for n4_dopant_val in n4_dopant:
                                        for alpha_val in alpha:
                                            # running the simulation
                                            start_time = time.time()

                                            fiber_profile.update_profile(dev, a1_val, a2_val, a3_val, a4_val,
                                                                         n1_dopant_val,
                                                                         n2_dopant_val, n3_dopant_val, n4_dopant_val,
                                                                         fiber_p, alpha_val)
                                            data_scan[i, 9:] = list(fiber_profile.mode_data(dev, param_Scan))
                                            data_scan[i, 0:9] = [a1_val, a2_val, a3_val, a4_val, n1_dopant_val,
                                                                 n2_dopant_val, n3_dopant_val, n4_dopant_val,
                                                                 alpha_val]
                                            end_time = time.time()
                                            elapsed_time[i] = end_time - start_time
                                            i = i + 1
                                            self.progressbar.set(i / steps)
                                            print('Simulation goes for: ' + str(
                                                100 * i / steps) + ' %' + ' It took: ' + str(elapsed_time[i - 1]))

        print("Average Simulation took {:.2f} seconds to run.".format(np.average(elapsed_time)))
        data_scan = data_scan.astype('str')
        # add the new row to the top of the array
        data_scan = np.vstack((header, data_scan))

        for element in data_scan:
            f.write(','.join(element) + '\n')

        f.close()
        del fimmap
        print('DONE')


app = App()
app.mainloop()
