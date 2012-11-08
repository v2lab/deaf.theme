from setuptools import setup, find_packages
import os

version = '1.0dev'

setup(name='deaf.theme',
      version=version,
      description="An installable Plone 4 theme for Deaf",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Wim Boucquaert - wimbou',
      author_email='wim@infrae.com',
      url='https://svn.v2.nl/plone/deaf.theme/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['deaf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.fileimage',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
