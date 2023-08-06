import setuptools
from pathlib import Path

setuptools.setup(
    name='Gym_env',
    version='0.0.1',
    description="A OpenAI Gym Env",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="Gym_env*"),
    install_requires=['gym']  # And any other dependencies foo needs
)