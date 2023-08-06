

class ZSetError(Exception):
    def __init__(self):
        Exception.__init__(self, "Operation between ZnInt of different Z set")


class ZVarError(Exception):
    def __init__(self):
        Exception.__init__(self, "Operation between ZnInt of different variables outside products")


class ParseError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class ResolveError(Exception):
    def __init__(self):
        Exception.__init__(self, "Could not resolve equation")
