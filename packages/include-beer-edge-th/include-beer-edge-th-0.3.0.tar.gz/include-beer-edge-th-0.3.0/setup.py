from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# use requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()
print(required)

# This call to setup() does all the work
setup(
    name="include-beer-edge-th",
    version="0.3.0",
    description="Monitor temperature and humidity on edge device",
    long_description=README,
    # long_description_content_type="text/markdown",
    url="https://github.com/mbhein/include-beer-edge-th",
    author="Matthew Hein",
    author_email="matthew.hein@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["includebeeredgeth"],
    include_package_data=True,
    install_requires=[
      'include-beer-DHT11',
      'include-beer-core',
    ],
)
