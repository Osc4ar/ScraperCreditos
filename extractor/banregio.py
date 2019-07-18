from selenium_automaton import banregio_automaton
from selenium_automaton import banregio_general

class Banregio:
    def __init__(self):
        #banregio_automaton.BanregioAutomaton()
        #banregio_general.BanregioGeneral('https://www.banregio.com/cot_terreno.php', 5, 100)
        #banregio_general.BanregioGeneral('https://www.banregio.com/cot_term.php', 5, 100)
        banregio_general.BanregioGeneral('https://www.banregio.com/cot_mejora.php', 5, 100)
        #banregio_general.BanregioGeneral('https://www.banregio.com/cot_remo.php', 5, 100)

if __name__ == "__main__":
    extractor = Banregio()