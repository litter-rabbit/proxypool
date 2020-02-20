

class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__()

    def __str__(self):
        return repr('代理池已满')