"""PROJECT PALTOP - lightweight desktop companion prototype."""

from __future__ import annotations

import json
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
SAVE_FILE = APP_DIR / "paltop_save.json"

CHARACTERS = {
    "Pip": {"emoji": "🐣", "cost": 0},
    "Mochi": {"emoji": "🐱", "cost": 30},
    "Sprout": {"emoji": "🌱", "cost": 60},
    "Orbit": {"emoji": "🪐", "cost": 100},
}

REACTIONS = [
    "You clicked me! ✨",
    "Tiny steps still count.",
    "Let's make today a good one.",
    "Task time? I've got you.",
    "Beep boop. Productivity mode!",
]

class PalTop:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PROJECT PALTOP")
        self.root.geometry("250x300+80+80")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#20283a")

        self.data = self.load_data()
        self.tasks = self.data.get("tasks", [])
        self.points = int(self.data.get("points", 0))
        self.character = self.data.get("character", "Pip")
        self.unlocked = set(self.data.get("unlocked", ["Pip"]))
        self.unlocked.add("Pip")
        self.focus_seconds = 25 * 60
        self.timer_running = False
        self.timer_job = None
        self.drag_origin = None

        self.build_ui()
        self.refresh_tasks()
        self.update_points()
        self.update_character()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_data(self):
        try:
            return json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def save_data(self):
        payload = {
            "tasks": self.tasks,
            "points": self.points,
            "character": self.character,
            "unlocked": sorted(self.unlocked),
        }
        SAVE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def build_ui(self):
        header = tk.Frame(self.root, bg="#20283a")
        header.pack(fill="x", padx=10, pady=(8, 2))
        tk.Label(header, text="PROJECT PALTOP", fg="#b8c7ff",
                 bg="#20283a", font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Button(header, text="×", command=self.on_close, relief="flat",
                  bg="#20283a", fg="white", activebackground="#39445e",
                  activeforeground="white").pack(side="right")

        self.pet_button = tk.Button(
            self.root, text="🐣", command=self.pet_clicked,
            font=("Segoe UI Emoji", 42), relief="flat",
            bg="#20283a", fg="white", activebackground="#20283a",
            activeforeground="white", cursor="hand2"
        )
        self.pet_button.pack(pady=(0, 0))

        self.reaction = tk.Label(self.root, text="Hi! I'm Pip.",
                                 fg="#e8edff", bg="#20283a",
                                 font=("Segoe UI", 9))
        self.reaction.pack(pady=(0, 7))

        self.points_label = tk.Label(self.root, text="PAL points: 0",
                                     fg="#ffd479", bg="#20283a",
                                     font=("Segoe UI", 9, "bold"))
        self.points_label.pack()

        task_frame = tk.Frame(self.root, bg="#2b354b")
        task_frame.pack(fill="both", expand=True, padx=10, pady=8)
        tk.Label(task_frame, text="TODAY'S TASKS", fg="#b8c7ff",
                 bg="#2b354b", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(7, 2))

        self.task_list = tk.Listbox(task_frame, height=4, bg="#35415b",
                                    fg="white", selectbackground="#586b91",
                                    relief="flat", font=("Segoe UI", 9),
                                    activestyle="none")
        self.task_list.pack(fill="both", expand=True, padx=7, pady=4)

        controls = tk.Frame(task_frame, bg="#2b354b")
        controls.pack(fill="x", padx=6, pady=(2, 7))
        tk.Button(controls, text="+ Add", command=self.add_task).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(controls, text="✓ Complete", command=self.complete_task).pack(side="left", expand=True, fill="x", padx=2)

        footer = tk.Frame(self.root, bg="#20283a")
        footer.pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(footer, text="Focus 25:00", command=self.toggle_focus).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(footer, text="Characters", command=self.open_characters).pack(side="left", expand=True, fill="x", padx=2)

        # Drag the borderless-feeling companion from its header or pet.
        for widget in (header, self.pet_button, self.reaction):
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag_window)

    def start_drag(self, event):
        self.drag_origin = (event.x_root - self.root.winfo_x(),
                            event.y_root - self.root.winfo_y())

    def drag_window(self, event):
        if self.drag_origin:
            x = event.x_root - self.drag_origin[0]
            y = event.y_root - self.drag_origin[1]
            self.root.geometry(f"+{x}+{y}")

    def pet_clicked(self):
        self.reaction.config(text=random.choice(REACTIONS))

    def update_points(self):
        self.points_label.config(text=f"PAL points: {self.points}")

    def refresh_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            mark = "✓" if task["done"] else "○"
            self.task_list.insert(tk.END, f"{mark} {task['title']}")

    def add_task(self):
        title = simpledialog.askstring("New task", "What would you like to get done?", parent=self.root)
        if title and title.strip():
            self.tasks.append({"title": title.strip(), "done": False})
            self.refresh_tasks()
            self.save_data()

    def complete_task(self):
        selection = self.task_list.curselection()
        if not selection:
            messagebox.showinfo("Choose a task", "Select a task first.", parent=self.root)
            return
        task = self.tasks[selection[0]]
        if task["done"]:
            return
        task["done"] = True
        self.points += 10
        self.reaction.config(text="Nice work! +10 PAL points ⭐")
        self.refresh_tasks()
        self.update_points()
        self.save_data()

    def open_characters(self):
        window = tk.Toplevel(self.root)
        window.title("PALTOP characters")
        window.configure(bg="#20283a")
        window.resizable(False, False)
        tk.Label(window, text=f"You have {self.points} PAL points",
                 fg="white", bg="#20283a", font=("Segoe UI", 10, "bold")).pack(padx=12, pady=10)

        for name, info in CHARACTERS.items():
            unlocked = name in self.unlocked
            status = "Unlocked" if unlocked else f"{info['cost']} points"
            row = tk.Frame(window, bg="#2b354b")
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=f"{info['emoji']}  {name} — {status}",
                     fg="white", bg="#2b354b", width=22, anchor="w").pack(side="left", padx=6, pady=6)
            action = "Use" if unlocked else "Unlock"
            tk.Button(row, text=action,
                      command=lambda n=name, w=window: self.select_character(n, w)).pack(side="right", padx=5)

    def select_character(self, name, window):
        cost = CHARACTERS[name]["cost"]
        if name not in self.unlocked:
            if self.points < cost:
                messagebox.showinfo("Keep earning", f"You need {cost - self.points} more PAL points.", parent=window)
                return
            self.points -= cost
            self.unlocked.add(name)
        self.character = name
        self.update_character()
        self.update_points()
        self.save_data()
        window.destroy()

    def update_character(self):
        info = CHARACTERS.get(self.character, CHARACTERS["Pip"])
        self.pet_button.config(text=info["emoji"])
        self.reaction.config(text=f"I'm {self.character}. Let's do this!")

    def toggle_focus(self):
        if self.timer_running:
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
            self.timer_running = False
            self.focus_seconds = 25 * 60
            self.reaction.config(text="Focus paused. Take a breath.")
            return
        self.timer_running = True
        self.reaction.config(text="Focus session started. You can do it!")
        self.tick_focus()

    def tick_focus(self):
        if not self.timer_running:
            return
        if self.focus_seconds <= 0:
            self.timer_running = False
            self.points += 15
            self.update_points()
            self.reaction.config(text="Focus session complete! +15 points 🎉")
            self.save_data()
            return
        minutes, seconds = divmod(self.focus_seconds, 60)
        self.root.title(f"PALTOP — Focus {minutes:02d}:{seconds:02d}")
        self.focus_seconds -= 1
        self.timer_job = self.root.after(1000, self.tick_focus)

    def on_close(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.save_data()
        self.root.destroy()


def main():
    root = tk.Tk()
    PalTop(root)
    root.mainloop()


if __name__ == "__main__":
    main()
