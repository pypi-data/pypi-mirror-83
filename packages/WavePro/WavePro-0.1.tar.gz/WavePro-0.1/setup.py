from setuptools import setup, find_packages

setup(
    name="WavePro",
    version="0.1",
    license="MIT Licence",

    url="https://github.com/ailabnjtech/Mickey-Mouse-Clubhouse",
    author="zhang_1998",
    author_email="",

    packages=find_packages(),
    install_requires=['torch>=1.6.0', 'numpy>=1.19.1'],
    include_package_data=True,
    platforms="any",
)