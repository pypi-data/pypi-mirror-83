import sys


def is_windows():
    """Check if OS is Windows."""
    return sys.platform == 'win32'


def is_linux():
    """Check if OS is Linux."""
    return sys.platform == 'linux' or sys.platform == 'linux2'


def is_darwin():
    """Check if OS is Darwin."""
    return sys.platform == 'darwin'
