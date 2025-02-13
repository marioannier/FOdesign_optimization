import tkinter as tk
from tkinter import messagebox
import sys
class SimulationTimeWind:
    def __init__(self):
        stop = False

    def show_confirmation_window(self, prof, steps):
        # one simulation time depending on the index profile
        self.stop = False
        match prof:
            case 'steps':
                case_time = 2
            case 'triangular':
                case_time = 10
            case 'graded':
                case_time = 8
            case 'raised cosine':
                case_time = 35

        hours = case_time * steps / 3600

        window = tk.Tk()
        window.title("Simulation Confirmation")

        # Center the window on the screen
        window_width = 300
        window_height = 150
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        message = f"The simulation will take {hours.__round__(2)} hours. Do you want to continue?"

        label = tk.Label(window, text=message, wraplength=250, justify='center', font=('Helvetica', 12))
        label.pack(padx=10, pady=10)

        frame = tk.Frame(window)
        frame.pack(pady=10)

        def on_yes():
            window.destroy()
            self.stop = True

        def on_no():
            window.destroy()

        yes_button = tk.Button(frame, text="Yes", command=on_yes, width=10, pady=5)
        yes_button.pack(side=tk.LEFT, padx=5)

        no_button = tk.Button(frame, text="No", command=on_no, width=10, pady=5)
        no_button.pack(side=tk.RIGHT, padx=5)

        window.mainloop()
        return self.stop
