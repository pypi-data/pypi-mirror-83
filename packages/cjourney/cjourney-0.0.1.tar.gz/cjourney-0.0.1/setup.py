'''
Date: 2020-10-26 11:20:05
LastEditors: ryan.ren
LastEditTime: 2020-10-26 14:13:42
Description: 
'''
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cjourney",
    version="0.0.1",
    author="ryanren",
    author_email="strrenyumm@gmail.com",
    description="cjourney is a moudle to analyse customer journey in app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renyumm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['colorsys']
)
