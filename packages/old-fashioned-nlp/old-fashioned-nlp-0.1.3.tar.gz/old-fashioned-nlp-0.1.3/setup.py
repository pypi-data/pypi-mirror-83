from pathlib import Path

import setuptools

setuptools.setup(
    name="old-fashioned-nlp",
    version="0.1.3",
    author="Chenghao Mou",
    author_email="mouchenghao@gmail.com",
    description="Sklearn base nlp models",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    py_modules=["old_fashioned_nlp"],
    url="https://github.com/sleeplessindebugging/old-fashioned-nlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "nlp",
        "pytest",
        "nltk",
        "scipy",
        "numpy",
        "loguru",
        "sklearn_crfsuite",
        "pandas",
        "regex",
        "rich",
        "scikit_learn",
    ],
)
