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
  version='0.0.1',
  description='A very basic calculator',
  long_description= long_description + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Anzony Quispe',
  author_email='anzony.quispe@gmail.com',
  long_description_content_type="text/markdown",
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['scipy'] 
)