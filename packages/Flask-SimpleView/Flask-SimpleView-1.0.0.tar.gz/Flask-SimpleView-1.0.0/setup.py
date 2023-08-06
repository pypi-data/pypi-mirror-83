from setuptools import find_packages
from setuptools import setup
from pathlib import Path

__version__ = "1.0.0"

ROOT_DIR = Path(".")

with open(str(ROOT_DIR / "README.md")) as readme:
    long_description = readme.read()

setup(
    name="Flask-SimpleView",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask"],
    author="Jack Wardell",
    author_email="jack@wardell.xyz",
    url="https://github.com/jackwardell/Flask-SimpleView/",
    description="A very simple wrapper around flask's MethodView to ease the adding of views to the app or blueprints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    test_suite="tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords="flask",
    python_requires=">=3.5",
)
