import os

from pathlib import PurePath

from clint.textui.progress import Bar

from polyaxon_cli.managers.ignore import IgnoreManager


def get_files_in_current_directory(file_type):
    """Gets the list of files in the current directory and subdirectories.
    Respects .plxignore file if present
    """
    local_files = []
    total_file_size = 0

    file_paths = IgnoreManager.get_unignored_file_paths()

    for file_path in file_paths:
        local_files.append((file_type,
                            (unix_style_path(file_path), open(file_path, 'rb'), 'text/plain')))
        total_file_size += os.path.getsize(file_path)

    return local_files, sizeof_fmt(total_file_size)


def unix_style_path(path):
    if os.path.sep != '/':
        return path.replace(os.path.sep, '/')
    return path


def matches_glob_list(path, glob_list):
    """Given a list of glob patterns, returns a if a path matches any glob in the list."""
    for glob in glob_list:
        try:
            if PurePath(path).match(glob):
                return True
        except TypeError:
            pass
    return False


def sizeof_fmt(num, suffix='B'):
    """
    Print in human friendly format
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def create_progress_callback(encoder):
    encoder_len = encoder.len
    bar = Bar(expected_size=encoder_len, filled_char='=')

    def callback(monitor):
        bar.show(monitor.bytes_read)
    return callback
