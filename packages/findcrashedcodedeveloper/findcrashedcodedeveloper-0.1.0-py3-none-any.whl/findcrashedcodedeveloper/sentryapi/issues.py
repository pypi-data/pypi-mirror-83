from .client import SentryClient
from .models.issue import SentryIssue


class SentryIssuesApi:
    """A class to interact with Sentry Issues API"""

    def __init__(self, client):
        """"
        Parameters
        ----------
        client : SentryClient
            sentry client for making request to sentry api server
        """
        self.client = client

    def get_list(self, organization, project):
        """Get latest issues of Sentry project

        Parameters
        ----------
        organization : str
            username of Sentry project organization
        project : str
            identifier of Sentry project

        Returns
        -------
        list of SentryIssue
            list of recent issues of project
        """
        api_point = 'projects/{}/{}/issues/'.format(
            organization,
            project
        )
        issues_data = self.client.get(api_point)
        return [SentryIssue(d) for d in issues_data]
