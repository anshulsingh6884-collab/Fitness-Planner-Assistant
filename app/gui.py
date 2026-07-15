"""Strive AI — Fitness Planner (Desktop)

A self-contained Python desktop app (CustomTkinter) that:
  1. Takes a user's profile (age, weight, height, goal, activity, diet pref)
  2. Runs it through a rule/formula based 'AI' planning engine
  3. Shows a Dashboard (BMI/BMR/TDEE/macros), a weekly Workout Plan,
     a Diet Plan, and an offline AI Assistant chat tab.

Run with:  python main.py
"""

import customtkinter as ctk
from tkinter import messagebox

from app.planner import calculate_targets, generate_workout_plan, generate_diet_plan, WEEK_DAYS
from app.assistant import get_response
from app.storage import save_data, load_data

ctk.set_appearance_mode("dark")

GREEN = "#34e07a"
GREEN_DIM = "#1b3a2a"
BG = "#0a0f0d"
CARD = "#121c19"
TEXT_MUTED = "#8a9a93"


class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master, text=text, command=command,
            anchor="w", corner_radius=10, height=40,
            fg_color="transparent", hover_color=GREEN_DIM,
            text_color="#e6efe9", font=ctk.CTkFont(size=13, weight="bold"),
            **kwargs,
        )


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Strive AI — Fitness Planner")
        self.geometry("1080x680")
        self.minsize(920, 600)
        self.configure(fg_color=BG)

        # ---- shared state ----
        self.profile = {}
        self.targets = {}
        self.workout_plan = {}
        self.diet_plan = {}

        self._build_layout()
        self._try_restore_saved_data()

    # ------------------------------------------------------------------
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=210, fg_color=CARD, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        logo = ctk.CTkLabel(sidebar, text="STRIVE  AI", font=ctk.CTkFont(size=19, weight="bold"),
                             text_color=GREEN)
        logo.pack(pady=(26, 30), padx=20, anchor="w")

        self.nav_buttons = {}
        nav_items = [
            ("Profile", self.show_profile),
            ("Dashboard", self.show_dashboard),
            ("Workout Plan", self.show_workout),
            ("Diet Plan", self.show_diet),
            ("AI Assistant", self.show_assistant),
        ]
        for name, cmd in nav_items:
            btn = SidebarButton(sidebar, text=name, command=cmd)
            btn.pack(fill="x", padx=14, pady=4)
            self.nav_buttons[name] = btn

        # Content area (container holding stacked frames)
        container = ctk.CTkFrame(self, fg_color=BG)
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame, name in [
            (ProfileFrame, "Profile"),
            (DashboardFrame, "Dashboard"),
            (WorkoutFrame, "Workout Plan"),
            (DietFrame, "Diet Plan"),
            (AssistantFrame, "AI Assistant"),
        ]:
            f = Frame(container, self)
            f.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = f

        self.show_profile()

    def _set_active(self, name):
        for n, btn in self.nav_buttons.items():
            btn.configure(fg_color=GREEN_DIM if n == name else "transparent",
                          text_color=GREEN if n == name else "#e6efe9")

    def show_profile(self):
        self._set_active("Profile")
        self.frames["Profile"].tkraise()

    def show_dashboard(self):
        self._set_active("Dashboard")
        self.frames["Dashboard"].refresh()
        self.frames["Dashboard"].tkraise()

    def show_workout(self):
        self._set_active("Workout Plan")
        self.frames["Workout Plan"].refresh()
        self.frames["Workout Plan"].tkraise()

    def show_diet(self):
        self._set_active("Diet Plan")
        self.frames["Diet Plan"].refresh()
        self.frames["Diet Plan"].tkraise()

    def show_assistant(self):
        self._set_active("AI Assistant")
        self.frames["AI Assistant"].tkraise()

    # ------------------------------------------------------------------
    def generate_plan(self, profile: dict):
        """Called by ProfileFrame once the user submits the form."""
        self.profile = profile
        self.targets = calculate_targets(profile)
        self.workout_plan = generate_workout_plan(profile)
        self.diet_plan = generate_diet_plan(profile, self.targets)
        save_data(self.profile, self.targets, self.workout_plan, self.diet_plan)
        self.show_dashboard()

    def _try_restore_saved_data(self):
        saved = load_data()
        if saved:
            self.profile = saved.get("profile", {})
            self.targets = saved.get("targets", {})
            self.workout_plan = saved.get("workout_plan", {})
            self.diet_plan = saved.get("diet_plan", {})
            if self.profile:
                self.frames["Profile"].prefill(self.profile)


