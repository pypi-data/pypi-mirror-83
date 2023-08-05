import setuptools
import os

setuptools.setup(
    name="qe",
    version="1.0.2",
    author="aeorxc",
    author_email="author@example.com",
    description="turn pandas dataframe into an excel instance on Windows",
    url="https://github.com/aeorxc/qe",
    project_urls={
        'Source': 'https://github.com/aeorxc/qe',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas', 'xlsxwriter'],
    python_requires='>=3.6',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

