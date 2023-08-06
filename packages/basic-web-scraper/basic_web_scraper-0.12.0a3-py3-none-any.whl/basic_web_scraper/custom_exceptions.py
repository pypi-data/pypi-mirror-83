

class GeckoNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParameterConflictError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BadScrollPositionException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
