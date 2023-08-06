from .client import GithubClient
from .files import GithubFilesAPI
from .blames import GithubBlamesAPI


class GithubAPI:
    """A class to interact with github API"""

    def __init__(self, api_token, api_server_url='https://api.github.com/graphql'):
        """
        Parameters
        ----------
        api_token : str
            api token to interact with github v4 API
        api_server_url : str
            Github API server url (default is 'https://api.github.com/graphql')
        """
        self.client = GithubClient(api_token, api_server_url=api_server_url)
        self.files = GithubFilesAPI(self.client)
        self.blames = GithubBlamesAPI(self.client)
