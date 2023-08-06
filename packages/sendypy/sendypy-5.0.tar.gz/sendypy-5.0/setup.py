import os

from setuptools import find_packages, setup

if os.path.exists("README.rst"):
    long_description = open("README.rst", "r").read()
else:
    long_description = "See https://code.netlandish.com/~netlandish/sendypy"


setup(
    name="sendypy",
    version=__import__("sendy").get_version(),
    packages=find_packages(),
    description="Python Interface for the Sendy API",
    author="Netlandish Inc.",
    author_email="hello@netlandish.com",
    url="https://code.netlandish.com/~netlandish/sendypy",
    long_description=long_description,
    platforms=["any"],
    install_requires=["requests>=2.19.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Web Environment",
    ],
    include_package_data=True,
)
