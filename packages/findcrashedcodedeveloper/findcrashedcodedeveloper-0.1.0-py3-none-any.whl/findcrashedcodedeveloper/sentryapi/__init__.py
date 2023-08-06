from .client import SentryClient
from .issues import SentryIssuesApi
from .events import SentryEventsApi


class SentryAPI:
    """A class to interact with Sentry API"""

    def __init__(self, api_token, server='https://sentry.io'):
        """
        Parameters
        ----------
        api_token : str
            sentry api token
        server : str
            sentry api server url to interact with API
        """
        self.client = SentryClient(api_token, server=server)
        self.issues = SentryIssuesApi(self.client)
        self.events = SentryEventsApi(self.client)
