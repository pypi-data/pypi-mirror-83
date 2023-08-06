from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'unicatdb',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='All rights reserved',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python library for accessing API of the UniCatDB - Universal Catalog Database for biological findings.',   # Give a short description about your library
  author = 'Ondřej Doktor',                   # Type in your name
  author_email = 'doktoo00@jcu.cz',      # Type in your E-Mail
  url = 'https://unicatdb.org',   # Provide either the link to your github or to your website
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['UniCatDB', 'API', 'Universal Catalog Database'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'certifi',
    'six',
    'python_dateutil',
    'setuptools',
    'urllib3'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: Other/Proprietary License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
  long_description_content_type="text/markdown",
  long_description=long_description,
)