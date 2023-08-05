from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# mypy: ignore-errors

import os
import re
import shutil
import subprocess
import sys
from typing import List
import zipfile

from setuptools import Distribution, find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist as sdist_orig


def find_version(path):
    with open(path) as f:
        match = re.search(
            r"^__version__ = os.getenv\(\"ANYSCALE_CLI_VERSION\", ['\"]([^'\"]*)['\"]\)",
            f.read(),
            re.MULTILINE,
        )
        if match:
            return os.getenv("ANYSCALE_CLI_VERSION") or match.group(1)
        raise RuntimeError("Unable to find version string.")


def move_file(filename):
    # TODO(rkn): This feels very brittle. It may not handle all cases. See
    # https://github.com/apache/arrow/blob/master/python/setup.py for an
    # example.
    source = filename

    destination = os.path.join(os.path.dirname(__file__), filename)
    # Create the target directory if it doesn't already exist.
    parent_directory = os.path.dirname(destination)
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
    if not os.path.exists(destination):
        print("Copying {} to {}.".format(source, destination))
        shutil.copy(source, destination, follow_symlinks=True)


def download_and_copy_files(url: str, files_to_copy: List[str]) -> None:
    """
    Downloads an archive from S3, unzips it and then copies the file to the anyscale folder.
    """
    import io
    import requests
    import tempfile

    work_dir = tempfile.mkdtemp()
    try:
        content = requests.get(url).content
        archive = zipfile.ZipFile(io.BytesIO(content))
        archive.extractall(pwd=work_dir.encode())
        for f in files_to_copy:
            destination = os.path.join("anyscale", f)
            # Remove the file if it already exists to make sure old
            # versions get removed.
            try:
                os.remove(destination)
            except OSError:
                pass
            shutil.copy2(f, destination)
            os.chmod(destination, 0o755)
            move_file(destination)
    finally:
        shutil.rmtree(work_dir)


def download_and_copy_fswatch():
    download_and_copy_files(
        "https://anyscale-dev.s3-us-west-2.amazonaws.com/fswatch-1.14.0-2.zip",
        ["fswatch-linux", "fswatch-darwin", "libfswatch.11.dylib"],
    )


def download_and_copy_rsync():
    download_and_copy_files(
        "https://anyscale-dev.s3-us-west-2.amazonaws.com/rsync-3.2.3-darwin.zip",
        [
            "libcrypto.1.1.dylib",
            "liblz4.1.dylib",
            "libxxhash.0.dylib",
            "libzstd.1.dylib",
            "rsync",
        ],
    )


class SdistCommand(sdist_orig):
    def run(self):
        download_and_copy_fswatch()
        download_and_copy_rsync()
        # run original sdist
        super().run()


class BinaryDistribution(Distribution):
    def is_pure(self):
        return True

    def has_ext_modules(self):
        return True


RAY_COMMIT = "5ef1784024a3a049399fcc3f202c9a70e2b8dcb4"
RAY_VERSION = "ray-1.1.0.dev0"


RAY_WHEELS = {
    "linux": {
        "3.8": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp38-cp38-manylinux1_x86_64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
        "3.7": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp37-cp37m-manylinux1_x86_64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
        "3.6": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp36-cp36m-manylinux1_x86_64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
    },
    "darwin": {
        "3.8": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp38-cp38-macosx_10_13_x86_64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
        "3.7": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp37-cp37m-macosx_10_13_intel.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
        "3.6": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp36-cp36m-macosx_10_13_intel.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
    },
    "win32": {
        "3.8": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp38-cp38-win_amd64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
        "3.7": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp37-cp37m-win_amd64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
        "3.6": "https://s3-us-west-2.amazonaws.com/ray-wheels/master/{}/{}-cp36-cp36m-win_amd64.whl".format(
            RAY_COMMIT, RAY_VERSION
        ),
    },
}


def install_private_ray(anyscale_path):
    platform = sys.platform
    py_version = "{0}.{1}".format(*sys.version_info[:2])

    matching_wheel = None
    for target_platform, wheel_map in RAY_WHEELS.items():
        print(f"Evaluating os={target_platform}, python={list(wheel_map)}")
        if platform.startswith(target_platform):
            if py_version in wheel_map:
                matching_wheel = wheel_map[py_version]
                break
        print("Not matched.")

    if matching_wheel is None:
        raise Exception(
            "Unable to identify a matching Ray wheel for Platform: {}, Python: {}".format(
                platform, py_version
            )
        )

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--target={}".format(os.path.join(anyscale_path, "anyscale", "anyscale_ray")),
        "-U",
        matching_wheel,
    ]
    print(f"Running: {' '.join(cmd)}.")
    subprocess.check_call(cmd)  # noqa: B1


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        print("Installing private version of Ray")
        download_and_copy_fswatch()
        download_and_copy_rsync()
        install_private_ray(os.path.dirname(__file__))


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        print("Installing private version of Ray")
        install_private_ray(self.install_lib)


setup(
    name="anyscale",
    version=find_version("anyscale/__init__.py"),
    author="Anyscale Inc.",
    description=("Command Line Interface for Anyscale"),
    packages=find_packages(exclude="tests"),
    cmdclass={
        "sdist": SdistCommand,
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    },
    distclass=BinaryDistribution,
    setup_requires=["setuptools_scm"],
    data_files=[
        (
            "generated",
            [
                "anyscale/fswatch-linux",
                "anyscale/fswatch-darwin",
                "anyscale/libfswatch.11.dylib",
                "anyscale/libcrypto.1.1.dylib",
                "anyscale/liblz4.1.dylib",
                "anyscale/libxxhash.0.dylib",
                "anyscale/libzstd.1.dylib",
                "anyscale/rsync",
            ],
        ),
    ],
    install_requires=[
        "aiohttp",
        "boto3",
        "Click>=7.0",
        "expiringdict",
        "GitPython",
        "jinja2",
        "jsonpatch",
        "jsonschema",
        "packaging",
        "ray>=0.8.5",
        "requests",
        "tabulate",
        "wrapt",
    ],
    entry_points={"console_scripts": ["anyscale=anyscale.scripts:main"]},
    include_package_data=True,
    zip_safe=False,
)