# =========================================================================
class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master, app: App):
        super().__init__(master, fg_color=BG)
        self.app = app

        wrap = ctk.CTkScrollableFrame(self, fg_color=BG)
        wrap.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(wrap, text="Your Profile", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(wrap, text="Fill this in and I'll build your personalised workout + diet plan.",
                     text_color=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        form = ctk.CTkFrame(wrap, fg_color=CARD, corner_radius=16)
        form.pack(fill="x", pady=10)
        form.grid_columnconfigure((0, 1), weight=1, uniform="col")

        pad = {"padx": 20, "pady": (14, 4)}

        # Name
        ctk.CTkLabel(form, text="Name").grid(row=0, column=0, sticky="w", **pad)
        self.name_entry = ctk.CTkEntry(form, placeholder_text="e.g. Rahul")
        self.name_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        # Age
        ctk.CTkLabel(form, text="Age").grid(row=0, column=1, sticky="w", **pad)
        self.age_entry = ctk.CTkEntry(form, placeholder_text="e.g. 24")
        self.age_entry.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 10))

        # Gender
        ctk.CTkLabel(form, text="Gender").grid(row=2, column=0, sticky="w", **pad)
        self.gender_menu = ctk.CTkOptionMenu(form, values=["Male", "Female"], fg_color=GREEN_DIM,
                                             button_color=GREEN_DIM, button_hover_color="#254a35")
        self.gender_menu.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

        # Weight
        ctk.CTkLabel(form, text="Weight (kg)").grid(row=2, column=1, sticky="w", **pad)
        self.weight_entry = ctk.CTkEntry(form, placeholder_text="e.g. 70")
        self.weight_entry.grid(row=3, column=1, sticky="ew", padx=20, pady=(0, 10))

        # Height
        ctk.CTkLabel(form, text="Height (cm)").grid(row=4, column=0, sticky="w", **pad)
        self.height_entry = ctk.CTkEntry(form, placeholder_text="e.g. 175")
        self.height_entry.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 10))

        # Activity level
        ctk.CTkLabel(form, text="Activity Level").grid(row=4, column=1, sticky="w", **pad)
        self.activity_menu = ctk.CTkOptionMenu(form, values=[
            "Sedentary (little/no exercise)",
            "Lightly active (1-3 days/week)",
            "Moderately active (3-5 days/week)",
            "Very active (6-7 days/week)",
        ], fg_color=GREEN_DIM, button_color=GREEN_DIM, button_hover_color="#254a35")
        self.activity_menu.grid(row=5, column=1, sticky="ew", padx=20, pady=(0, 10))

        # Goal
        ctk.CTkLabel(form, text="Goal").grid(row=6, column=0, sticky="w", **pad)
        self.goal_menu = ctk.CTkOptionMenu(form, values=["Lose Weight", "Maintain Weight", "Gain Muscle"],
                                           fg_color=GREEN_DIM, button_color=GREEN_DIM, button_hover_color="#254a35")
        self.goal_menu.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 10))

        # Diet preference
        ctk.CTkLabel(form, text="Diet Preference").grid(row=6, column=1, sticky="w", **pad)
        self.diet_menu = ctk.CTkOptionMenu(form, values=["Vegetarian", "Non-Vegetarian", "Vegan"],
                                           fg_color=GREEN_DIM, button_color=GREEN_DIM, button_hover_color="#254a35")
        self.diet_menu.grid(row=7, column=1, sticky="ew", padx=20, pady=(0, 10))

        # Workout days per week
        ctk.CTkLabel(form, text="Workout Days / Week").grid(row=8, column=0, sticky="w", **pad)
        self.days_menu = ctk.CTkOptionMenu(form, values=["3", "4", "5", "6"],
                                           fg_color=GREEN_DIM, button_color=GREEN_DIM, button_hover_color="#254a35")
        self.days_menu.grid(row=9, column=0, sticky="ew", padx=20, pady=(0, 20))

        generate_btn = ctk.CTkButton(wrap, text="Generate My AI Plan", height=44,
                                     fg_color=GREEN, hover_color="#28c169", text_color="#06120c",
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     command=self._on_generate)
        generate_btn.pack(fill="x", pady=(20, 0))

    def prefill(self, profile: dict):
        try:
            self.name_entry.insert(0, profile.get("name", ""))
            self.age_entry.insert(0, str(profile.get("age", "")))
            self.weight_entry.insert(0, str(profile.get("weight", "")))
            self.height_entry.insert(0, str(profile.get("height", "")))
            self.gender_menu.set(profile.get("gender", "Male"))
            self.activity_menu.set(profile.get("activity_level", "Lightly active (1-3 days/week)"))
            self.goal_menu.set(profile.get("goal", "Maintain Weight"))
            self.diet_menu.set(profile.get("diet_pref", "Vegetarian"))
            self.days_menu.set(str(profile.get("workout_days", 4)))
        except Exception:
            pass

    def _on_generate(self):
        try:
            name = self.name_entry.get().strip() or "Athlete"
            age = int(self.age_entry.get())
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if not (10 <= age <= 100 and 20 <= weight <= 300 and 100 <= height <= 250):
                raise ValueError("out of range")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for age, weight, and height.")
            return

        profile = {
            "name": name,
            "age": age,
            "gender": self.gender_menu.get(),
            "weight": weight,
            "height": height,
            "activity_level": self.activity_menu.get(),
            "goal": self.goal_menu.get(),
            "diet_pref": self.diet_menu.get(),
            "workout_days": int(self.days_menu.get()),
        }
        self.app.generate_plan(profile)


