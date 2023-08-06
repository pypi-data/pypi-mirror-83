from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='patrick-helloworld',
    version='0.0.2',
    description='Say Hello!',
    py_modules=['helloworld'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "blessings ~= 1.7", # Change this to the packages that are required for your setup (helpful tip, look into pip freeze)
    ],
    url="http://patrickold.me",
    author="Patrick Old",
    author_email="patrickold96@gmail.com",
)