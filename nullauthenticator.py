"""Null Authenticator for JupyterHub

For cases where authentication should be disabled,
e.g. only allowing access via API tokens.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado.auth import OAuth2Mixin
from tornado import gen, web
from jupyterhub.auth import Authenticator
from jupyterhub.handlers.base import BaseHandler

__version__ = '1.1.0.dev'


class NullLoginHandler(BaseHandler):
    def get(self):
        self.log.warning("%s" % self)
        raise web.HTTPError(403, "Login is not supported")


class NullAuthenticator(Authenticator):

    # auto_login skips 'Login with...' page on Hub 0.8
    auto_login = True

    # for Hub 0.7, show 'login with...'
    login_service = 'null'

    def get_handlers(self, app):
        self.log.warning("%s" % self)
        return [('/nologin', NullLoginHandler)]
        
    @gen.coroutine
    def authenticate(self, handler, data):
        if data is not None:
            self.log.warning("%s" % self)
            return data['username']
        if handler is not None:
            self.log.warning("%s" % handler)
            return handler.get_argument('username')
        return 'admin'
      