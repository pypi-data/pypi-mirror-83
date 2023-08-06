class RepositoryInfo:
    """A class to represent information about a Github repository"""

    def __init__(self, repository, branch):
        """
        Parameters
        ----------
        repository : GithubRepository
            github repository
        branch : str
            name of branch of repository
        """
        self.repository = repository
        self.branch = branch
