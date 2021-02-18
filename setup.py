from setuptools import setup
import sys

if sys.version_info < (3, 6):
    raise RuntimeError("aiobungie reuires Python 3.6 or higher")

with open("./README.md", "r", encoding='utf-8') as f:
    fs = f.read()

setup(
    name='aiobungie',
    description='An async wrapper for the bungie api',
    long_description=fs,
    version='0.1',
    long_description_content_type="text/markdown",
    url='https://github.com/nxtlo/aiobungie',
    author='nxtlo',
    license='MIT',
    install_requires=['httpx'],
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
