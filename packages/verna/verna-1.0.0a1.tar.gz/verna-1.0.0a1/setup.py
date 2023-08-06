import pathlib
import setuptools

long_description = pathlib.Path("README.md").read_text()

setuptools.setup(
    name="verna",
    version="1.0.0-alpha1",
    author="Julin S",
    author_email="",
    description="A simple module to handle colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ju-sh/verna",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        'Changelog': 'https://github.com/ju-sh/verna/blob/master/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/ju-sh/verna/issues',
    },
    install_requires=[],
    python_requires='>=3.6',
)
