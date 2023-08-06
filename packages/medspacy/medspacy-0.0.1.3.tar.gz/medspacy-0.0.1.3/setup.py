from setuptools import setup, find_namespace_packages

# read the contents of the README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

def get_version():
    """Load the version from version.py, without importing it.
    This function assumes that the last line in the file contains a variable defining the
    version string with single quotes.
    """
    try:
        with open('medspacy/_version.py', 'r') as f:
            return f.read().split('\n')[0].split('=')[-1].replace('\'', '').strip()
    except IOError:
        raise IOError

setup(
    name="medspacy",
    version=get_version(),
    description="Library for clinical NLP with spaCy.",
    author="medSpaCy",
    author_email="medspacy.dev@gmail.com",
    packages=["medspacy"],
    install_requires=[
        "spacy>=2.3.0,<3.0.0",
        "nlp_preprocessor>=0.0.1",
        "PyRuSH>=1.0.3.5",
        "cycontext>=1.0.3.2",
        "clinical_sectionizer>=1.0.0.0",
        "target_matcher>=0.0.3",
        "nlp_postprocessor>=0.0.1",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"medspacy": ["../resources/*"]},
)
