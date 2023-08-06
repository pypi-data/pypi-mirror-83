from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="python-on-whales",
    version=0.1,
    install_requires=Path("requirements.txt").read_text().splitlines(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "python-on-whales=python_on_whales.command_line_entrypoint:main"
        ],
    },
    long_description=(Path(__file__).parent / "README.md").read_text(),
    include_package_data=True,
    long_description_content_type='text/markdown',
)
