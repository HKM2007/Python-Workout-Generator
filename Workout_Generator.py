import tkinter as tk
from tkinter import ttk, messagebox
import random

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Generator")
        self.root.geometry("580x450")
        self.root.configure(bg="#e6f0ff")  

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#e6f0ff", foreground="#023047", font=("Helvetica", 11))
        style.configure("TButton", background="#0077b6", foreground="#023047", font=("Helvetica", 11), padding=6)
        style.configure("TEntry", padding=4)


        self.exercises = self.get_exercise_data()
        self.daily_plans = []
        self.water_logs = []
        self.step_logs = []
        self.workout_streak = 0
        self.current_day = 1

        self.create_input_ui()

    def create_input_ui(self):
        self.clear_window()
        
        ttk.Label(self.root,text="✨ Welcome To Your Personalized Workout Generator ✨",font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        ttk.Label(self.root,text="🙏Please Enter The Details Below🙏",font=("Helvetica", 14, "bold")).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self.root, text="👤 Name:").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=10, column=1)

        ttk.Label(self.root, text="🚻 Gender:").grid(row=15, column=0, sticky="w", padx=10)
        self.gender_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.gender_var, values=["Male", "Female"]).grid(row=15, column=1)

        ttk.Label(self.root, text="🎯 Fitness Goal:").grid(row=20, column=0, sticky="w", padx=10)
        self.goal_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.goal_var, values=["1 - Weight Loss", "2 - Muscle Gain", "3 - Strength Training", "4 - General Fitness"]).grid(row=20, column=1)

        ttk.Label(self.root, text="📈 Level:").grid(row=25, column=0, sticky="w", padx=10)
        self.level_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.level_var, values=["1 - Beginner", "2 - Intermediate", "3 - Advanced"]).grid(row=25, column=1)

        ttk.Label(self.root, text="📅 Days per Week:").grid(row=30, column=0, sticky="w", padx=10)
        self.days_entry = ttk.Entry(self.root)
        self.days_entry.grid(row=30, column=1)

        ttk.Label(self.root, text="💧 Water Goal (glasses/day):").grid(row=35, column=0, sticky="w", padx=10)
        self.water_entry = ttk.Entry(self.root)
        self.water_entry.grid(row=35, column=1)

        ttk.Label(self.root, text="👟 Step Goal (per day):").grid(row=40, column=0, sticky="w", padx=10)
        self.step_entry = ttk.Entry(self.root)
        self.step_entry.grid(row=40, column=1)

        ttk.Button(self.root, text="Start Plan", command=self.start_plan).grid(row=45, column=0, columnspan=2, pady=15)

    def start_plan(self):
        try:
            self.name = self.name_entry.get()
            self.goal = self.goal_var.get()[0]
            self.level = self.level_var.get()[0]
            self.total_days = int(self.days_entry.get())
            self.water_target = int(self.water_entry.get())
            self.step_target = int(self.step_entry.get())
        except:
            messagebox.showerror("Input Error", "Please enter valid values for all fields.")
            return

        self.show_workout_day()

    def show_workout_day(self):
        self.clear_window()

        if self.current_day > self.total_days:
            self.show_summary()
            return

        ttk.Label(self.root, text=f"📅 Day {self.current_day}", font=("Helvetica", 16)).pack(pady=10)

        if self.workout_streak == 2:
            ttk.Label(self.root, text="💤 Rest Day!").pack()
            self.daily_plans.append("Rest")
            self.water_logs.append(None)
            self.step_logs.append(None)
            self.workout_streak = 0
            self.current_day += 1
            ttk.Button(self.root, text="Next Day ➡️", command=self.show_workout_day).pack(pady=20)
        else:
            plan = random.sample(self.exercises[self.goal][self.level], 5)
            self.daily_plans.append(plan)

            workout_frame = ttk.Frame(self.root)
            workout_frame.pack()
            workout_frame.pack_propagate(True) 
            for i, ex in enumerate(plan, 1):
                ttk.Label(workout_frame, text=f"{i}. ✨ {ex}").pack(anchor="w")

            
            self.water_today = tk.IntVar()
            self.step_today = tk.IntVar()

            ttk.Label(self.root, text=f"\n💧 Water intake today (glasses):").pack()
            ttk.Entry(self.root, textvariable=self.water_today).pack()

            ttk.Label(self.root, text="👟 Steps walked today:").pack()
            ttk.Entry(self.root, textvariable=self.step_today).pack()

            ttk.Button(self.root, text="Submit Day", command=self.submit_day).pack(pady=20)

    def submit_day(self):
        try:
            water = self.water_today.get()
            steps = self.step_today.get()
            self.water_logs.append(water)
            self.step_logs.append(steps)
        except:
            messagebox.showerror("Input Error", "Enter valid water/step numbers.")
            return

        self.workout_streak += 1
        self.current_day += 1
        self.show_workout_day()

    def show_summary(self):
        self.clear_window()
        ttk.Label(self.root, text="📊 Weekly Summary", font=("Helvetica", 16)).pack(pady=10)

        for i in range(self.total_days):
            day_text = f"Day {i+1}: "
            if self.daily_plans[i] == "Rest":
                day_text += "💤 Rest Day"
            else:
                w = self.water_logs[i]
                s = self.step_logs[i]
                day_text += f"    💧 {(w/self.water_target)*100}% Water Intake Completed from target\n\t👟 {(s/self.step_target)*100}% Steps Completed from Target"
            ttk.Label(self.root, text=day_text).pack(anchor="w")

        ttk.Button(self.root, text="🏁 Restart", command=self.reset).pack(pady=15)

    def reset(self):
        self.daily_plans = []
        self.water_logs = []
        self.step_logs = []
        self.workout_streak = 0
        self.current_day = 1
        self.create_input_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_exercise_data(self):
        return {
            "1": {  # Weight Loss
                "1": ["Jumping Jacks", "High Knees", "Wall Sit", "Plank Hold", "Bodyweight Squats"],
                "2": ["Burpees", "Mountain Climbers", "Jump Rope", "Lunges", "Push-ups"],
                "3": ["Sprints", "Box Jumps", "Skater Hops", "Jump Lunges", "Bear Crawls"]
            },
            "2": {  # Muscle Gain
                "1": ["Bodyweight Squats", "Wall Push-ups", "Glute Bridges", "Superman Holds", "Wall Sit"],
                "2": ["Push-ups", "Lunges", "Dips", "Step-ups", "Diamond Push-ups"],
                "3": ["Pistol Squats", "Pull-ups", "Decline Push-ups", "Split Squats", "Handstand Holds"]
            },
            "3": {  # Strength Training
                "1": ["Wall Sit", "Incline Push-ups", "Glute Bridges", "Calf Raises", "Dead Bug"],
                "2": ["Push-ups", "Lunges", "Chair Dips", "Step-ups", "Side Plank"],
                "3": ["Decline Push-ups", "Pistol Squats", "Plank Push-ups", "Split Squats", "Jump Squats"]
            },
            "4": {  # General Fitness
                "1": ["Neck Rolls", "Shoulder Circles", "Arm Swings", "Wall Push-ups", "Marching in Place"],
                "2": ["Toe Touches", "Knee Push-ups", "Side Lunges", "Wall Sit", "Reverse Lunges"],
                "3": ["Side Plank", "Speed Skaters", "Mountain Climbers", "Jumping Lunges", "Push-ups"]
            }
        }

root = tk.Tk()
app = WorkoutApp(root)
root.mainloop()

