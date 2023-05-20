def lr0_automaton(self):
        automaton = set()
        visiteds = set()
        
        item = Item(0,"�",parser.grammar.Initial)
        closure = set()
        closure.add(item)
        closure = parser.closure(closure)
        automaton.add(frozenset(closure))
        
        while len(automaton - visiteds) > 0:
            print(len(automaton - visiteds))
            actual_closure = (automaton - visiteds).pop()
            
            visiteds.add(actual_closure)
            symbols = set()
            
            new_state = actual_closure
            for item in new_state:
                for sm in item.production:
                    symbols.add(sm)
            
            for character in symbols:
                kernel = self.consume(character, new_state)
                automaton.add(frozenset(self.closure(kernel)))
        
        return automaton