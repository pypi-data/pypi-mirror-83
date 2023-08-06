# coding: utf8

from refinitiv.dataplatform.core.session import Session, DesktopSession, PlatformSession, GrantPassword

__all__ = ['CoreFactory',
           'open_desktop_session',
           'open_platform_session'
           # 'close_session'
           ]


class CoreFactory:

    @staticmethod
    def create_session(session_params):
        if isinstance(session_params, Session.Params):
            # check the platform
            if isinstance(session_params, DesktopSession.Params):
                return DesktopSession(app_key=session_params._app_key,
                                      on_state=session_params._on_state_cb,
                                      on_event=session_params._on_event_cb,
                                      token=session_params._dacs_params.authentication_token,
                                      deployed_platform_username=session_params._dacs_params.deployed_platform_username,
                                      dacs_position=session_params._dacs_params.dacs_position,
                                      dacs_application_id=session_params._dacs_params.dacs_application_id)
            elif isinstance(session_params, PlatformSession.Params):
                return PlatformSession(app_key=session_params._app_key,
                                       grant=session_params.get_grant(),
                                       deployed_platform_host=session_params._deployed_platform_host,
                                       # Deployed Platform parameter
                                       signon_control=session_params.take_signon_control(),
                                       on_state=session_params._on_state_cb,
                                       on_event=session_params._on_event_cb,
                                       token=session_params._dacs_params.authentication_token,
                                       deployed_platform_username=session_params._dacs_params.deployed_platform_username,
                                       dacs_position=session_params._dacs_params.dacs_position,
                                       dacs_application_id=session_params._dacs_params.dacs_application_id)
        else:
            raise Exception("Wrong session parameter")

    @staticmethod
    def create_desktop_session(app_key, on_state=None, on_event=None):
        return DesktopSession(app_key, on_state, on_event)

    @staticmethod
    def create_platform_session(app_key,
                                oauth_grant_type=None,
                                deployed_platform_host=None,  # Deployed Platform parameter
                                authentication_token=None,  # Deployed Platform parameter
                                take_signon_control=True,
                                deployed_platform_username=None,
                                dacs_position=None,
                                dacs_application_id=None,
                                on_state=None,
                                on_event=None,
                                auto_reconnect=None, ):
        return PlatformSession(app_key=app_key,
                               grant=oauth_grant_type,
                               deployed_platform_host=deployed_platform_host,  # Deployed Platform parameter
                               authentication_token=authentication_token,  # Deployed Platform parameter
                               signon_control=take_signon_control,
                               deployed_platform_username=deployed_platform_username,
                               dacs_application_id=dacs_application_id,
                               dacs_position=dacs_position,
                               on_state=on_state,
                               on_event=on_event,
                               auto_reconnect=auto_reconnect, )


def open_desktop_session(app_key):
    from refinitiv.dataplatform.legacy.tools import set_default_session
    session = CoreFactory.create_desktop_session(app_key)
    close_session()
    set_default_session(session)
    session.open()
    return session


def open_platform_session(app_key,
                          # for RDP
                          grant=None,
                          # for deployed platform
                          deployed_platform_host=None,
                          deployed_platform_username=None):
    from refinitiv.dataplatform.legacy.tools import set_default_session
    session = CoreFactory.create_platform_session(app_key,
                                                  #  for RDP
                                                  oauth_grant_type=grant,
                                                  deployed_platform_host=deployed_platform_host,
                                                  deployed_platform_username=deployed_platform_username)
    close_session()
    set_default_session(session)
    session.open()
    return session


def close_session():
    from refinitiv.dataplatform.legacy.tools import DefaultSession
    DefaultSession.close_default_session()
