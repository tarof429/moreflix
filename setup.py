from setuptools import setup, find_packages

setup(
    name="moreflix",
    version='0.1.0',
    author="Taro Fukunaga",
    author_email="taro@example.com",
    description="moreflix",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tarof429/moreflix",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    license="BSD-3-Clause"
)