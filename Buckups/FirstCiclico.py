def si():
    First = {}
        
        for symbol in self.grammar.Non_Terminals.union(self.grammar.Terminals):
            if symbol in self.grammar.Terminals:
                First[symbol] = {symbol}
            else:
                First[symbol] = set([])
                
        for nt in self.grammar.Non_Terminals:
            for production in self.grammar.Productions[nt]:
                if production[0] in self.grammar.Terminals:
                    First[nt].add(production[0])
        
        for nt in self.grammar.Non_Terminals:
            for production in self.grammar.Productions[nt]:
                if production[0] in self.grammar.Non_Terminals and not self.grammar.epsilon_Transition(production[0]):
                    First[nt].update(First[production[0]])
        
        added = True   
        while added:
            added = False
            for nt in self.grammar.Non_Terminals:
                for production in self.grammar.Productions[nt]:
                    for i in range(len(production)):
                        first_sub_i = [First[j] for j in production[:i+1]]
                        if 'ε' in set.intersection(*first_sub_i):
                            First[nt].update(First[production[i]])