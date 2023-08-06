import time
from json import JSONDecodeError

import requests_async as requests

from refinitiv.dataplatform.core.log_reporter import LogReporter
from refinitiv.dataplatform.errors import RDPError
from .session import Session
from .updater import Updater
from .event import UpdateEvent

codes = requests.codes


class RefreshTokenUpdater(Updater, LogReporter):

    def __init__(self, session, delay, callback):
        Updater.__init__(self, delay=delay)
        LogReporter.__init__(self, logger=session)

        self._session = session
        self._callback = callback

    @Updater.delay.setter
    def delay(self, value):
        Updater.delay.fset(self, self.calculate_delay(value))

    def calculate_delay(self, value):
        new_value = value // 2

        if new_value <= 0:
            new_value = 1

        return new_value

    async def _do_update(self):
        cur_time = time.time()

        if self._session._token_expires_at <= cur_time:
            event = UpdateEvent.REFRESH_TOKEN_EXPIRED
            message = "Time expired for the refresh token update"
            self.debug(message)
            self._callback(event, message)

            return

        refresh_grant = self._session._refresh_grant

        if refresh_grant is None:
            raise RDPError(-1, "AuthorizeUser is passed a null grant")

        access_token = self._session._access_token
        app_key = self._session.app_key
        uri = self._session.authentication_token_endpoint_uri

        response = await self._request_token(refresh_grant, access_token, app_key, uri)

        status_code = response.status_code
        try:
            json_content = response.json()
        except JSONDecodeError as e:
            if status_code == Session._DUMMY_STATUS_CODE:
                json_content = {
                    "error": response.code,
                    "error_description": response.reason_phrase
                    }
            else:
                raise e

        if status_code == codes.ok:
            event = UpdateEvent.REFRESH_TOKEN_SUCCESS
            message = "All is well"

            # Process the Authentication response
            expires_in = int(json_content["expires_in"])
            refresh_token = json_content["refresh_token"]
            access_token = json_content["access_token"]

            self.debug(f"Received refresh token {refresh_token}\n"
                       f"   Expire in {expires_in} seconds")

            self._session._refresh_grant.refresh_token(refresh_token)
            self._session._access_token = access_token

            self._session._token_expires_in_secs = expires_in
            self._session._token_expires_at = cur_time + expires_in

            self.delay = expires_in

            self.debug(f"Set refresh token delay to {self.delay} seconds")

            # set the authentication token to all stream in session
            self._session.set_stream_authentication_token(access_token)

        elif status_code in [codes.unauthorized, codes.forbidden]:
            event = UpdateEvent.REFRESH_TOKEN_BAD
            error = json_content.get("error", "empty error")
            error_description = json_content.get("error_description", "empty error description")
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        elif status_code is codes.bad:
            event = UpdateEvent.REFRESH_TOKEN_EXPIRED
            error = json_content.get("error", "empty error")
            error_description = json_content.get("error_description", "empty error description")
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        else:
            event = UpdateEvent.REFRESH_TOKEN_FAILED
            error = json_content.get("error", "empty error")
            error_description = json_content.get("error_description", "empty error description")
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        self._callback(event, message)

    async def _request_token(self, grant, access_token, app_key, uri):
        username = grant.get_username()
        refresh_token = grant.get_refresh_token()

        post_data = {
            "client_id": app_key,
            "grant_type": "refresh_token",
            "username": username,
            "refresh_token": refresh_token,
            "takeExclusiveSignOnControl": True
            }

        self.debug(f"Request refresh token to {uri}\n"
                   f"   with post data = {str(post_data)}")

        response = await self._session.http_request_async(
            url=uri,
            method="POST",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
                },
            data=post_data,
            auth=(username, "")
            )

        self.debug(f"Refresh token response: {response.text}")

        return response

    def _do_dispose(self):
        self._session = None
        self._callback = None
