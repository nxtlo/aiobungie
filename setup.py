from setuptools import setup
import sys
import aiobungie

if sys.version_info < (3, 6):
    raise RuntimeError("aiobungie reuires Python 3.6 or higher")

with open("./README.md", "r") as f:
    fs = f.read()

setup(
    name=aiobungie.__title__,
    version=aiobungie.__version__,
    description=aiobungie.__description__,
    long_description=fs,
    long_description_content_type="text/markdowb",
    url=aiobungie.__url__,
    author=aiobungie.__author__,
    license=aiobungie.__license__,
    python_requires='>=3.6.0',
    classifires=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natrual Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
