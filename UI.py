import customtkinter


class MyFrameleft(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []
        self.labels = []
        self.entries = []
        self.matte_red = ('#FF6666', '#993333')
        self.matte_green = ('#66CC66', '#336633')

        self.title = customtkinter.CTkLabel(self, text="Variable", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=3, padx=0, pady=(10, 0), sticky="w")

        self.title = customtkinter.CTkLabel(self, text="Steps", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=4, padx=0, pady=(10, 0), sticky="w")

        for i, value in enumerate(self.values):
            # label
            label = customtkinter.CTkLabel(self, text=value)
            label.grid(row=i + 1, column=0, padx=10, pady=(10, 0))
            self.labels.append(label)
            # entries, lower value
            entry = customtkinter.CTkEntry(self, placeholder_text="Enter the value", fg_color=self.matte_green)
            entry.grid(row=i + 1, column=1, padx=10, pady=(10, 0))
            # self.entries.append(entry)
            # entries, upper value
            entry = customtkinter.CTkEntry(self, placeholder_text="Enter the value", fg_color=self.matte_red)
            entry.grid(row=i + 1, column=2, padx=10, pady=(10, 0))
            entry.configure(state="disabled")
            self.entries.append(entry)
            # check boxes
            checkbox = customtkinter.CTkCheckBox(self, text="", command=self.action_check)
            checkbox.grid(row=i + 1, column=3, padx=10, pady=(10, 0))
            self.checkboxes.append(checkbox)
            # number of steps
            entry = customtkinter.CTkEntry(self, placeholder_text="----")
            entry.grid(row=i + 1, column=4, padx=(0, 30), pady=(10, 0), sticky="e")
            # self.entries.append(entry)
            entry.configure(width=50)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(True)
            else:
                checked_checkboxes.append(False)
        return checked_checkboxes

    def action_check(self):
        i = 0
        for entry in self.entries:
            a = self.checkboxes[i].get()
            if a == 1:
                entry.configure(state="normal", fg_color=self.matte_green)
            else:
                entry.configure(state="disable", fg_color=self.matte_red)

            i = i + 1


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

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(True)
            else:
                checked_checkboxes.append(False)
        return checked_checkboxes


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        values_input = ["a1(um)", "a2(um)", "a3(um)", "a4(um)", "n1(%)", "n2(%)", "n3(%)", "n4(%)", "alpha"]
        values_output = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]

        self.title("Scan")
        self.geometry("900x500")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame_1 = MyFrameleft(self, values_input)
        self.checkbox_frame_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        choice = "Step Index"
        self.checkbox_frame_2 = MyFrameright(self, "Output", values_output, choice)
        self.checkbox_frame_2.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="RUN", command=self.button_callback)
        self.button.grid(row=3, column=1, padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self, text="Estimated simulation time", fg_color="transparent")
        self.label.grid(row=3, column=0, padx=100, pady=(10, 0), sticky="w")

        time = '00:00:00'
        self.label = customtkinter.CTkLabel(self, text=time, fg_color="transparent")
        self.label.grid(row=3, column=0, padx=100, pady=(10, 0), sticky="e")

    def button_callback(self):
        print("checkbox_frame_1:", self.checkbox_frame_1.get())
        print("checkbox_frame_2:", self.checkbox_frame_2.get())


app = App()
app.mainloop()
