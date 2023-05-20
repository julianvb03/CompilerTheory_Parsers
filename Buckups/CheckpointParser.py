from Grammar import Grammar

class Parser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar
    
    
    '''
    Rules to compute FIRST set:
    1. If x is a terminal, then FIRST (x) = { "x" }
    2. If x-> Є, is a production rule, then add Є to FIRST (x).
    3. If X->Y1 Y2 Y3….Yn is a production, FIRST (X) = FIRST (Y1)
    4. If FIRST (Y1) contains Є then FIRST (X) = { FIRST (Y1) - Є } U { FIRST (Y2) }
    5. If FIRST (Yi) contains Є for all i = 1 to n, then add Є to FIRST (X).
    '''
    
    def fouth_rule_first(self, symbol: str) -> bool:
        if symbol in self.grammar.Non_Terminals and self.grammar.epsilon_Transition(symbol):
            return True
        return False
    
    def first_set(self, First, expresion, nt, visiteds = None) -> dict:
        if visiteds == None:
            visiteds = set()
        if not expresion[0] in self.grammar.Non_Terminals and not expresion[0] in self.grammar.Terminals:
            raise SyntaxError
        #Testear este funcionamiento más tarde
        if nt in visiteds:
            return First
        #1° regla del FIRST
        if expresion[0] in self.grammar.Terminals:
            First[nt].add(expresion[0])
            return First
        #3° regla del FIRST
        if expresion[0] in self.grammar.Non_Terminals and not self.grammar.epsilon_Transition(expresion[0]):
        #if expresion[0] in self.grammar.Non_Terminals:
            for production in self.grammar.Productions[expresion[0]]:
                First[nt].update(self.first_set(First, production, expresion[0])[expresion[0]], visiteds)
            visiteds.add(expresion[0])
            return First
        #4° regla del FIRST
        if self.fouth_rule_first(expresion[0]):
            first_word = set([])
            First[nt].update(self.first_of_word(First, first_word,expresion,nt,visiteds))
            return First
        return First
        
    def first_of_word(self, First, first_word, expresion, nt, visiteds = None):
        if len(expresion) == 1:
            first_word.update(self.first_set(First, expresion[0], nt, visiteds)[expresion[0]])
            return first_word
        if len(expresion) > 1:
            if expresion[0] in self.grammar.Terminals:
                if expresion[0] in visiteds:
                    first_word.update(First[expresion[0]])
                else:
                    for production in self.grammar.Productions[expresion[0]]:
                        first_word.update(self.first_set(First, production, expresion[0], visiteds)[expresion[0]])
                first_word.add(expresion[1])
                return first_word
            else:
                first_word.update(self.first_set(First, expresion[0], expresion[0], visiteds)[expresion[0]].union(self.first_set(First, expresion[1:], expresion[1], visiteds)[expresion[1]]))
                return first_word
    
    def first_thirdR(self, First, first_word, expresion, nt, visiteds):
        
                
        return First
            
gramatica = Grammar()
gramatica.from_file("Gramatica.txt")
parser = Parser(gramatica)
first = {}
first['B'] = set([])
first['A'] = set([])
first['E'] = set([])
first['C'] = set([])
'''
for production in gramatica.Productions['B']:
    parser.first_set(first,production,'B')
print(first)'''

print(parser.first_set(first,'EDa','B'))