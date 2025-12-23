import json
import random

class EventEngine:
    def __init__(self, state):
        self.state = state
        self.recent_events = []
        self.max_memory = 4  # prevents immediate repetition

        with open("E:\Documents\Projects\Python\Procedural Survival Game\data\events.json") as f:
            self.events = json.load(f)

    def get_event(self):
        valid_events = [
            e for e in self.events
            if self.state.environment in e["environment"]
            and e["id"] not in self.recent_events
        ]

        # fallback if all events were recently used
        if not valid_events:
            self.recent_events.clear()
            valid_events = [
                e for e in self.events
                if self.state.environment in e["environment"]
            ]

        event = random.choice(valid_events)

        self.recent_events.append(event["id"])
        if len(self.recent_events) > self.max_memory:
            self.recent_events.pop(0)

        return event

    def resolve_choice(self, event, index):
        choice = event["choices"][index]
        if random.random() <= choice["probability"]:
            self.state.apply_effects(choice["effects"])
