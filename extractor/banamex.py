from selenium_automaton import banamex_automaton

class Banamex:
    def __init__(self):
        self.automaton = banamex_automaton.BanamexAutomaton()

if __name__ == "__main__":
    extractor = Banamex()