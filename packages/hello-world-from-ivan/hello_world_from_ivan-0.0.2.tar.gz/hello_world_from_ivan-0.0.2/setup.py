from setuptools import setup

setup(name='hello_world_from_ivan',
      version='0.0.2',
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
      include_package_data = True,
)
