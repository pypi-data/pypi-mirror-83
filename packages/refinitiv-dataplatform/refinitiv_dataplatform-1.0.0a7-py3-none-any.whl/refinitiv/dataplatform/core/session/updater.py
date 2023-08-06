import abc
import asyncio


class Updater(abc.ABC):
    def __init__(self, delay):
        self.delay = delay or 1
        self._stopped = False
        self._event = asyncio.Event()

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    async def start(self):
        self._event.clear()
        self._stopped = False
        while not self._stopped:
            try:
                await asyncio.wait_for(self._event.wait(), timeout=self.delay)
            except (asyncio.TimeoutError, RuntimeError):
                pass

            if not self._stopped:
                try:
                    await self._do_update()
                except Exception as e:
                    self.stop()
                    raise e

    def stop(self):
        self._stopped = True
        self._event.set()

    def dispose(self):
        self._do_dispose()

        if not self._stopped:
            self.stop()

        self._event = None

    @abc.abstractmethod
    async def _do_update(self):
        # for override
        pass

    @abc.abstractmethod
    def _do_dispose(self):
        # for override
        pass
