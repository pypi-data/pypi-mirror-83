import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="grexx-gcloudtools",
    version="0.0.2",
    description="Tools for accessing Google Cloud interfaces for Budget Coach services",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Grexx",
    author_email="servicedesk@grexx.net",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=["click", "tqdm", "google-cloud-core", "google-cloud-core", 
                      "google-cloud-bigquery", "google-cloud-storage", "google-cloud-tasks",
                      "google-api-core", "google-api-python-client", "google-auth",
                      "google-auth-httplib2", "flask", "Flask-Restful", "pyarrow"],
)
