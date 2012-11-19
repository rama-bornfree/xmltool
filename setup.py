from setuptools import setup, find_packages
import sys, os

# Hack to prevent TypeError: 'NoneType' object is not callable error
# on exit of python setup.py test
try:
    import multiprocessing
except ImportError:
    pass

version = '0.0'

setup(name='xml-tools/',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Aur\xc3\xa9lien Matouillot',
      author_email='a.matouillot@gmail.com',
      url='https://github.com/LeResKP/xml-tools',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml',
      ],
      test_suite = 'nose.collector',
      tests_require = [
          'nose',
          'BeautifulSoup',
          'strainer',
          'FormEncode',
          'tw2.core',
          'WebTest',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
