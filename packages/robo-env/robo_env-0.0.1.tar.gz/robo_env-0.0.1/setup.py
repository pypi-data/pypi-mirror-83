import setuptools
from pathlib import Path

setuptools.setup(
    name='robo_env',
    version='0.0.1',
    description="A OpenAI ",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="robo_env*"),
    install_requires=['gym']  # And any other dependencies foo needs
)