import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lit2go",
    version="0.0.1",
    author="Fiaz Sami",
    description="Literacy2 CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://literacy2.com",
    packages=['literacy2',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': ['lit2go=literacy2.lit2go:main']
    },
    python_requires='>=3.6',
)
