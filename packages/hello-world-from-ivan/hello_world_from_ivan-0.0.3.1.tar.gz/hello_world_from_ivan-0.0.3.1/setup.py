from setuptools import setup
from os import path


############## Read long description from README.MD

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.MD'), encoding='utf-8') as f:
    long_description = f.read()

############# Setup package from source

setup(name='hello_world_from_ivan',
      version='0.0.3.1',
      description='Shows how to use setup.py',
      url='https://www.domain.com',
      author='Ivan Pavlov',
      license='GPLv3',
      packages=['hello_world'],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='tutorial',
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown'
)
