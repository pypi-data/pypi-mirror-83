import os
from setuptools import setup, find_packages


if os.name == "nt":
    third_parties = ["win10toast"]
else:
    third_parties = []


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="big-O calculator",
    version="0.0.9.8.1",
    description="A calculator to predict big-O of sorting functions",
    url="https://github.com/Alfex4936",
    author="Seok Won",
    author_email="ikr@kakao.com",
    license="MIT",
    # packages=["bigO"],
    packages=find_packages(exclude=["tests", "benchmarks", "node_modules"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=third_parties,
    zip_safe=False,
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest"],
)
