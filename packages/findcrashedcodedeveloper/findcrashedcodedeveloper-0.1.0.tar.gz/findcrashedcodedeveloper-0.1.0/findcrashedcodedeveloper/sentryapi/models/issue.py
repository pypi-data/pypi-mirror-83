class SentryIssue:
    """A class to represent an issue in Sentry"""
    def __init__(self, data):
        """
        Parameters
        ----------
        data : dict
            information returned by sentry issue API
        """
        self.data = data
        self.id = data['id']
        self.assignedTo = data['assignedTo']
        self.firstSeen = data['firstSeen']
        self.lastSeen = data['lastSeen']
        self.hasSeen = data['hasSeen']
        self.metadata = data['metadata']
        self.permalink = data['permalink']
        self.status = data['status']
        self.title = data['title']
        self.type = data['type']
        self.userCount = data['userCount']

        # not direct fields
        self.filename = self.metadata['filename']
