from selenium_automaton import banregio_automaton

class Banregio:
    def __init__(self):
        self.automaton = banregio_automaton.BanregioAutomaton()

if __name__ == "__main__":
    extractor = Banregio()