import os
from setuptools import setup

readme = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

version = '0.0.1'

setup(
    name='no-more-query-string',
    version=version,
    description="Remove unneccessary query-string from the URL given. Especially fbclid.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License"
    ],
    project_urls={
        "Bug Tracker": "https://github.com/EltonChou/no-more-query-string/issues",
        "Source Code": "https://github.com/EltonChou/no-more-query-string/",
        "Changelog": "https://github.com/EltonChou/no-more-query-string/blob/main/CHANGELOG.md",
    },
    python_requires=">=3.6, <4",
    keywords='fbclid, query strings, python',
    author='Elton H.Y. Chou',
    author_email='plscd748@gmail.com',
    url='https://github.com/EltonChou/no-more-query-string',
    packages=['no_more_qs'],
    license='MIT',
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
        "tld",
        "w3lib"
    ]
)
