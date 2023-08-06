#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='xingyunlib',
    version="1.2.20201024",
    description=(
        '星光☆学而思专用库'
    ),
    long_description=open('README.md',encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='严子昱',
    author_email='yanziyu252625@qq.com',
    maintainer='严子昱',
    maintainer_email='yanziyu252625@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests',"pygame","zmail","pillow","numpy"#,"alsolib"
    ]
)
#
# 9abe5372d54460c07f202585e7da2cf53cf016bc884542732e07a3544275