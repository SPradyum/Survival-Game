import tkinter as tk
from tkinter import ttk
import json
from engine.state_manager import GameState
from engine.event_engine import EventEngine

class SurvivalGameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echoes of Survival")
        self.root.geometry("900x600")
        self.root.configure(bg="#121212")

        self.container = tk.Frame(self.root, bg="#121212")
        self.container.pack(fill="both", expand=True)

        self.state = None
        self.engine = None

        self.show_instructions()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ---------- INSTRUCTIONS ----------
    def show_instructions(self):
        self.clear()

        tk.Label(
            self.container,
            text="ECHOES OF SURVIVAL",
            fg="#e53935",
            bg="#121212",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=15)

        tk.Label(
            self.container,
            text=(
                "A procedural survival experience.\n\n"
                "• Every decision has consequences\n"
                "• Resources drain fast\n"
                "• Morality shapes your ending\n\n"
                "Survive. Adapt. Decide."
            ),
            fg="#cccccc",
            bg="#121212",
            font=("Segoe UI", 14),
            justify="center"
        ).pack(pady=20)

        tk.Button(
            self.container,
            text="BEGIN SURVIVAL",
            font=("Segoe UI", 14, "bold"),
            bg="#e53935",
            fg="white",
            width=20,
            command=self.start_game
        ).pack(pady=15)

    # ---------- GAME ----------
    def start_game(self):
        self.state = GameState()
        self.engine = EventEngine(self.state)
        self.next_turn()

    def draw_bar(self, label, value):
        frame = tk.Frame(self.container, bg="#121212")
        frame.pack(fill="x", padx=40, pady=3)

        tk.Label(frame, text=label, fg="white", bg="#121212", width=10).pack(side="left")

        bar = ttk.Progressbar(frame, maximum=100, value=value)
        bar.pack(fill="x", expand=True, side="left", padx=10)

    def next_turn(self):
        if not self.state.is_alive():
            self.game_over()
            return

        self.clear()
        event = self.engine.get_event()

        tk.Label(
            self.container,
            text=f"ENVIRONMENT: {self.state.environment.upper()} | TURN {self.state.turn}",
            fg="#ffb300",
            bg="#121212",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=5)

        self.draw_bar("Health", self.state.health)
        self.draw_bar("Hunger", self.state.hunger)
        self.draw_bar("Energy", self.state.energy)
        self.draw_bar("Morale", self.state.morale)

        tk.Label(
            self.container,
            text=event["description"],
            fg="#00e5ff",
            bg="#121212",
            font=("Segoe UI", 16),
            wraplength=750
        ).pack(pady=30)

        for i, choice in enumerate(event["choices"]):
            tk.Button(
                self.container,
                text=choice["text"],
                font=("Segoe UI", 13),
                bg="#263238",
                fg="white",
                activebackground="#37474f",
                width=60,
                command=lambda i=i, e=event: self.choose(e, i)
            ).pack(pady=6)

    def choose(self, event, index):
        self.engine.resolve_choice(event, index)
        self.state.tick()
        self.next_turn()

    # ---------- GAME OVER ----------
    def game_over(self):
        self.clear()
        with open("E:\Documents\Projects\Python\Procedural Survival Game\data\endings.json") as f:
            endings = json.load(f)

        if self.state.reputation >= 5:
            ending = endings["leader"]
        elif self.state.morale <= 0:
            ending = endings["paranoia"]
        else:
            ending = endings["lone"]

        tk.Label(
            self.container,
            text="YOU DID NOT SURVIVE",
            fg="#e53935",
            bg="#121212",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=20)

        tk.Label(
            self.container,
            text=ending,
            fg="white",
            bg="#121212",
            font=("Segoe UI", 16),
            wraplength=700
        ).pack(pady=25)

        tk.Button(
            self.container,
            text="PLAY AGAIN",
            font=("Segoe UI", 13),
            width=18,
            command=self.show_instructions
        ).pack(pady=15)

    def run(self):
        self.root.mainloop()
