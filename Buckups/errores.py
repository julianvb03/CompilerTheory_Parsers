elif len(tokens) > 1 and tokens[0] in self.grammar.Non_Terminals and tokens[1] in self.grammar.Non_Terminals:
            return self.first_aux(tokens[0], First).union(self.first_aux(tokens[1:], First))
        return {}