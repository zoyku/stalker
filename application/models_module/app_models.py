class BaseResponse:
    def __init__(self, is_okay=True, message='', response_code=200):
        self.is_okay = is_okay
        self.message = message
        self.response_code = response_code
