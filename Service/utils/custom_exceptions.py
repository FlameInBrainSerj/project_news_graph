class ParseError(Exception):
    def __init__(self, message="The page was not parsed"):
        self.message = message
        super().__init__(self.message)
