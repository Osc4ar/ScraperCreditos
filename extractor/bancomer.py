from selenium_automaton import bancomer_automaton

class Bancomer:
    def __init__(self):
        self.automaton = bancomer_automaton.BancomerAutomaton()

if __name__ == "__main__":
    extractor = Bancomer()