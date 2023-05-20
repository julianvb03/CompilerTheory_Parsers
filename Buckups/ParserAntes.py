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
    def first_set(self) -> set:
        First = {}
        for nt in self.grammar.Non_Terminals:
            if nt == 'S': continue
            First[nt] = set()
            #2° rule of FIRST set
            if self.grammar.epsilon_Transition(nt): First[nt].add('ϵ')
            for production in self.grammar.Productions[nt] - {'ϵ'}:
                First[nt].update(self.first_aux(production,First[nt]))
        return First
                
    def first_aux(self, expresion: str, First: set()):  
        tokens = list(expresion)
        #1° rule of FIRST set
        if tokens[0] in self.grammar.Terminals:
            return First.add(tokens[0])
        #3° rule of FIRST set
        if tokens[0] in self.grammar.Non_Terminals and not self.grammar.epsilon_Transition(tokens[0]):
            return self.first_third_rule(tokens[0], First)
        #4°rule of FIRST set
        #if tokens[0] in self.grammar.Non_Terminals and self.grammar.epsilon_Transition(tokens[0]):
        return First
            
            
            
    def first_third_rule(self, symbol: str, First: set()) -> set:
        if symbol in self.grammar.Terminals:
            return First.add(symbol)
        else:
            for production in self.grammar.Productions[symbol] - {'ϵ'}:
                tokens = list(production)
                if tokens[0] in self.grammar.Terminals:
                    return First.add(tokens[0])
                else:
                    return self.first_third_rule(tokens[0], First)
                    
    def first_fourth_rule(self, tokens: set(), First: set()) -> set:
        pass              
        
        
    '''
    Rules to compute FOLLOW set:
    1) FOLLOW(S) = {$} where S is the starting Non-Terminal
    2) If A -> pBq is a production, where p, B and q are any grammar symbols, then everything in FIRST(q) except ε is in FOLLOW(B).
    3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
    4) If A->pBq is a production and FIRST(q) contains ε, then FOLLOW(B) contains {FIRST(q) - ε} U FOLLOW(A)²
    '''

gramatica = Grammar()
gramatica.from_file("Gramatica.txt")
parser = Parser(gramatica)
print(parser.first_set())
