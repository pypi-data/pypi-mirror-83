import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

    name="seleniumqt",
    version="0.2.7",
    author="lll",
    author_email="seleniumqt@gmail.com",
    description='seleniumqt trial information retriver',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/lll/seleniumqt',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)


# from setuptools import setup
#
# setup(name='seleniumqt',
#       version='0.2.5',
#       description='seleniumqt trial information retriver',
#       url='http://github.com/lll/seleniumqt',
#       author='lll',
#       author_email='seleniumqt@gmail.com',
#       license='MIT.seleniumqt',
#       packages=['seleniumqt'],
#       zip_safe=False)
