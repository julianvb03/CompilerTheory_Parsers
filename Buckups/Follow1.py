def follow_set(self) -> dict:
        Follow = {}
        added = True
        for nt in self.grammar.Non_Terminals:
            Follow[nt] = set([])
        while added:
            added = False
            if '$' not in Follow[self.grammar.Initial]: 
                Follow[self.grammar.Initial].add('$')
                added = True
            for nt in self.grammar.Non_Terminals:
                for production in self.grammar.Productions[nt]:
                    i = 0
                    for token in production:
                        i += 1
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
                            first_B = self.first_of_word(set([]), production[i:])
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