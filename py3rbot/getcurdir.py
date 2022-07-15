def getcurdir(__file: str) -> str:
    import os
    return os.path.dirname(os.path.realpath(__file))
