from setuptools import setup, find_packages

with open("requirements.in") as f:
    setup(
        name = "btch",
        version = "0.2",
        packages = find_packages(),
        scripts = ["bin/btch"],
        install_requires = f.read().splitlines()
    )
