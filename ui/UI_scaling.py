import customtkinter
from fiber_design import *
from tkinter import filedialog
from tkinter import *

import numpy as np
import time

# This code was made for testing the scalability of a code design. After selecting the dimensions of the base core
# we perform simulations changing the parameters: a1, a2, a3.
# the scaling factor changes btw 1 and max_scaling_factor (= 2) in scaling_steps = 1000 steps


class MyFrameleft(customtkinter.CTkFrame):
    def __init__(self, master, labels, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.labels = labels
        self.entriesPamDW = []
        self.matte_red = ('#FF6666', '#993333')
        self.matte_green = ('#66CC66', '#336633')

        self.title = customtkinter.CTkLabel(self, text="Fill-in:  initial fiber core parameters", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=1, padx=0, pady=(10, 0), sticky="w")

        for i, label in enumerate(self.labels):
            # label
            label = customtkinter.CTkLabel(self, text=label)
            label.grid(row=i + 1, column=0, padx=10, pady=(10, 0))

            # entries, lower value
            entry = customtkinter.CTkEntry(self, placeholder_text=str(self.values[i]), fg_color=self.matte_green)
            entry.grid(row=i + 1, column=1, padx=(0,10), pady=(10, 0))
            self.entriesPamDW.append(entry)

    def get_entry(self):
        a = np.zeros(9)
        i = 0
        # default values
        a1 = 3.3
        a2 = 4.5
        a3 = 1.3
        a4 = 10
        n1_dopant = 0.075
        n2_dopant = 0
        n3_dopant = 0
        n4_dopant = 0
        alpha = 1

        # Assign the values
        a[0] = a1
        a[1] = a2
        a[2] = a3
        a[3] = a4
        a[4] = n1_dopant
        a[5] = n2_dopant
        a[6] = n3_dopant
        a[7] = n4_dopant
        a[8] = alpha

        for entryDW in self.entriesPamDW:
            if entryDW.get() != '':
                a[i] = entryDW.get()
            i += 1
        return a


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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        labels_input = ["a1(um)", "a2(um)", "a3(um)", "a4(um)", "n1(%)", "n2(%)", "n3(%)", "n4(%)", "alpha"]
        values_input = [3, 2, 2.5, 15, 0.05, 0, 0, 0, 1]
        values_output = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]

        self.title("Scaling core")
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
        self.label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        time = '--:--:--'
        self.label_t = customtkinter.CTkLabel(self, text=time, fg_color="transparent")
        self.label_t.grid(row=3, column=0, padx=180, pady=(10, 0), sticky="w")

        self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
        self.progressbar.configure(height=15, corner_radius=4, progress_color='green')

    def buttonRUN_callback(self):
        # get the project directory (project)
        start_time = time.time()
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
        fiber_profile = CoreProfile(fimmap)

        values = self.frame_left.get_entry()
        values_f = np.array(values).astype(float)
        fiber_p = self.frame_right.get_menu()

        # this variable define the number of steps in terms of scaling factor
        scaling_steps = 1000
        max_scaling_factor = 2
        steps = np.linspace(1, max_scaling_factor, scaling_steps)
        a1 = np.linspace(values_f[0], values_f[0]*max_scaling_factor, scaling_steps)
        a2 = np.linspace(values_f[1], values_f[1]*max_scaling_factor, scaling_steps)
        a3 = np.linspace(values_f[2], values_f[2]*max_scaling_factor, scaling_steps)
        a4 = values_f[3]
        n1_dopant = values_f[4]
        n2_dopant = values_f[5]
        n3_dopant = values_f[6]
        n4_dopant = values_f[7]
        alpha = values_f[8]

        # creating variable to store the result
        data_scan = np.zeros(
            (scaling_steps, 10 + 9))  # 10 -> number of fiber parameters and 9-> max output of fiber_profile.mode_data()
        i = 0

        param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
                      "neffg": True, "fillFac": True, "gammaE": True}
        header = (
            ['scaling factor', 'a1(um)', 'a2(um)', 'a3(um)', 'a4(um)', 'n1 dopant(%)', 'n2 dopant(%)', 'n3 dopant(%)',
             'n4 dopant(%)', 'alpha',
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

        time_sim = str(one_sim * scaling_steps) + ' seg = ' + str(
            np.around((one_sim * scaling_steps) / 60, decimals=3)) + ' min = ' \
                   + str(np.around((one_sim * scaling_steps) / 3600, decimals=3)) + ' h'
        elapsed_time = np.zeros(scaling_steps)
        self.label_t.configure(text=time_sim)
        print('Simulation estimeted time: ' + time_sim)

        # Iterate over all scaling values
        for sca_fact in steps:
            # running the simulation
            start_time = time.time()
            fiber_profile.update_profile(dev, a1[i], a2[i], a3[i], a4, n1_dopant,
                                         n2_dopant, n3_dopant, n4_dopant,
                                         fiber_p, alpha)
            data_scan[i, 10:] = list(fiber_profile.mode_data(dev, param_Scan))
            data_scan[i, 0:10] = [sca_fact, a1[i], a2[i], a3[i], a4, n1_dopant,
                                  n2_dopant, n3_dopant, n4_dopant,
                                  alpha]

            end_time = time.time()
            elapsed_time[i] = end_time - start_time

            i = i + 1
            self.progressbar.set(i / scaling_steps)
            print(
                'Simulation goes for: ' + str(100 * i / scaling_steps) + ' %' + ' It took: ' + str(
                    elapsed_time[i - 1]))

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
