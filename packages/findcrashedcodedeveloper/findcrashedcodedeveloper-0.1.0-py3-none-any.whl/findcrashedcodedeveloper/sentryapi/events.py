from .models.event import SentryEvent


class SentryEventsApi:
    """A class to interact with Sentry Events API"""

    def __init__(self, client):
        """"
        Parameters
        ----------
        client : SentryClient
            sentry client for making request to sentry api server
        """
        self.client = client

    def get_latest_event(self, issue_id):
        """Get latest event of Issue

        Parameters
        ----------
        issue_id : str
            id of Sentry Issue

        Returns
        -------
        SentryEvent
            sentry event object
        """
        api_point = 'issues/{}/events/latest/'.format(
            issue_id
        )
        event_data = self.client.get(api_point)
        return SentryEvent(event_data)
