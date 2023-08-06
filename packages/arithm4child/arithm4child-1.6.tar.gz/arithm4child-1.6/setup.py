# -*- coding: UTF-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='arithm4child',
    version='1.6',
    packages=['arithm4child'],
    author="Bai Wensimi",
    author_email="baiwensimi@gmail.com",
    description="arithmetic quiz for children",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baiwensimi/arithm4child",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'douyin_image=douyin_image:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.6',
)
