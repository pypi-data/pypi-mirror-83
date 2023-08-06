from setuptools import setup, find_packages

# setup(name="deployx", packages=find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="deployx-server-sdk1", # Replace with your own username
    version="0.0.1",
    author="CaptainKryuk",
    author_email="andrey.kryukov@protonmail.com",
    description="deployx-server-sdk package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CaptainKryuk/deployx-server-sdk",
    packages=find_packages('dxclient'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)