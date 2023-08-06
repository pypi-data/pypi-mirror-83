import json
from graphqlclient import GraphQLClient


class GithubClient:
    def __init__(self, api_token, api_server_url='https://api.github.com/graphql'):
        """Client to interact with github graphql API

        Parameters
        ----------
        api_token : str
            Github API token of user
        api_server_url : str
            Github API server url (default is 'https://api.github.com/graphql')
        """
        self._api_token = api_token
        self._client = GraphQLClient(api_server_url)
        if api_token:
            self._client.inject_token('bearer ' + api_token)

    def get(self, query):
        """Make graphql query to github API

        Parameters
        ----------
        query : str
            graphql query

        Returns
        -------
        response_data : dict or list
            json decoded reponse of api call
        """
        result = self._client.execute(query)
        data = json.loads(result)
        return data
