def predictive_parsing_table(self) -> list:       
        initial = self.closure(set([Item(0,"�",parser.grammar.Initial)]))
        index = 0
        mapping = {}
        mapping[frozenset(initial)] = index

        states = set()
        states.add(frozenset(initial))
        visiteds = set()
        
        actual = None
        for state in states:
            if state not in visiteds:
                actual = state

        while actual not in visiteds:
            visiteds.add(frozenset(actual))
            for symbol in self.symbol_in_state(actual):
                new_state = self.closure(self.elements_of_the_type(actual,symbol))
                states.add(frozenset(new_state))

                if new_state not in states:
                    index += 1
                    mapping[frozenset(new_state)] = index
                
        return mapping



        return initial