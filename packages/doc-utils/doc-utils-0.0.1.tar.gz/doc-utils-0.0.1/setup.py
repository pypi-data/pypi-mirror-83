import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doc-utils",
    version="0.0.1",
    author="Aleksandr Ader",
    author_email="info@ader-design.ee",
    description="Utilities for docx, xlsx and pdf froms templating",
    url="https://github.com/a-ader/doc-utils",
    packages=setuptools.find_packages(),
    install_requires=[
        'python-docx',
        'openpyxl',
        'pdfrw'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)