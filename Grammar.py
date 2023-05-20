'''
Grammar.py takes information in a specific order from a .txt file located in the "Tests" folder.
In addition, it converts the contained information into a grammar that the program can parse.
'''

class Grammar:

    #Grammar has a constructor, it contains: Productions, Initial, Non_Terminals, Terminals, Auxiliar.
    def __init__(self) -> None:
        self.Productions = {}
        self.Initial = ""
        self.Non_Terminals = set()
        self.Terminals = set()
        self.Auxiliar = set()

    #Creation of new production:
    #If the non_terminal isn't in the productions, create a new set and add production.
    def new_Production(self, no_Terminal: str, produccion: str) -> None:
        if no_Terminal not in self.Productions:
            self.Productions[no_Terminal] = set()
        self.Productions[no_Terminal].add(produccion)

    def set_Initial(self, simbol: str) -> None:
        self.Initial = simbol   #Set initial  symbol.

    def add_Terminal(self, simbol: str) -> None:
        self.Terminals.add(simbol)  #Add terminal.

    def add_Non_Terminal(self, simbol: str):
        self.Non_Terminals.add(simbol)  #Add new terminal.
        
    #Print production rules.
    def __str__(self) -> str:
        gramatica = "Reglas de Producción:\n\n"
        for no_Terminal, producciones in self.Productions.items():
            gramatica += f"  {no_Terminal} -> {' | '.join(producciones)}\n"
        return gramatica
    
    #Verify epsilon transition.
    def epsilon_Transition(self, Non_Terminal: str) -> bool:
        if 'ε' in self.Productions[Non_Terminal]:   #If ε is in the prodution set
            return True
        return False               

    #Take a grammar file and convert it into a parseable grammar.
    def from_file(self, file: str) -> None:
        #Reading file.                 
        with open(file, 'r', encoding='utf-8') as text:
            
            line = text.readline().strip()  #Reading first file's line.
            self.Initial = line.split("=")[1].strip()
            
            line = text.readline().strip()  #Reading second file's line.
            self.Non_Terminals = set(line.split("=")[1].strip().split(","))
            
            line = text.readline().strip()  #Reading third file's line.
            self.Terminals = set(line.split("=")[1].strip().split(","))
            
            line = text.readline().strip()
            line = text.readline().strip()
            #Reading the grammar production of the file and saving.
            while line:
                parts = line.split(":")
                no_terminal = parts[0].strip()
                productions = parts[1].strip().split("|")
                for p in productions:
                    self.new_Production(no_terminal, p.strip())
                line = text.readline().strip()