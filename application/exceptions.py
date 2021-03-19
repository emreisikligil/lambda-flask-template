class ApplicationException(Exception):

    def __init__(self, msg: str = None, code: int = 500):
        self.msg = msg

