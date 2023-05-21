from Parser import Parser
from Grammar import Grammar
from collections import deque
import Exceptions
import pandas as pd


class TDParser(Parser):
    #TDParser has a constructor, it contains same items that Grammar.
    def __init__(self, gramatic):
        super().__init__(gramatic)

    def ll1_verification(self) -> bool:
        for nt in self.grammar.Non_Terminals:
            for production in self.grammar.Productions[nt]:
                first_1 = self.first_of_word(production)
                epsilon_counter = 0
                if 'ε' in first_1:
                    epsilon_counter += 1
                for production2 in self.grammar.Productions[nt]:
                    if production == production2:
                        continue
                    if len(first_1.intersection(self.first_of_word(production2))) > 0:
                        return False
                    if 'ε' in self.first_of_word(production2):
                        epsilon_counter += 1
                    if 'ε' in first_1 and len(self.first_of_word(production2).intersection(self.follow[nt])) > 0:
                        return False
                    elif 'ε' in self.first_of_word(production2) and len(first_1.intersection(self.follow[nt])) > 0:
                        return False
                if epsilon_counter > 1:
                    return False
        return True
        
    def predictive_parsing_table(self) -> list:
        non_terminals_len = [0] * len(self.grammar.Non_Terminals)
        terminals = [i for i in self.grammar.Non_Terminals]
        data = {}
        
        for tm in (self.grammar.Terminals - {'ε'}).union('$') :
            data[tm] = non_terminals_len
        
        predictive_pt = pd.DataFrame(data, index=terminals)
        
        for nt in self.grammar.Non_Terminals:
            for production in self.grammar.Productions[nt]:
                for terminal in self.first_of_word(production):
                    if terminal == 'ε':
                        for terminalB in self.follow[nt]:
                            if predictive_pt.loc[nt,terminalB] != 0: raise Exceptions.Not_LL1Gramar("La gramatica no es LL(1)")
                            else: predictive_pt.loc[nt,terminalB] = production
                        continue  
                    if predictive_pt.loc[nt,terminal] != 0: raise Exceptions.Not_LL1Gramar("La gramatica no es LL(1)")
                    else: predictive_pt.loc[nt,terminal] = production
        return predictive_pt    
    
    def analixer_word(self, word: str):
        for i in word:
            if i not in self.grammar.Non_Terminals and i not in self.grammar.Terminals:
                raise Exceptions.Non_Pertenecient_Symbol("Un simbolo de la entrada no pertenece a Σ")

        predictive_PT = self.predictive_parsing_table()
        
        stack = deque()
        stack.append('$')
        stack.append(self.grammar.Initial)
        
        word += '$'
        i = 0
        while stack[-1] != '$':
            if stack[-1] == word[i]:
                stack.pop()
                i += 1
            elif stack[-1] in self.grammar.Terminals:
                return False
            elif predictive_PT.loc[stack[-1],word[i]] == 0:
                return False
            else:
                rule = predictive_PT.loc[stack.pop(),word[i]]
                for j in range(len(rule)) :
                    if rule[-(j+1)] == 'ε': continue
                    stack.append(rule[-(j+1)])
        
        if word[i] != "$": return False

        return True