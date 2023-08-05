from pyramid_debugtoolbar.panels import DebugPanel

from pyramid.interfaces import ICSRFStoragePolicy
from ... import DualCookieCSRFStoragePolicy

_ = lambda x: x


class CSRFMultiSchemeDebugPanel(DebugPanel):
    """
    Sample debug panel
    """

    name = "CSRFMultiScheme"
    has_content = None
    template = "pyramid_csrf_multi_scheme.debugtoolbar.panels:templates/csrf_multi_scheme.dbtmako"

    # only query the policy once
    _policy = None

    # stash
    _cookie_names = None

    response = None  # we may never have a response

    def __init__(self, request):

        self.data = {
            "request_data": {
                "cookie_secure": {"in": None, "out": None, "cookie_name": None},
                "cookie_http": {"in": None, "out": None, "cookie_name": None},
            }
        }
        policy = request.registry.queryUtility(ICSRFStoragePolicy)
        if isinstance(policy, DualCookieCSRFStoragePolicy):
            self._policy = policy
            self._cookie_names = [policy.cookie_name_secure, policy.cookie_name_http]

            self.has_content = True

            self.data["request_data"]["cookie_secure"]["in"] = request.cookies.get(
                policy.cookie_name_secure
            )
            self.data["request_data"]["cookie_secure"][
                "cookie_name"
            ] = policy.cookie_name_secure

            self.data["request_data"]["cookie_http"]["in"] = request.cookies.get(
                policy.cookie_name_http
            )
            self.data["request_data"]["cookie_http"][
                "cookie_name"
            ] = policy.cookie_name_http

            # `process_response` fires before the set_cookie callbacks, so use this hack...
            def finished_callback(request):
                self._process_response_deferred()

            request.add_finished_callback(finished_callback)

    def process_response(self, response):
        """`
        process_response` fires before the set_cookie callbacks
        so we use a hack from pyramid_debugtoolbar's HeaderDebugPanel

        1. `__init__()` sets a callback to `_process_response_deferred()`
        2. `process_response()` stashes the response
        3. `_process_response_deferred` has the headers
        """
        self.response = response

    def _process_response_deferred(self):
        """
        `process_response` fires before the set_cookie callbacks
        so we use a hack from pyramid_debugtoolbar's HeaderDebugPanel
        """
        if self.response is not None:
            cookies = [i for i in self.response.headerlist if i[0] == "Set-Cookie"]
            # [('Set-Cookie', 'ci_ss_ck=eXrTEtumW4Jal3FyEXtkJijofCAyOnayzGQiPG7IAjukycfE; Domain=.dev.example.com; Path=/'),
            #  ('Set-Cookie', 'ci_s_ck=iG6dqE5mff_iR2Y95o5eENuVdC; Domain=.dev.example.com; Path=/')
            #  ]
            for ck in cookies:
                try:
                    ck_parts = ck[1].split(";")
                    (ck_name, ck_value) = ck_parts[0].split(
                        "=", 1
                    )  # maxsplit 1, because the value could be an encoding with == as a right pad
                    if ck_name in self._cookie_names:
                        if (
                            ck_name
                            == self.data["request_data"]["cookie_secure"]["cookie_name"]
                        ):
                            self.data["request_data"]["cookie_secure"]["out"] = ck_value
                        elif (
                            ck_name
                            == self.data["request_data"]["cookie_http"]["cookie_name"]
                        ):
                            self.data["request_data"]["cookie_http"]["out"] = ck_value
                except Exception as exc:
                    # TODO: logging
                    pass

    @property
    def nav_title(self):
        return _(self.name)

    @property
    def title(self):
        return _(self.name)

    @property
    def url(self):
        return ""

    def render_content(self, request):
        return DebugPanel.render_content(self, request)
