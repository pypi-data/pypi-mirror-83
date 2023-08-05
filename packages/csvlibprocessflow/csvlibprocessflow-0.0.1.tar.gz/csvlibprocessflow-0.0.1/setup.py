from setuptools import setup, find_packages
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='csvlibprocessflow',
  version='0.0.1',
  description='creating xls from user input in databricks',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  # the URL of your package's home page e.g. github link
  author='Bhavsik',
  author_email='bbhadarka@infosenseglobal.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='', # used when people are searching for a module, keywords separated with a space
  package_dir={' ':'csvlibpy'},
  install_requires=['xlrd','xlwt','xlutils'] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)