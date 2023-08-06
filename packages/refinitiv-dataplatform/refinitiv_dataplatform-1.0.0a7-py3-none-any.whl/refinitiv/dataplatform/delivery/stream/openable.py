import abc

from .state import State


class Openable(State, abc.ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = kwargs.get("loop")
        self._next_state = None
        self._prev_state = None
        self._with_updates = None

    def is_open(self):
        from .stream import StreamState
        return self.state is StreamState.Open

    def is_pause(self):
        from .stream import StreamState
        return self.state is StreamState.Pause

    def open(self, with_updates=True):
        return self._loop.run_until_complete(self.open_async(with_updates=with_updates))

    async def open_async(self, with_updates=True):
        from .stream import StreamState

        if self.state in [StreamState.Pending, StreamState.Open]:
            # it is already opened or is opening
            return self.state

        if self.is_pause():
            self._next_state = StreamState.Open
            self._with_updates = with_updates
            return self.state

        self._state = StreamState.Pending
        is_success = await self._do_open_async(with_updates=with_updates)

        if is_success:
            self._state = StreamState.Open
        else:
            self._state = StreamState.Closed

        return self.state

    @abc.abstractmethod
    async def _do_open_async(self, with_updates=True):
        # for override
        pass

    def close(self):
        return self._loop.run_until_complete(self.close_async())

    async def close_async(self):
        from .stream import StreamState

        if self.state is StreamState.Closed:
            return self.state

        await self._do_close_async()
        self._state = StreamState.Closed
        return self.state

    @abc.abstractmethod
    async def _do_close_async(self):
        # for override
        pass

    def pause(self):
        if self.is_pause():
            return self.state

        self._set_pause()
        self._do_pause()

        return self.state

    def _set_pause(self):
        from .stream import StreamState

        self._prev_state = self.state
        self._state = StreamState.Pause

    @abc.abstractmethod
    def _do_pause(self):
        # for override
        pass

    def resume(self):
        from .stream import StreamState

        if not self.is_pause():
            return self.state

        self._set_resume()

        if self._next_state is StreamState.Open:
            self.open(self._with_updates)

        self._do_resume()

        return self.state

    def _set_resume(self):
        self._state = self._prev_state

    @abc.abstractmethod
    def _do_resume(self):
        # for override
        pass
