from Parser import Parser
from copy import deepcopy
from Grammar import Grammar
from collections import deque
import Exceptions

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
           
        if position < 0 or position > len(production):
            raise Exceptions.Point_Invalid_Position("Error en la creación de un Item")
    
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
            raise Exceptions.Point_Invalid_Position("Error en la creación de un Item")
        
class BUParser(Parser):
    def __init__(self, gramatic):
        super().__init__(gramatic)
        #self.action, self.goto, self.ppt = self.predictive_parsing_table()
        
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

    def symbol_in_state(self, state: set()) -> set():
        symbols = set()

        for item in state:
            for character in item.production:
                if character not in symbols:
                    symbols.add(character)
        
        return symbols
    
    def elements_of_the_type(self, items: set(), symbol: str) -> set():
        proces = set()
        for item in items:
            index = 0
            for character in item.production:
                if character == symbol and index == item.point_position and character != 'ε':
                    new_item = deepcopy(item)
                    new_item.point_position += 1
                    new_item.verify_reduction()
                    proces.add(new_item)
                    break
                index += 1
        return proces
    
    def shift_condition(self, state: set(), nt: str) -> bool:
        exist = False
        for item in state:
            index = 0
            for character in item.production:
                if character == nt and index == item.point_position:
                    exist = True
        return True
    
    def reduce_condition(self, state: set()) -> set():
        items = set()

        for item in state:
            if item.final:
                items.add(item)

        return items    

    def predictive_parsing_table(self) -> set():       
        initial = self.closure(set([Item(0,"�",self.grammar.Initial)]))
        index = 0
        mapping = {}

        Action = {}
        Goto = {}

        states = set()
        states.add(frozenset(initial))
        visiteds = set()
        
        actual = initial
        Action[index] = { x:float('inf') for x in self.grammar.Terminals.union('$') - {'ε'} }
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
                    Action[index] = { x:float('inf') for x in self.grammar.Terminals.union('$') - {'ε'}}
                    Goto[index] = {x:float('inf') for x in self.grammar.Non_Terminals}
                if len(new_state) > 0:
                    states.add(frozenset(new_state))
                 
                if symbol in self.grammar.Non_Terminals and len(new_state) > 0:
                    if Goto[mapping[frozenset(actual)]][symbol] == float('inf'):
                       Goto[mapping[frozenset(actual)]][symbol] = mapping[frozenset(new_state)]
                    else:
                        raise Exceptions.Not_LRSGramar(f'La gramatica tiene un erro en la creación de la tabla Goto en el estado {mapping[frozenset(actual)]} para el estado {mapping[frozenset(new_state)]}')
                else:
                    if symbol in self.grammar.Terminals.union("$") and self.shift_condition(actual,symbol) and len(new_state) > 0:
                        if Action[mapping[frozenset(actual)]][symbol] == float('inf'):
                            Action[mapping[frozenset(actual)]][symbol] = ('s',mapping[frozenset(new_state)])
                        else:
                            raise Exceptions.Not_LRSGramar(f'La gramatica tiene un erro en la creación de la tabla Action en el estado {mapping[frozenset(actual)]} para una acción del tipo shift')
                    
            for state in states:
                if state not in visiteds:
                    actual = state

        for state in states:
            set_reduction = self.reduce_condition(state)
            if len(set_reduction) > 0 and len(state) > 0:
                for item in set_reduction:
                    if item.non_terminal == "�" and item.production == self.grammar.Initial:
                          Action[mapping[frozenset(state)]]['$'] = ('a',0)
                    else:
                        follow = self.follow[item.non_terminal]
                        for terminal in follow:
                            if Action[mapping[frozenset(state)]][terminal] == float('inf'):
                                Action[mapping[frozenset(state)]][terminal] = ('r',(item.non_terminal,item.production))
                            else:
                                raise Exceptions.Not_LRSGramar(f'La gramatica tiene un erro en la creación de la tabla Action en el estado {mapping[frozenset(state)]} para una acción del tipo reduce')
                    
        return Action, Goto, mapping

    def analyce_word(self, word: str) -> bool:
        for i in word:
            if i not in self.grammar.Non_Terminals and i not in self.grammar.Terminals:
                raise Exceptions.Non_Pertenecient_Symbol("Un simbolo de la entrada no pertenece a Σ")
        
        stack = deque()
        stack.append(0)
        word += '$'
        i = 0
        while True:
            if(self.action[stack[-1]][word[i]][0] == 's'):
                element = self.action[stack[-1]][word[i]][1]
                stack.append(element)
                i += 1
            elif(self.action[stack[-1]][word[i]][0] == 'r'):
                reduction_tuple = self.action[stack[-1]][word[i]]
                non_terminal_rt = reduction_tuple[1][0]
                production_rt = reduction_tuple[1][1]
                if production_rt != 'ε':
                    j = len(production_rt)
                    while j != 0:
                        stack.pop()
                        j -= 1
                stack.append(self.goto[stack[-1]][non_terminal_rt])
            elif(self.action[stack[-1]][word[i]][0] == 'a'):
                return True
            else:
                print(type(self.action[stack[-1]][word[i]]),self.action[stack[-1]][word[i]], stack, i)
                return False
    
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
    


gramatica = Grammar()
gramatica.from_file("C:\\Users\\valen\\OneDrive\\Escritorio\\Estudio\\Analizadores Sintacticos LFC\\Tests\\Gramatica21.txt")
parser = BUParser(gramatica)

table = parser.lr0_automaton()
i = 0
for estate in table:
    for item in estate:
        print(f'En el estado {i} el item {item}')
    i+=1
    print()