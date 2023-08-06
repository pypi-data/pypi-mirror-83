"""Setup for the chocobo package."""

import setuptools


# read the contents of your README file
with open('README.md') as f:
    README = f.read()


setuptools.setup(
    author="Yuki Kakegawa",
    author_email="kake.19940627@gmail.com",
    name='pyhello',
    license="MIT",
    description='pyhello is a package that has a func that prints hello.',
    version='v0.0.1',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/StuffbyYuki/pyhello',
    packages=setuptools.find_packages(),
    #python_requires=">=3.5",
    #install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
