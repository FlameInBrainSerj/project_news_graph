class ParseError(Exception):
    """
    ParseError class.
    """

    def __init__(self, message: str = "The page was not parsed"):
        """
        ParseError init.

        :param message: message when error is arisen
        :type message: str
        """
        self.message = message
        super().__init__(self.message)
