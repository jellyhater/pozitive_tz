class Model:

    def __init__(self, *args):
        pass

    def predict(self, **kwargs):
        return kwargs.get("REQUEST_SIZE")