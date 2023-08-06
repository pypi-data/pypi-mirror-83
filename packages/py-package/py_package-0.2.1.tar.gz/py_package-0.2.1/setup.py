import setuptools
import re

with open(".github/pypi.md", "r") as fh:
    long_description = fh.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('py_package/__init__.py', 'r').read(),
    re.M).group(1)


setuptools.setup(
    name="py_package",
    version=version,
    author="Aahnik Daw",
    author_email="meet.aahnik@gmail.com",
    description="This is a template repository for creating python packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aahnik/py_package",
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    package_data={
        'py_package': ['resources/*']
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['py_package=py_package.command_line:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
