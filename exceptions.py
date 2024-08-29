class GetLocationError(Exception):
    def __init__(self, message: str = """PROGRAM CANT GET CURRENT GPS""") -> None:
        super().__init__(message)

class ApiServerError(Exception):
    def __init__(self, message: str = """PROGRAM CANT GET CURRENT WEATHER""") -> None:
        super().__init__(message)