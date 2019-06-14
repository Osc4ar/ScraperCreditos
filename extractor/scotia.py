from selenium_automaton import scotia_automaton

class Scotia:
    def __init__(self):
        self.automaton = scotia_automaton.ScotiaAutomaton()

if __name__ == "__main__":
    extractor = Scotia()