# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import hashlib
import random

from webob.exc import HTTPForbidden
from wtforms import Form, HiddenField, validators

from mediagoblin import mg_globals

# Use the system (hardware-based) random number generator if it exists.
# -- this optimization is lifted from Django
if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange


class CsrfForm(Form):
    """Simple form to handle rendering a CSRF token and confirming it
    is included in the POST."""

    csrf_token = HiddenField("",
                             [validators.Required()])


def render_csrf_form_token(request):
    """Render the CSRF token in a format suitable for inclusion in a
    form."""

    form = CsrfForm(csrf_token=request.environ['CSRF_TOKEN'])

    return form.csrf_token


class CsrfMiddleware(object):
    """CSRF Protection Middleware

    Adds a CSRF Cookie to responses and verifies that it is present
    and matches the form token for non-safe requests.
    """

    MAX_CSRF_KEY = 2 << 63
    SAFE_HTTP_METHODS = ("GET", "HEAD", "OPTIONS", "TRACE")

    def __init__(self, mg_app):
        self.app = mg_app

    def process_request(self, request):
        """For non-safe requests, confirm that the tokens are present
        and match.
        """

        # get the token from the cookie
        try:
            request.environ['CSRF_TOKEN'] = \
                request.cookies[mg_globals.app_config['csrf_cookie_name']]

        except KeyError, e:
            # if it doesn't exist, make a new one
            request.environ['CSRF_TOKEN'] = self._make_token(request)

        # if this is a non-"safe" request (ie, one that could have
        # side effects), confirm that the CSRF tokens are present and
        # valid
        if request.method not in self.SAFE_HTTP_METHODS:
            return self.verify_tokens(request)

    def process_response(self, request, response):
        """Add the CSRF cookie to the response if needed and set Vary
        headers.
        """

        # set the CSRF cookie
        response.set_cookie(
            mg_globals.app_config['csrf_cookie_name'],
            request.environ['CSRF_TOKEN'],
            max_age=60 * 60 * 24 * 7 * 52,
            path='/',
            domain=mg_globals.app_config.get('csrf_cookie_domain', None),
            secure=(request.scheme.lower() == 'https'),
            httponly=True)

        # update the Vary header
        response.vary = (response.vary or []) + ['Cookie']

    def _make_token(self, request):
        """Generate a new token to use for CSRF protection."""

        return hashlib.md5("%s%s" %
                           (randrange(0, self.MAX_CSRF_KEY),
                            mg_globals.app_config['secret_key'])).hexdigest()

    def verify_tokens(self, request):
        """Verify that the CSRF Cookie exists and that it matches the
        form value."""

        # confirm the cookie token was presented
        cookie_token = request.cookies.get(
            mg_globals.app_config['csrf_cookie_name'],
            None)

        if cookie_token is None:
            # the CSRF cookie must be present in the request
            return HTTPForbidden()

        # get the form token and confirm it matches
        form = CsrfForm(request.POST)
        if form.validate():
            form_token = form.csrf_token.data

            if form_token == cookie_token:
                # all's well that ends well
                return

        # either the tokens didn't match or the form token wasn't
        # present; either way, the request is denied
        return HTTPForbidden()