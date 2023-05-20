class Not_LL1Gramar(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Not_LRSGramar(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Point_Invalid_Position(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Non_Pertenecient_Symbol(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
