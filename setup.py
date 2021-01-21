from setuptools import find_packages
from setuptools import setup


version = "11.6.4.dev0"

setup(
    name="Euphorie",
    version=version,
    description="Euphorie Risk Assessment tool",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
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
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Plone >=5.1.999999",
        "Zope2 >=3.999999",
        "AccessControl >= 3.0",
        "Products.membrane >=4.999999",
        "SQLAlchemy >=1.2.999999",
        "alembic",
        "anytree",
        "decorator",
        "py-bcrypt",
        "ftw.upgrade",
        "htmllaundry [z3cform]",
        "lxml",
        "plone.app.dexterity [relations]",
        "plone.app.folder",
        "plone.app.imagecropping",
        "plone.app.redirector",
        "plone.app.vocabularies",
        "plone.app.z3cform",
        "plone.behavior >=1.0b4",
        "plone.dexterity >=1.0b6",
        "plone.formwidget.namedfile",
        "plone.memoize",
        "plone.namedfile[blobs]",
        "plone.api",
        "python-docx",
        "repoze.formapi",
        "setuptools",
        "z3c.form",
        "z3c.schema",
        "z3c.saconfig",
        "zope.configuration",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
        "NuPlone >=1.999999",
        "plone.uuid",
        "pyrtf-ng",
        "openpyxl",
        "Chameleon",
    ],
    tests_require=[
        "mock",
        "plone.app.testing",
    ],
    extras_require={
        "sphinx": [
            "Sphinx >=1.0",
            "repoze.sphinx.autointerface",
        ],
        "tests": [
            "mock;python_version<'3'",
            "plone.app.testing",
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
