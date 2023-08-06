import re
import ast
from setuptools import setup, find_packages


setup(
    name="fxtest",
    url="https://github.com/shuaiwangNB/fxtest",
    author="shuaiwang",
    version="0.0.2",
    install_requires=[
        "py",
        "ansi2html",
        'pytest',
        "allure-pytest",
        "pytest-fxtest",
        "openpyxl",
        "pyyaml",
        "selenium",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts' :[
            'fxtest=fxtest.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)