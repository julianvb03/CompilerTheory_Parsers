from Grammar import Grammar
from Parser import Parser
from copy import deepcopy
from prettytable import PrettyTable
import pandas as pd

class Item():
    point_position = None
    non_terminal = None
    production = None
    final = False
    
    def __init__(self, position: int, terminal: str, production: str) -> None:
        self.point_position = position
        self.non_terminal = terminal
        self.production = production
        
        if self.production == 'ε' and position == 0:
            self.final = True
        elif position == len(production):
            self.final = True
           
        #Cambiar este raise por una excepción personalizada 
        if position < 0 or position > len(production):
            raise SyntaxError
    
    def __str__(self) -> str:
        return f"{self.non_terminal} -> {self.production[:self.point_position]}.{self.production[self.point_position:]} [{self.final}]"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Item):
            return False
        return (self.point_position == other.point_position and
                self.non_terminal == other.non_terminal and
                self.production == other.production and
                self.final == other.final)

    def __hash__(self) ->  hash:
        return hash((self.point_position, self.non_terminal, self.production, self.final))
    
    def verify_reduction(self) -> None:
        if self.production == 'ε' and self.point_position == 0:
            self.final = True
        elif self.point_position == len(self.production):
            self.final = True
            
        if self.point_position < 0 or self.point_position > len(self.production):
            raise SyntaxError
        
class BUParser(Parser):
    def __init__(self, gramatic):
        super().__init__(gramatic)
        
    def closure(self, closure: set()) -> set([]):
        added = True
        
        while added:
            added = False
            temp = set([])
            changed = len(closure)
            
            for item in closure:
                for number in range(len(item.production)):
                    if item.production[number] in self.grammar.Non_Terminals and number == item.point_position:
                        temp.update(set(Item(0,item.production[number],production) for production in self.grammar.Productions[item.production[number]]))
            
            closure.update(temp)
            if len(closure) > changed: added= True
            
        for item in closure:
            item.verify_reduction()
                                    
        return closure
    
    def consume(self,symbol: str, closure: set()) -> set():
        closure = deepcopy(closure)
        new_state = set()
        
        for item in closure:
            if not item.final and item.production[item.point_position] == symbol:
                item.point_position += 1
                item.verify_reduction()
                new_state.add(item)
        
        return new_state
    
    def lr0_automaton(self) -> set():
        automaton = set()
        visiteds = set()
        
        item = Item(0,"�",parser.grammar.Initial)
        closure = set()
        closure.add(item)
        closure = parser.closure(closure)
        automaton.add(frozenset(closure))
        
        while len(automaton - visiteds) > 0:
            actual_closure = (automaton - visiteds).pop()
            
            visiteds.add(actual_closure)
            symbols = set()
            
            new_state = actual_closure
            for item in new_state:
                for sm in item.production:
                    symbols.add(sm)
            
            for character in symbols:
                kernel = self.consume(character, new_state)
                clousure_temp = frozenset(self.closure(kernel))
                if len(clousure_temp) > 0:
                    automaton.add(clousure_temp)
        
        return automaton
    
    def print_automaton(self) -> None:
        automaton = self.lr0_automaton()
        table = PrettyTable()
        table.field_names = ["Numero","Item"]
        
        i = 1
        for state in automaton:
            for item in state:
                table.add_row([i,item])
            i += 1
        
        table.title = "Estados del Automata"
        table.hrules = True
        
        print(table)

    #Este metodo me permite saber que x / ϵ N U Σ
    def symbol_in_state(self, state: set()) -> set():
        symbols = set()

        for item in state:
            for character in item.production:
                if character not in symbols:
                    symbols.add(character)
        
        return symbols
    
    #Este metodo me permite saber cuales son las producciones del tipo A -> a.Bb con B e N
    def elements_of_the_type(self, items: set(), symbol: str) -> set():
        proces = set()
        for item in items:
            index = 0
            for character in item.production:
                if character == symbol and index == item.point_position:
                    new_item = deepcopy(item)
                    new_item.point_position += 1
                    new_item.verify_reduction()
                    proces.add(new_item)
                    break
                index += 1
        return proces
    

    def predictive_parsing_table(self) -> list:       
        initial = self.closure(set([Item(0,"�",parser.grammar.Initial)]))
        index = 0
        mapping = {}

        Action = {}
        Goto = {}

        states = set()
        states.add(frozenset(initial))
        visiteds = set()
        
        actual = initial
        Action[index] = { x:float('inf') for x in self.grammar.Terminals.union('$') }
        Goto[index] = {x:float('inf') for x in self.grammar.Non_Terminals}
        mapping[frozenset(initial)] = index

        while actual not in visiteds:
            visiteds.add(frozenset(actual))
            actual_tate = index

            for symbol in self.symbol_in_state(actual):
                new_state = self.closure(self.elements_of_the_type(actual,symbol))
                
                if new_state not in states and len(new_state) > 0:
                    index += 1
                    mapping[frozenset(new_state)] = index
                    Action[index] = { x:float('inf') for x in self.grammar.Terminals.union('$') }
                    Goto[index] = {x:float('inf') for x in self.grammar.Non_Terminals}
                if len(new_state) > 0:
                    states.add(frozenset(new_state))

                if symbol in self.grammar.Non_Terminals and len(new_state) > 0:
                    if Goto[mapping[frozenset(actual)]][symbol] == float('inf'):
                       Goto[mapping[frozenset(actual)]][symbol] = mapping[frozenset(new_state)]
                    else:
                        raise SyntaxError
                else:
                    pass



                

            for state in states:
                if state not in visiteds:
                    actual = state
                
        return Action, Goto



        return initial
                     
gramatica = Grammar()
gramatica.from_file(".\\Tests\\Gramatica16.txt")
parser = BUParser(gramatica)

#estado = parser.predictive_parsing_table()
#state = parser.closure(set([Item(0,"�",parser.grammar.Initial)]))
#print(parser.symbol_in_state(state))
tabla, goto = parser.predictive_parsing_table()
for i in tabla:
    print(i,tabla[i])

print()

for i in goto:
    print(i, goto[i])