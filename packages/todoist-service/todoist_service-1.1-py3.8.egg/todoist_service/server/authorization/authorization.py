import random
import string

from flask import redirect, request, abort, make_response, url_for
from requests_oauthlib import OAuth2Session

from .consts import *
from .registration import register_user


class AuthorizationHandler:
    def __init__(self,
                 server_redirect_url: str,
                 inner_server: str,
                 outer_server: str,
                 client_id: str,
                 client_secret: str,
                 todoist_permissions: str):
        self.server_redirect_url = server_redirect_url
        self.inner_server = inner_server
        self.outer_server = outer_server
        self.client_id = client_id
        self.client_secret = client_secret
        self.todoist_permissions = todoist_permissions

    def handle_authorization_request(self, client):
        generated_state = ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(random.randint(80, 100)))

        result = client.prepare_request_uri(TODOIST_AUTHORIZE_URL,
                                            redirect_uri=self.server_redirect_url,
                                            scope=self.todoist_permissions, state=generated_state)

        response = redirect(result)
        response.set_cookie(COOKIE_STATE, generated_state)
        return response

    def handle_redirect_request(self, client):
        # validate state
        expected_state = request.cookies.get(COOKIE_STATE)
        if not expected_state == request.args.get(PARAM_STATE):
            abort(make_response("invalid state"))

        # parse uri params
        url = request.url.replace(self.inner_server, self.outer_server)
        parsed = client.parse_request_uri_response(url, state=expected_state)

        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=TODOIST_TOKEN_URL,
                                  client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  include_client_id=True,
                                  code=parsed[PARAM_CODE])

        # register user to system
        token, user_id = register_user(access_token=token[PARAM_ACCESS_TOKEN])

        # redirect user to the settings page
        response = redirect(url_for(".settings"))

        # set the cookie so that we can recognize the user
        response.set_cookie(COOKIE_USERID, user_id)

        return response
