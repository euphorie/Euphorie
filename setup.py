from setuptools import find_packages
from setuptools import setup


version = '10.0.3'

setup(
    name="Euphorie",
    version=version,
    description="Euphorie Risk Assessment tool",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="euphorie OiRA Interactive Risk Assessment",
    author="Wichert Akkerman and Syslab.com",
    author_email="info@syslab.com",
    url="http://euphorie.readthedocs.org/en/latest/",
    license="GPL",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Plone >=5.1.0",
        "Zope2 >=2.13.19",
        'AccessControl >= 3.0',
        'Products.membrane >=2.1.3',
        "SQLAlchemy >=0.5.2",
        "anytree",
        "decorator",
        "py-bcrypt",
        "five.grok",
        "htmllaundry [z3cform] >=1.1dev-r11183",
        "lxml",
        "plone.app.dexterity [grok, relations]",
        "plone.app.folder",
        "plone.app.imaging",
        "plone.app.redirector >= 1.0.12dev-r27477",
        "plone.app.vocabularies",
        "plone.app.z3cform",
        "plone.behavior >=1.0b4",
        "plone.dexterity >=1.0b6",
        "plone.directives.dexterity",
        "plone.directives.form",
        "plone.formwidget.namedfile",
        "plone.memoize",
        "plone.namedfile[blobs]",
        "plone.api",
        "repoze.formapi >=0.4.2",
        "setuptools",
        "simplejson",
        "z3c.form >= 2.1.0",
        "z3c.schema",
        "z3c.saconfig",
        "zope.configuration >= 3.6",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
        "NuPlone >=1.4.0",
        "plone.uuid",
        "pyrtf-ng",
        "z3c.appconfig >=1.0",
        "openpyxl",
        "Chameleon >=2.12",
    ],
    tests_require=[
        "collective.testcaselayer >=1.6",
        "Products.PloneTestCase >=0.9.9",
        'mock',
    ],
    extras_require={
        "sphinx": [
            "Sphinx >=1.0",
            "repoze.sphinx.autointerface",
        ],
        "tests": [
            "plone.app.testing",
            "collective.testcaselayer",
            "Products.PloneTestCase >=0.9.9",
            "mock",
        ],
    },
    entry_points="""
      [z3c.autoinclude]
      target = plone

      [zopectl.command]
      initdb = euphorie.deployment.commands.initdb:main
      xmlimport = euphorie.deployment.commands.xmlimport:main

      [console_scripts]
      upgradedb = euphorie.deployment.commands.upgradedb:main
      """,
)
