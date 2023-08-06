import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='HyperclassifierSearch',
      version='1.0',
      description='Train multiple classifiers/pipelines',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['HyperclassifierSearch'],
      author='Jan Henner',
      author_email='mail@janhenner.de',
      url="https://github.com/dabln/HyperclassifierSearch",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.0',
      zip_safe=False)
