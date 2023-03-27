import os


def env_var_enabled(env_var_name: str, default: bool) -> bool:
    if env_var_name in os.environ:
        return os.environ[env_var_name] in {'true', 'True', '1'}
    return default
