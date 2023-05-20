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
    
    def first_set(self, First, expresion, nt, visiteds = 0) -> dict:
        if visiteds == 0:
            visiteds = set()
        if  not expresion[0] in self.grammar.Terminals and not expresion[0] in self.grammar.Non_Terminals:
            raise SyntaxError
        if expresion[0] in self.grammar.Terminals:
            First[nt].add(expresion[0])
            return First
        if expresion[0] in self.grammar.Non_Terminals and not self.grammar.epsilon_Transition(expresion[0]):
            for production in self.grammar.Productions[expresion[0]]:
                self.first_set(First, production, nt)
        else:
            '''for production in self.grammar.Productions[expresion[0]]:
                self.first_thirdR(First, production, nt)'''
            self.first_thirdR(First, expresion, nt)
        return First            
    
    def first_thirdR(self, First, expresion, nt):
                
        return First
            
gramatica = Grammar()
gramatica.from_file("Gramatica.txt")
parser = Parser(gramatica)
first = {}
first['B'] = set([])
first['D'] = set([])
print(parser.first_set(first,"D","D"))