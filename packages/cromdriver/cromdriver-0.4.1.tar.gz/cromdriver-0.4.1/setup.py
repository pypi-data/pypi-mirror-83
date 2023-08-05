import setuptools
import cromdriver

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cromdriver',
    version=cromdriver.__version__,
    author='gokender',
    author_email='gauthier.chaty+pypi@outlook.com',
    description='Auto downloader for chromedrivers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Gokender/cromdriver',
    packages=setuptools.find_packages(include=['cromdriver']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['requests', 'appdirs'],
    test_suite='tests',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cromdriver=cromdriver.cli',
        ],
    }
)