import random
import json

class GameState:
    def __init__(self):
        with open("E:\Documents\Projects\Python\Procedural Survival Game\data\environments.json") as f:
            self.environment = random.choice(list(json.load(f).keys()))

        self.health = 70
        self.hunger = 60
        self.energy = 60
        self.morale = 60
        self.reputation = 0
        self.turn = 1

    def apply_effects(self, effects):
        for stat, value in effects.items():
            setattr(self, stat, max(0, getattr(self, stat) + value))

    def tick(self):
        self.turn += 1
        self.hunger -= 5
        self.energy -= 4

        if self.hunger <= 0:
            self.health -= 10

        if self.energy <= 0:
            self.morale -= 8

    def is_alive(self):
        return self.health > 0 and self.morale > 0
