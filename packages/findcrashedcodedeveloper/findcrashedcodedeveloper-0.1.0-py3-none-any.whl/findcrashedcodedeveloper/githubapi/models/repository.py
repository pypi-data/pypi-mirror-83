class GithubRepository:
    """A class to represent a github repository"""

    def __init__(self, owner, repository_name):
        """
        Parameters
        ----------
        owner : str
            username of owner of repository
        repository_name : str
            name of repository
        """
        self.owner = owner
        self.repository_name = repository_name
