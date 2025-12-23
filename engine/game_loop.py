from engine.state_manager import GameState
from engine.event_engine import EventEngine
from ui.console_ui import ConsoleUI
import random

class GameLoop:
    def __init__(self):
        self.ui = ConsoleUI()
        self.state = GameState()
        self.event_engine = EventEngine(self.state)

    def start(self):
        self.ui.intro(self.state.environment)

        while self.state.is_alive():
            self.ui.display_stats(self.state)
            event = self.event_engine.get_event()
            choice = self.ui.present_event(event)
            self.event_engine.resolve_choice(event, choice)

            self.state.tick()

        self.ui.game_over(self.state)
