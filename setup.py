from setuptools import setup, find_packages

setup(
    name="backterm",
    version="1.0",
    description="Download a random image from Unsplash and set it as the background for the Windows Terminal.",
    author="Hadas Volkov",
    author_email="hadasvol@pm.me",
    url="https://github.com/hadasvolk/BackTerm",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "backterm=backterm:main"
        ]
    },
)
