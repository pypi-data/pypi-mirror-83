from setuptools import setup, find_packages

setup(
    name="smart-manage-crypt",
    version='0.0.1b',
    packages=find_packages(),
    install_requires=["pycrypto==2.6.1"],
)
