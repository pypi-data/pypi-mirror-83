from .models.file import FileContent, FileInfo

_ls_query = '''
query {{
  repository(owner: "{}", name: "{}") {{
    object(expression: "{}") {{
  ... on Tree {{
        entries {{
          name
          type
        }}
      }}
    }}
  }}
}}
'''


def _build_ls_query(owner, repository, expression):
    return _ls_query.format(owner, repository, expression)


_content_query = '''
query {{
  repository(owner: "{}", name: "{}") {{
    object(expression: "{}:{}") {{
      ... on Blob {{
        text
      }}
    }}
  }}
}}
'''


def _build_content_query(owner, repository, branch, file_path):
    return _content_query.format(owner, repository, branch, file_path)


class GithubFilesAPI:
    """Get information about file in github repository"""

    def __init__(self, client):
        """
        Parameters
        ----------
        client : GithubClient
            client used to interact with Github API
        """
        self._client = client

    def get_files(self, repository, folder_path, branch='master'):
        """Get information about the files in folder in github repository

        Parameters
        ----------
        repository : GithubRepository
            repository object
        folder_path : str
            unix style path of folder inside the repository.
            example:- findthedeveloper/githubapi
        branch : str, optional
            name of branch (default is 'master')

        Returns
        -------
        list
            a list of FileInfo objects
        """
        expression = '{}:{}'.format(branch, folder_path)
        query = _build_ls_query(
            repository.owner, repository.repository_name, expression
        )
        result = self._client.get(query)

        object_data = result['data']['repository']['object']
        if object_data is None:
            raise FileNotFoundError(folder_path)

        folder_files_info = object_data['entries']
        result = []
        for file_info in folder_files_info:
            name = file_info['name']
            filepath = '{}/{}'.format(folder_path, name)
            is_directory = True if file_info['name'] == 'tree' else False
            result.append(
                FileInfo(name, filepath, is_directory)
            )
        return result

    def get_file_content(self, repository, filepath, branch='master'):
        """Get content of file

        Parameters
        ----------
        repository : GithubRepository
            repository object
        filepath : str
            unix style path of file inside the repository.
            example:- findthedeveloper/githubapi/files.py
        branch : str, optional
            name of branch (default is 'master')

        Returns
        -------
        FileContent
            content of file
        """
        query = _build_content_query(
            repository.owner, repository.repository_name, branch, filepath
        )
        data = self._client.get(query)
        object_data = data['data']['repository']['object']
        if object_data is None:
            raise FileNotFoundError(filepath)
        return FileContent(object_data['text'])
