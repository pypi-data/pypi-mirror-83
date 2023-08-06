from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="torch-cv",
    version="0.0.1",
    author="Raghhuveer Jaikanth",
    author_email="raghhuveerj97@gmail.com",
    description="A high level package for Computer Vision with pytorch",
    long_description=long_description,
    long_description_content_type="text/reStructuredText ",
    url="https://github.com/RJaikanth/torch-cv",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Operating System :: Unix"
    ],
    python_requires=">=3.7",
    scripts=["scripts/tcv"]
)
