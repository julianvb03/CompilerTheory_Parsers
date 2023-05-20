def closure(self, closure: Item) -> set([]):
        closure = set()
        closure.add(item)
        added = True
        
        while added:
            added = False
            temp = set([])
            changed = len(closure)
            
            for item in closure:
                for number in range(len(item.production)):
                    if item.production[number] in self.grammar.Non_Terminals and number == item.point_position:
                        temp.update(set(Item(0,item.production[number],production) for production in self.grammar.Productions[item.production[number]]))
                    else: break
            
            closure.update(temp)
            if len(closure) > changed: added= True
                        
        return closure