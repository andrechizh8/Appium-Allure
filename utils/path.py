from pathlib import Path


def path_to_apk(env_path:str):
    return Path(__file__).parent.parent.joinpath(env_path).absolute().__str__()