# =========================================================================
class StatCard(ctk.CTkFrame):
    def __init__(self, master, label, value, sub=""):
        super().__init__(master, fg_color=CARD, corner_radius=16)
        ctk.CTkLabel(self, text=label.upper(), font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXT_MUTED).pack(anchor="w", padx=18, pady=(16, 2))
        ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=GREEN).pack(anchor="w", padx=18)
        if sub:
            ctk.CTkLabel(self, text=sub, font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(
                anchor="w", padx=18, pady=(2, 16))
        else:
            ctk.CTkLabel(self, text="").pack(pady=(0, 8))


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app: App):
        super().__init__(master, fg_color=BG)
        self.app = app
        self.body = None
        self._build_placeholder()

    def _build_placeholder(self):
        self.placeholder = ctk.CTkLabel(self, text="Fill in your Profile first to generate a plan.",
                                        text_color=TEXT_MUTED, font=ctk.CTkFont(size=15))
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def refresh(self):
        if self.body:
            self.body.destroy()
            self.body = None
        if not self.app.targets:
            self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
            return
        self.placeholder.place_forget()

        t = self.app.targets
        p = self.app.profile

        self.body = ctk.CTkScrollableFrame(self, fg_color=BG)
        self.body.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(self.body, text=f"Hey {p.get('name', '')}, here's your dashboard",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(self.body, text=f"Goal: {p.get('goal', '')}  ·  {p.get('workout_days', '')} workout days/week",
                     text_color=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        grid = ctk.CTkFrame(self.body, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="c")

        StatCard(grid, "BMI", f"{t['bmi']}", t["bmi_category"]).grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        StatCard(grid, "BMR", f"{t['bmr']} kcal", "at rest").grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        StatCard(grid, "TDEE", f"{t['tdee']} kcal", "maintenance").grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
        StatCard(grid, "Daily Target", f"{t['calorie_target']} kcal", "for your goal").grid(
            row=0, column=3, sticky="nsew", padx=6, pady=6)

        macro_card = ctk.CTkFrame(self.body, fg_color=CARD, corner_radius=16)
        macro_card.pack(fill="x", pady=16)
        ctk.CTkLabel(macro_card, text="Daily Macro Targets", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=20, pady=(16, 10))
        macro_row = ctk.CTkFrame(macro_card, fg_color="transparent")
        macro_row.pack(fill="x", padx=20, pady=(0, 20))
        for label, val, color in [
            ("Protein", f"{t['protein_g']} g", GREEN),
            ("Carbs", f"{t['carb_g']} g", "#6fb3e0"),
            ("Fat", f"{t['fat_g']} g", "#e0a15c"),
        ]:
            col = ctk.CTkFrame(macro_row, fg_color="transparent")
            col.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(col, text=label, text_color=TEXT_MUTED, font=ctk.CTkFont(size=12)).pack(anchor="w")
            ctk.CTkLabel(col, text=val, font=ctk.CTkFont(size=18, weight="bold"), text_color=color).pack(anchor="w")

        tip = ("You're in a calorie deficit to lose weight steadily." if p.get("goal") == "Lose Weight" else
               "You're in a slight surplus to support muscle growth." if p.get("goal") == "Gain Muscle" else
               "You're eating at maintenance to hold your current weight.")
        ctk.CTkLabel(self.body, text=tip, text_color=TEXT_MUTED, wraplength=700, justify="left").pack(
            anchor="w", pady=(0, 10))


# =========================================================================
class WorkoutFrame(ctk.CTkFrame):
    def __init__(self, master, app: App):
        super().__init__(master, fg_color=BG)
        self.app = app
        self.body = None
        self.placeholder = ctk.CTkLabel(self, text="Generate a plan from the Profile tab first.",
                                        text_color=TEXT_MUTED, font=ctk.CTkFont(size=15))
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def refresh(self):
        if self.body:
            self.body.destroy()
            self.body = None
        if not self.app.workout_plan:
            self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
            return
        self.placeholder.place_forget()

        self.body = ctk.CTkScrollableFrame(self, fg_color=BG)
        self.body.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(self.body, text="Weekly Workout Plan", font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", pady=(0, 16))

        for day in WEEK_DAYS:
            info = self.app.workout_plan.get(day)
            if not info:
                continue
            card = ctk.CTkFrame(self.body, fg_color=CARD, corner_radius=16)
            card.pack(fill="x", pady=6)

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=(14, 6))
            ctk.CTkLabel(header, text=day, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
            ctk.CTkLabel(header, text=info["type"], text_color=GREEN,
                         font=ctk.CTkFont(size=12, weight="bold")).pack(side="right")

            for name, sets, reps in info["exercises"]:
                row = ctk.CTkFrame(card, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=2)
                ctk.CTkLabel(row, text=f"•  {name}", anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=f"{sets} x {reps}" if sets != "-" else "",
                             text_color=TEXT_MUTED).pack(side="right")
            ctk.CTkLabel(card, text="").pack(pady=(0, 8))  # bottom spacing


# =========================================================================
class DietFrame(ctk.CTkFrame):
    def __init__(self, master, app: App):
        super().__init__(master, fg_color=BG)
        self.app = app
        self.body = None
        self.placeholder = ctk.CTkLabel(self, text="Generate a plan from the Profile tab first.",
                                        text_color=TEXT_MUTED, font=ctk.CTkFont(size=15))
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def refresh(self):
        if self.body:
            self.body.destroy()
            self.body = None
        if not self.app.diet_plan:
            self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
            return
        self.placeholder.place_forget()

        self.body = ctk.CTkScrollableFrame(self, fg_color=BG)
        self.body.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(self.body, text="Today's Diet Plan", font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", pady=(0, 4))
        ctk.CTkLabel(self.body, text=f"Target: {self.app.targets.get('calorie_target', '-')} kcal "
                                     f"({self.app.profile.get('diet_pref', '')})",
                     text_color=TEXT_MUTED).pack(anchor="w", pady=(0, 16))

        for meal, info in self.app.diet_plan.items():
            card = ctk.CTkFrame(self.body, fg_color=CARD, corner_radius=16)
            card.pack(fill="x", pady=6)
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=16)
            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(left, text=meal, font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=GREEN).pack(anchor="w")
            ctk.CTkLabel(left, text=info["suggestion"], wraplength=560, justify="left").pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(row, text=f"~{info['approx_calories']} kcal", text_color=TEXT_MUTED).pack(side="right")


# =========================================================================
class AssistantFrame(ctk.CTkFrame):
    def __init__(self, master, app: App):
        super().__init__(master, fg_color=BG)
        self.app = app

        ctk.CTkLabel(self, text="AI Fitness Assistant", font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", padx=40, pady=(30, 4))
        ctk.CTkLabel(self, text="Ask about protein, calories, workouts, diet, sleep, or motivation.",
                     text_color=TEXT_MUTED).pack(anchor="w", padx=40, pady=(0, 16))

        self.chat_box = ctk.CTkTextbox(self, fg_color=CARD, corner_radius=16, wrap="word",
                                       font=ctk.CTkFont(size=13))
        self.chat_box.pack(fill="both", expand=True, padx=40, pady=(0, 12))
        self.chat_box.configure(state="disabled")

        input_row = ctk.CTkFrame(self, fg_color="transparent")
        input_row.pack(fill="x", padx=40, pady=(0, 30))
        self.entry = ctk.CTkEntry(input_row, placeholder_text="Type your question…", height=40)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self._send())
        ctk.CTkButton(input_row, text="Send", width=90, height=40, fg_color=GREEN, hover_color="#28c169",
                     text_color="#06120c", font=ctk.CTkFont(weight="bold"), command=self._send).pack(side="left")

        self._append("Assistant", "Hi! I'm your offline fitness assistant. Ask me anything about your plan.")

    def _append(self, who, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{who}: {text}\n\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def _send(self):
        question = self.entry.get().strip()
        if not question:
            return
        self.entry.delete(0, "end")
        self._append("You", question)
        reply = get_response(question, self.app.profile, self.app.targets)
        self._append("Assistant", reply)

