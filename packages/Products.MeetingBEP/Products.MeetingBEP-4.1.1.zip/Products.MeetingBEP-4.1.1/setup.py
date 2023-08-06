from setuptools import setup, find_packages
import os

version = '4.1.1'

setup(name='Products.MeetingBEP',
      version=version,
      description="Official meetings management for BEP (PloneMeeting extension profile)",
      long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
      classifiers=[
          "Development Status :: 6 - Mature",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Office/Business",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://www.imio.be/produits/gestion-des-deliberations',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=['unittest2',
                'zope.testing',
                'plone.testing',
                'plone.app.testing',
                'plone.app.robotframework',
                'Products.CMFPlacefulWorkflow',
                'zope.testing',
                'Products.PloneTestCase',
                'Products.PloneMeeting[test]'],
          templates=['Genshi', ]),
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'Pillow',
          'Products.PloneMeeting',
          'Products.MeetingCommunes'],
      entry_points={},
      )
