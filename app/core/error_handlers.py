class AppError(Exception):
    def __init__(self, code, message="Internal Server Error"):
        self.code = code
        self.message = message
        self.success = False
        self.data = None
