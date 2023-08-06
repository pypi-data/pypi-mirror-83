from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['calendar_base']

setup(
    name="calendar_base",

    version="0.0.1",
    # 0.0.1 - added EWS.ConnectionStatus property to read the status at will

    packages=packages,
    install_requires=[
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A package to help organize calendar events",
    long_description=long_description,
    license="PSF",
    keywords="grant miller calendar base office365 google calendar",
    url="https://github.com/GrantGMiller/flask_dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/flask_dictabase",
    }

)
