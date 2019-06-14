from selenium_automaton import banorte_automaton

class Banorte:
    def __init__(self):
        self.automaton = banorte_automaton.BanorteAutomaton()

if __name__ == "__main__":
    extractor = Banorte()