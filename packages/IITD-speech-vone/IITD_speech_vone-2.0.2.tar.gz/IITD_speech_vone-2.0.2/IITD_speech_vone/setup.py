from distutils.core import setup
from setuptools import find_packages

setup(
    # Application name:
    name = "IITD_speech_vone",

    # Version number (initial):
    version = "2.0.1",

    # Application author details:
    author= "Anshu Bansal, Jayanth, Abhishek, Prashit",
    author_email = "abhishekburnwal2@gmail.com",

    # Packages
    packages = find_packages(),

    # Include additional files into the package
    include_package_data = True,

    # Details
    url="http://pypi.python.org/pypi/IITD_speech_vone_v101/",
    # url="https://github.com/javatechy/dokr",
    #
    # license="LICENSE.txt",
    description = "Useful speech recognition and transcription related library for Indian languages.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
		"pydub",
		"numpy",
		"sklearn",
		"soundfile",
		"pyAudioAnalysis",
		"statistics",
    ],
    classifiers=[
         "Programming Language :: Python :: 3",
        #  "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
