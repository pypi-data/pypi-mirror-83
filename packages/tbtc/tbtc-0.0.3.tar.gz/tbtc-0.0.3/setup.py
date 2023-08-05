from os import path
from setuptools import (
    find_packages,
    setup,
)

# managing version
with open("VERSION", 'r') as f:
    VERSION = f.read()

# managing readme
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='tbtc',
    version=VERSION,
    py_modules=['tbtc'],
    description="""A python library to interact with the tbtc protocol.""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ankit Chiplunkar',
    author_email='ankitchiplunkar@gmail.com',
    url='https://github.com/ankitchiplunkar/tbtc.py',
    include_package_data=True,
    python_requires='>=3.6, <4',
    keywords=['ethereum', 'bitcoin'],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "web3==5.12.1",
        "riemann-tx==2.1.0",
        "pytest==6.0.2",
        "pytest-cov==2.8.1",
      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
