class Grammar:

    def __init__(self) -> None:
        self.Productions = {}
        self.Initial = ""
        self.Non_Terminals = set()
        self.Terminals = set()
        self.Auxiliar = set()

    def new_Production(self, no_Terminal: str, produccion: str) -> None:
        if no_Terminal not in self.Productions:
            self.Productions[no_Terminal] = set()
        self.Productions[no_Terminal].add(produccion)

    def set_Initial(self, simbol: str) -> None:
        self.Initial = simbol

    def add_Terminal(self, simbol: str) -> None:
        self.Terminals.add(simbol)

    def add_Non_Terminal(self, simbol: str):
        self.Non_Terminals.add(simbol)
        
    def __str__(self) -> str:
        gramatica = "Reglas de Producción:\n\n"
        for no_Terminal, producciones in self.Productions.items():
            gramatica += f"  {no_Terminal} -> {' | '.join(producciones)}\n"
        return gramatica
    
    def epsilon_Transition(self, Non_Terminal: str) -> bool:
        if 'ε' in self.Productions[Non_Terminal]:
            return True
        return False               
                            
    def from_file(self, file: str) -> None:
        with open(file, 'r', encoding='utf-8') as text:
            
            line = text.readline().strip()
            self.Initial = line.split("=")[1].strip()
            
            line = text.readline().strip()
            self.Non_Terminals = set(line.split("=")[1].strip().split(","))
            
            line = text.readline().strip()
            self.Terminals = set(line.split("=")[1].strip().split(","))
            
            line = text.readline().strip()
            line = text.readline().strip()
            while line:
                parts = line.split(":")
                no_terminal = parts[0].strip()
                productions = parts[1].strip().split("|")
                for p in productions:
                    self.new_Production(no_terminal, p.strip())
                line = text.readline().strip()