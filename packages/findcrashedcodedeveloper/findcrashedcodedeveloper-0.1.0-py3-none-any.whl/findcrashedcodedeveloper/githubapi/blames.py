from .models.blame import GithubBlame

_blame_query = '''
query {{
  repository(owner: "{}", name: "{}") {{
    ref(qualifiedName: "{}") {{
      target {{
        ... on Commit {{
          blame(path: "{}") {{
            ranges {{
              startingLine
              endingLine
              commit {{
                author {{
                  name
                  email
                  user {{
                    login
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
'''


def _build_blame_query(owner, repository, branch, file_path):
    return _blame_query.format(owner, repository, branch, file_path)


class GithubBlamesAPI:
    def __init__(self, client):
        """
        Parameters
        ----------
        client : GithubClient
            client used to interact with Github API
        """
        self._client = client

    def get_blame(self, repository, filepath, branch='master'):
        """Get Blame info for the file

        Parameters
        ----------
        repository : GithubRepository
            repository object
        filepath : str
            unix style path of file inside the repository.
            example:- findthedeveloper/githubapi/blames.py
        branch : str, optional
            name of branch (default is 'master')

        Returns
        -------
        GithubBlame
            blame info of the file
        """
        query = _build_blame_query(
            repository.owner, repository.repository_name, branch, filepath
        )
        result = self._client.get(query)

        blame_ranges = result['data']['repository']['ref']['target']['blame']['ranges']

        if not blame_ranges:
            raise FileNotFoundError(filepath)

        blame_data = []
        for blame in blame_ranges:
            blame_data.append({
                'startingLine': blame['startingLine'],
                'endingLine': blame['endingLine'],
                'author': {
                    'name': blame['commit']['author']['name'],
                    'email': blame['commit']['author']['email'],
                    'username': blame['commit']['author']['user']['login']
                }
            })
        return GithubBlame(blame_data)
