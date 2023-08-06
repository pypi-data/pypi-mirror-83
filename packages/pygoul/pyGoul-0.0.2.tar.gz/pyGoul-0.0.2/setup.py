import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'pyGoul',
    version="0.0.2",
  description = 'A goul library',
  author = 'Goulc\'hen',
  author_email = 'goulmeur@gmail.com',
  url = 'https://github.com/goulchen/PyGoul',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)