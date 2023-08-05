from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
  name = 'singhtools',
  packages = ['singhtools'],
  version = '0.1.1-alpha',
  license='gpl-3.0',
  description = 'Functions for estimating coverage of confidence structures',
  author = 'Alexander Wimbush',
  author_email = 'alexanderpwimbush@gmail.com', 
  url = 'https://github.com/Institute-for-Risk-and-Uncertainty/Singh-Tools',
  download_url = 'https://github.com/Institute-for-Risk-and-Uncertainty/Singh-Tools/archive/0.1.1-alpha.tar.gz', 
  keywords = ['confidence'], 
  install_requires=[
          'numpy'
      ],
)
