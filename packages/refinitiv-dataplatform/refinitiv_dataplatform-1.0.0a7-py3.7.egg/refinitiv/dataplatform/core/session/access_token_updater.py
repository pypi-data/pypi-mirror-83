import time
from json import JSONDecodeError

import requests_async as requests

from refinitiv.dataplatform.core.log_reporter import LogReporter
from refinitiv.dataplatform.errors import RDPError
from .event import UpdateEvent
from .grant_password import GrantPassword
from .session import Session
from .updater import Updater

codes = requests.codes


class AccessTokenUpdater(Updater, LogReporter):

    def __init__(self, session, delay, callback):
        Updater.__init__(self, delay=delay)
        LogReporter.__init__(self, logger=session)

        self._session = session
        self._callback = callback

    async def _do_update(self):
        grant = self._session._grant

        if grant is None:
            raise RDPError(-1, "AuthorizeUser is passed a null grant")

        if not isinstance(grant, GrantPassword):
            raise RDPError(-1, "Invalid EDP Authentication Grant specification")

        self._session._refresh_grant.username(grant.get_username())

        response = await self._request_token(
            grant,
            self._session._app_key,
            self._session.authentication_token_endpoint_uri,
            self._session._take_signon_control
            )

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
            event = UpdateEvent.ACCESS_TOKEN_SUCCESS
            message = "All is well"

            expires_in = int(json_content["expires_in"])
            refresh_token = json_content["refresh_token"]

            self._session._refresh_grant.refresh_token(refresh_token)
            self._session._access_token = json_content["access_token"]
            self._session._token_expires_in_secs = expires_in
            self._session._token_expires_at = time.time() + expires_in
            self.debug(f"Received refresh token {refresh_token}\n"
                       f"   Expire in {expires_in} seconds")

        elif status_code in [codes.bad, codes.unauthorized, codes.forbidden]:
            event = UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED
            error = json_content.get("error", "empty error")
            error_description = json_content.get("error_description", "empty error description")
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        else:
            event = UpdateEvent.ACCESS_TOKEN_FAILED
            error = json_content.get("error", "empty error")
            error_description = json_content.get("error_description", "empty error description")
            message = error_description
            self.error(f"[Error {status_code} - {error}] {error_description}")

        self._callback(event, message)

    async def _request_token(self, grant, app_key, uri, take_signon_control):
        username = grant.get_username()

        post_data = {
            "scope": grant.get_token_scope(),
            "grant_type": "password",
            "username": username,
            "password": grant.get_password(),
            "takeExclusiveSignOnControl": "true" if take_signon_control else "false"
            }

        if app_key is not None:
            post_data["client_id"] = app_key

        self.debug(f"Request access token to {uri}\n"
                   f"   with post data {str(post_data)}\n"
                   f"   with auth {username}")

        response = await self._session.http_request_async(
            url=uri,
            method="POST",
            headers={"Accept": "application/json"},
            data=post_data,
            auth=(username, "")
            )

        self.debug(f"Access token response: {response.text}")

        return response

    def _do_dispose(self):
        self._session = None
        self._callback = None
