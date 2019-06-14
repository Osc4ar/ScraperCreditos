from selenium_automaton import inbursa_automaton

class Inbursa:
    def __init__(self):
        self.automaton = inbursa_automaton.InbursaAutomaton()

if __name__ == "__main__":
    extractor = Inbursa()