'''
Parser.py takes as reference the grammars that previously passed the conversion from .txt files to Grammar objects.
In addition, the converted grammar will get a pair of sets which are First and Follow.
'''
from Grammar import Grammar

class Parser:
    #Parser has a constructor, it contains: grammas, first and follow.
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar
        self.first = self.first_set()
        self.follow = self.follow_set()

    #Print first and follow
    def __str__(self) -> str:
        first_info = "First:\n"
        for key, value in self.first.items():
            first_info += f"{key} -> {', '.join(value)}\n"
        
        follow_info = "Follow:\n"
        for key, value in self.follow.items():
            follow_info += f"{key} -> {', '.join(value)}\n"
    
        return first_info + follow_info
    
    '''
    Rules to compute FIRST set:
    1. If x is a terminal, then FIRST (x) = { "x" }
    2. If x-> Є, is a production rule, then add Є to FIRST (x).
    3. If X->Y1 Y2 Y3….Yn is a production, FIRST (X) = FIRST (Y1).
    4. If FIRST (Y1) contains Є then FIRST (X) = { FIRST (Y1) - Є } U { FIRST (Y2) }
    5. If FIRST (Yi) contains Є for all i = 1 to n, then add Є to FIRST (X).
    '''
    #First
    def first_set(self) -> dict:
        First = {}  #Create dictionary.
        
        for symbol in self.grammar.Non_Terminals.union(self.grammar.Terminals):
            if symbol in self.grammar.Terminals:
                First[symbol] = {symbol}    #Adding only terminal.
            else:       
                First[symbol] = set([])     #Creating a terminals-set.
        
        added = True   
        while added:    #Adding First of non-terminals.
            added = False
            for nt in self.grammar.Non_Terminals:
                for production in self.grammar.Productions[nt]: #Touring production on a non-terminal.
                    for i in range(len(production)):
                        first_sub_i = [First[j] for j in production[:i]]
                        if i == 0:  #Empty.
                            first_sub_i.append({'ε'})
                        if 'ε' in set.intersection(*first_sub_i):
                            changed = len(First[nt])
                            First[nt].update(First[production[i]]-{'ε'}) #Updatting First withput epsilon.
                            if len(First[nt]) > changed: added = True 
                    if 'ε' in set.intersection(*[First[j] for j in production]):    #Verify all sets have epsilon.
                        changed = len(First[nt])
                        First[nt].add('ε')
                        if len(First[nt]) > changed: added = True 
                        
        
        eliminate_TF = self.grammar.Terminals
        for key in eliminate_TF:
            del First[key]                 
             
        return First
    
    #Select First symbols of a word.
    def first_of_word(self, word: str) -> set([]):
        First = self.first_set()
        for t in self.grammar.Terminals:
            First[t] = {t}
            
        First_word = set([])    #Empty set.
        for i in range(len(word)):
            first_sub_i = [First[j] for j in word[:i]]
            if i == 0:  #Empty word.
                first_sub_i.append({'ε'})
            if 'ε' in set.intersection(*first_sub_i):
                First_word.update(First[word[i]]-{'ε'}) #Updatting First_word without epsilon.
        if 'ε' in set.intersection(*[First[j] for j in word]):  #Verify all sets have epsilon.
            First_word.add('ε')
            
        return First_word
    
    #No soporta recursividad izquierda
    def first_recursive(self) -> dict:
        First = {}
        for nt in self.grammar.Non_Terminals:
            First[nt] = set([])
            for production in self.grammar.Productions[nt]:
                first = set([])
                if len(production) == 1:
                    First[nt].update(self.first_symbol_recursive(first,production))
                else:
                    First[nt].update(self.first_of_word_recursive(first,production))
        return First
    
    def first_symbol_recursive(self, First: set(), expresion: str) -> set():
        if not expresion[0] in self.grammar.Non_Terminals and not expresion[0] in self.grammar.Terminals:
            raise SyntaxError

        if expresion[0] in self.grammar.Terminals:
            return set([expresion[0]])
        
        if expresion[0] in self.grammar.Non_Terminals:
            if self.grammar.epsilon_Transition(expresion[0]):
                self.first_of_word_recursive(First, expresion)        
            else:
                for production in self.grammar.Productions[expresion[0]]:
                    First.update(self.first_symbol_recursive(First, production))

            return First
        return First
                   
    def first_of_word_recursive(self, First: set(), expresion: str) -> set():
        if expresion[0] in self.grammar.Terminals:
            First.add(expresion[0])
            return First
        tokens = list(expresion)
        i = 0
        for token in tokens:
            i += 1
            if token in self.grammar.Terminals:
                First.add(token)
                break
            if not self.grammar.epsilon_Transition(token):
                First.update(self.first_symbol_recursive(First, token))
                break
            for production in self.grammar.Productions[token] - {'ε'}:
                if len(production) == 1:
                    First.update(self.first_symbol_recursive(First, production))
                else:
                    First.update(self.first_of_word_recursive(First, production))
            if i == len(tokens) and token in self.grammar.Non_Terminals and self.grammar.epsilon_Transition(token):
                First.add('ε')
        return First
    
    '''
    Rules to compute FOLLOW set:
    1) FOLLOW(S) = {$} where S is the starting Non-Terminal
    2) If A -> pBq is a production, where p, B and q are any grammar symbols, then everything in FIRST(q) except ε is in FOLLOW(B).
    3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
    4) If A->pBq is a production and FIRST(q) contains ε, then FOLLOW(B) contains {FIRST(q) - ε} U FOLLOW(A)
    '''

    def follow_set(self) -> dict:
        Follow = {} #Create dictionary.
        added = True
        for nt in self.grammar.Non_Terminals:
            Follow[nt] = set([])    #Empty set for all non-terminals.
        while added:
            added = False
            if '$' not in Follow[self.grammar.Initial]: 
                Follow[self.grammar.Initial].add('$')   #Add '$' to non-terminal's initial.
                added = True
            for nt in self.grammar.Non_Terminals:
                for production in self.grammar.Productions[nt]:
                    i = 0
                    for token in production:
                        i += 1
                        #Rules to compute FOLLOW set.
                        if i == len(production) and token in self.grammar.Non_Terminals:
                            follow_len = len(Follow[token])
                            Follow[token].update(Follow[nt])
                            if len(Follow[token]) > follow_len: added = True
                        if token in self.grammar.Non_Terminals:
                            if production[i:] == "":
                                Follow[token].update(Follow[nt])
                                Follow[token].update(Follow[nt])
                                if len(Follow[token]) > follow_len: added = True
                                continue
                            first_B = self.first_of_word(production[i:])
                            if not 'ε' in first_B:
                                follow_len = len(Follow[token])
                                Follow[token].update(first_B)
                                if len(Follow[token]) > follow_len: added = True
                            else:
                                follow_len = len(Follow[token])
                                Follow[token].update(first_B-{'ε'}) 
                                Follow[token].update(Follow[nt])
                                if len(Follow[token]) > follow_len: added = True
        return Follow