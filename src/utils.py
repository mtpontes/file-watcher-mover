def get_path_str(path: str | bytes) -> str:
    if isinstance(path, bytes):
        return path.decode('utf-8', errors='replace')
    return path