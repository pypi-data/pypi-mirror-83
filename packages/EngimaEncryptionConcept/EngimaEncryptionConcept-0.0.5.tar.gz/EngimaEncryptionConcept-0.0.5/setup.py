from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
with open('README.md') as f:
    long_description = f.read()

setup(
  name='EngimaEncryptionConcept',
  version='0.0.5',
  description='Enigma Machine Encryption',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',
  author='Youwei Zhen',
  author_email='anthony20151128@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='encryption',
  packages=find_packages(),
  install_requires=['']
)
