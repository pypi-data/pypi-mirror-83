class State(object):

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()
        self._state = None

    @property
    def state(self):
        return self._state
