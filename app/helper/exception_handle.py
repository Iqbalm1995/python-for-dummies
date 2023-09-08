class ExceptionHandle(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)  # Initialize the base Exception with the message
        self.message = message
        self.status_code = status_code