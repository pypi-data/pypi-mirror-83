import pathlib

import os_aiohttp_utils


def test_version():
    version_file = (
        pathlib.Path(__file__)
        .parents[1]
        .joinpath("src/os_aiohttp_utils/VERSION")
        .absolute()
    )
    assert os_aiohttp_utils.__version__ == open(version_file).read().strip()


if __name__ == "__main__":
    test_version()
