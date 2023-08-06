def _sanitize_repository_path(path):
    if path and path[0] == '/':
        path = str(path[1:])
    return path


def get_all_possible_repository_paths(absolute_filepath, repository_name):
    """Get possible repository paths of this file in repository_name

    absolute_filepath : str
        absolute path of crashed file
    repository_name : str
        name of repository for which this file may belong

    Returns
    -------
    list of str
        all possible repository path of file in this repository
    """
    separator = repository_name + '/'
    path_parts = absolute_filepath.split(separator)

    if len(path_parts) <= 1:
        return []

    result = []
    for i in range(1, len(path_parts)):
        possible_repository_path = separator.join(path_parts[i:])
        possible_repository_path = _sanitize_repository_path(
            possible_repository_path
        )
        result.append(possible_repository_path)

    return result


def get_all_possible_repository_root_directory_paths(absolute_filepath, repository_files):
    """Get possible repository paths of this file in repository_name

    absolute_filepath : str
        absolute path of crashed file
    repository_files : list of FileInfo
        list of FileInfo of root level files in repository

    Returns
    -------
    list of str
        all possible repository path of file in this repository
    """
    result = []
    for file in repository_files:
        if file.is_directory():
            possible_paths = get_all_possible_repository_paths(
                absolute_filepath, file.get_name()
            )
            for path in possible_paths:
                result.append('{}/{}'.format(file.get_filepath(), path))
        elif absolute_filepath.endswith('/' + file.get_name()):
            result.append(file.get_filepath())

    return result
