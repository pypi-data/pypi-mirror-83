class GithubUser:
    """A class to represent a Github user"""

    def __init__(self, name, email, username):
        """
        Parameters
        ----------
        name : str
            name of user
        email : str
            email id of user
        username : str
            github username of user
        """
        self._name = name
        self._email = email
        self._username = username

    def get_name(self):
        """Get name of user"""
        return self._name

    def get_email(self):
        """Get email of user"""
        return self._email

    def get_username(self):
        """Get Github username of user"""
        return self._username
