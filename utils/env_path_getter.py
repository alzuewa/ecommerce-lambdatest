from pathlib import Path


def get_resource_path(local_file_path):
    return Path(__file__).parent.parent.joinpath(local_file_path).absolute()