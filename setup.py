"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib
import os

__version__ = '0.0.1'

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Set the project homepage
home = 'https://github.com/MrTJP/curseuploadpy'

# Load requirements from requirements.txt
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='curseuploadpy',
    version=__version__,
    description='Python library for uploading files to CurseForge',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=home,
    author='MrTJP',
    author_email='mrtjp@icloud.com',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        # Stating that we are platform independent:
        'Operating System :: OS Independent',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='curseforge, curseforge-upload, curseforge-upload-api, curseforge-api, curseforge-api-python',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=install_requires,
    package_data={},
    project_urls={
        'Bug Reports': f'{home}/issues',
        'Source': home,
    }
)