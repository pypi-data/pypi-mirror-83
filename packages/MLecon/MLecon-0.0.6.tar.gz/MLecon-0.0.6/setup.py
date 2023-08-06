from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='MLecon',
  version='0.0.6',
  description='Package with all the functions necessary to follow Intro_Memo',
  long_description= long_description + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Anzony Quispe',
  author_email='anzony.quispe@gmail.com',
  long_description_content_type="text/markdown",
  license='MIT', 
  classifiers=classifiers,
  keywords='Machine Learning', 
  packages=find_packages(),
  install_requires=['scipy'] 
)