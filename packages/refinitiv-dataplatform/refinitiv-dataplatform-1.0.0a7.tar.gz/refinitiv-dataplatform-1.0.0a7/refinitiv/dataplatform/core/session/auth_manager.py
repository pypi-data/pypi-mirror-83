import asyncio

from .session import Session
from refinitiv.dataplatform.core.log_reporter import LogReporter
from .access_token_updater import AccessTokenUpdater
from .refresh_token_updater import RefreshTokenUpdater

from .event import UpdateEvent

State = Session.State
SessionEvent = Session.EventCode
SessionStatus = Session.EventCode


def handle_exception(task):
    exception = None

    try:
        exception = task.exception()
    except asyncio.CancelledError:
        pass

    if exception:
        raise exception


class AuthManager(LogReporter):
    """
    Methods
    -------
    is_closed()
        The method returns True if closed, otherwise False

    is_authorized()
        The method returns True if authorized, otherwise False. If instance destroyed or closed always returns False

    authorize()
        The method starts process authorization

    close()
        The method stops refresh token updater and access token updater

    dispose()
        The method destroy an instance

    """

    def __init__(self, session, auto_reconnect):
        LogReporter.__init__(self, logger=session)

        self._session = session
        self._auto_reconnect = auto_reconnect

        self._refresh_token_updater = None
        self._access_token_updater = None

        self._authorized = None
        self._closed = False

    def is_closed(self):
        """

        Returns
        -------
        bool
            True if closed, otherwise False
        """
        return self._closed is True

    def is_authorized(self):
        """

        Returns
        -------
        bool
            True if authorized, otherwise False
        """
        if self.is_closed():
            return False

        return bool(self._authorized and self._authorized.result())

    async def authorize(self):
        """
        The method starts process authorization

        Returns
        -------
        bool
            True if authorized, otherwise False
        """
        if self.is_authorized() is True:
            return True

        self.debug("AuthManager: start authorize")

        task = asyncio.create_task(self._do_authorize())
        result = await task

        self.debug(f"AuthManager: end authorize, result {result}")

        return result

    async def _do_authorize(self):
        self.debug("AuthManager: connecting")

        self._closed = False
        self._authorized = asyncio.Future()

        if self._access_token_updater is None:
            self._access_token_updater = AccessTokenUpdater(self._session, 1, self._access_token_update_handler)

        self.debug(f"AuthManager: Access token will be requested in {self._access_token_updater.delay} seconds")
        await asyncio.create_task(self._access_token_updater.start())

        await self._authorized

        if self._authorized.result():
            delay = self._session._token_expires_in_secs

            if self._refresh_token_updater is None:
                self._refresh_token_updater = RefreshTokenUpdater(self._session, 1, self._refresh_token_update_handler)

            self._refresh_token_updater.delay = delay
            self.debug(f"AuthManager: Refresh token will be requested in {self._refresh_token_updater.delay} seconds")
            asyncio.create_task(self._refresh_token_updater.start()).add_done_callback(handle_exception)

        self.debug("AuthManager: connected")
        return self._authorized.result()

    def close(self):
        """
        The method stops refresh token updater and access token updater

        Returns
        -------
        None
        """
        self.debug("AuthManager: close")
        if self.is_closed():
            return

        if self._authorized is not None:
            not self._authorized.done() and self._authorized.set_result(False)

        self._access_token_updater and self._access_token_updater.stop()
        self._refresh_token_updater and self._refresh_token_updater.stop()
        self._closed = True

    def _access_token_update_handler(self, event, message):
        self.debug(f"AuthManager: Access token handler, event: {event}, message: {message}")

        if event is UpdateEvent.ACCESS_TOKEN_SUCCESS:
            self._session._status = SessionStatus.SessionAuthenticationSuccess

            self._access_token_updater.stop()
            self._authorized.set_result(True)
            self._session._on_event(SessionEvent.SessionAuthenticationSuccess, message)

        elif event is UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED:
            self._session._last_event_code = event
            self._session._last_event_message = message
            self._session._status = SessionStatus.SessionAuthenticationFailed

            self._access_token_updater.stop()
            self._authorized.set_result(False)
            self._session._on_event(SessionEvent.SessionAuthenticationFailed, message)
            self.close()
            self._close_session()

        elif event is UpdateEvent.ACCESS_TOKEN_FAILED:
            self._session._last_event_code = event
            self._session._last_event_message = message
            self._session._status = SessionStatus.SessionAuthenticationFailed

            if not self._auto_reconnect:
                self._access_token_updater.stop()
                self._authorized.set_result(False)

            self._session._on_event(SessionEvent.SessionAuthenticationFailed, message)

            if self._auto_reconnect:
                self.debug("AuthManager: reconnecting")
                self._session._status = SessionStatus.SessionReconnecting
                self._session._on_event(SessionEvent.SessionReconnecting, "Session is reconnecting")

            else:
                self.close()
                self._close_session()

    def _refresh_token_update_handler(self, event, message):
        self.debug(f"AuthManager: Refresh token handler, event: {event}, message: {message}")

        if event is UpdateEvent.REFRESH_TOKEN_SUCCESS:
            self._session._status = SessionStatus.SessionAuthenticationSuccess
            self._session._on_event(SessionEvent.SessionAuthenticationSuccess, message)

        elif event is UpdateEvent.REFRESH_TOKEN_BAD:
            self._session._last_event_code = event
            self._session._last_event_message = message
            self._session._status = SessionStatus.SessionAuthenticationFailed
            self._session._on_event(SessionEvent.SessionAuthenticationFailed, message)
            self.close()
            self._close_session()

        elif event is UpdateEvent.REFRESH_TOKEN_FAILED:
            self._session._last_event_code = event
            self._session._last_event_message = message
            self._session._status = SessionStatus.SessionAuthenticationFailed

            self._session._on_event(SessionEvent.SessionAuthenticationFailed, message)

            if self._auto_reconnect:
                self.debug("AuthManager: Trying to get Refresh token again")
                self._session._status = SessionStatus.SessionReconnecting
                self._session._on_event(SessionEvent.SessionReconnecting, "Trying to get Refresh token again")

            else:
                self.close()
                self._close_session()

        elif event is UpdateEvent.REFRESH_TOKEN_EXPIRED:
            self._session._last_event_code = event
            self._session._last_event_message = message
            self._session._status = SessionStatus.SessionAuthenticationFailed

            self._session._on_event(SessionEvent.SessionAuthenticationFailed, message)

            if self._auto_reconnect:
                self.debug("AuthManager: reconnecting")
                self._session._status = SessionStatus.SessionReconnecting
                self._session._on_event(SessionEvent.SessionReconnecting, "Session is reconnecting")
                self.close()
                asyncio.create_task(self._do_authorize())

            else:
                self.close()
                self._close_session()

    def _close_session(self):
        self._session._on_state(State.Closed, "Session is closed.")
        self._session.close()

    def dispose(self):
        """
        The method destroy an instance

        Returns
        -------
        None
        """
        self.close()
        self._access_token_updater and self._access_token_updater.dispose()
        self._access_token_updater = None
        self._refresh_token_updater and self._refresh_token_updater.dispose()
        self._refresh_token_updater = None
        self._authorized = None
        self._session = None
