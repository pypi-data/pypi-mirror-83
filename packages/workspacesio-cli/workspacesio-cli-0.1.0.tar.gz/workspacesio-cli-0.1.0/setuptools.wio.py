import os

from setuptools import find_packages, setup

deps = [
    "boto3",
    "click",
    "click-aliases",
    "colorama",
    "elasticsearch>=7.0.0,<8.0.0",
    "ffmpeg-python",
    "minio",
    "pydantic",
    "requests",
    "requests-toolbelt",
    "tqdm",
]

setup(
    name="workspacesio-cli",
    version="0.1.0",
    script_name="setuptools.wio.py",
    python_requires=">3.7",
    zip_safe=False,
    install_requires=deps,
    include_package_data=True,
    packages=["workspacesio.cli", "workspacesio.common"],
    entry_points={
        "console_scripts": [
            "wio=workspacesio.cli:cli",
        ],
    },
)
