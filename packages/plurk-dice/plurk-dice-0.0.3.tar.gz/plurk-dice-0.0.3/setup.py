from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plurk-dice",
    version="0.0.3",
    author="SheiUn",
    author_email="develop@sheiun.me",
    description="A third-party Python API of Plurk Dice Emojis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Plurk-Project/plurk-dice",
    packages=find_packages(),
    install_requires=["requests"],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
