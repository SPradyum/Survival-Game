class ChoiceResolver:
    def __init__(self, state):
        self.state = state

    def apply(self, effects):
        self.state.apply_effects(effects)
