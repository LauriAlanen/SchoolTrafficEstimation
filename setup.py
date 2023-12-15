from setuptools import setup, find_packages

setup(
    name="LukkariKoneTools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask_cors",
        "pandas",
        "requests",
        "urllib3",
        "selenium",
        "alive_progress",
    ],
)
