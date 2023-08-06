import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as dep_file:
    dependencies = [dep.rstrip() for dep in dep_file.readlines()]

setuptools.setup(
    name="nflfastpy",
    version="0.0.4",
    author="Ben Dominguez",
    author_email="bendominguez011@gmail.com",
    description="A Python package for loading NFL play by play data from nflfastR",
    long_description=long_description,
    url="https://github.com/fantasydatapros/nflfast_py",
    license="MIT",
    install_requires=['pandas'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)