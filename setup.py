from setuptools import find_packages
from setuptools import setup


version = "19.1.4"

setup(
    name="Euphorie",
    version=version,
    description="Euphorie Risk Assessment tool",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="euphorie OiRA Interactive Risk Assessment",
    author="Wichert Akkerman and Syslab.com",
    author_email="info@syslab.com",
    url="https://euphorie.readthedocs.org/en/latest/",
    license="GPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "AccessControl",
        "alembic",
        "anytree",
        "Chameleon",
        "decorator",
        "ftw.upgrade",
        "lxml",
        "markdownify",
        "nltk",
        "NuPlone >= 4.0.1",
        "openpyxl",
        "path.py",
        "Plone >=6.0",
        "plone.api",
        "plone.app.imagecropping",
        "plone.app.redirector",
        "plone.app.vocabularies",
        "plone.app.z3cform",
        "plone.behavior",
        "plone.dexterity",
        "plone.formwidget.namedfile",
        "plone.memoize",
        "plone.namedfile",
        "plone.patternslib",
        "plonestatic.euphorie",
        "plone.uuid",
        "Products.membrane >=4.999999",
        "py-bcrypt",
        "python-docx",
        "repoze.formapi",
        "scikit-learn",
        "setuptools",
        "sh",
        "SQLAlchemy >=1.2.999999",
        "stoneagehtml",
        "user_agents",
        "weasyprint",
        "z3c.form",
        "z3c.saconfig",
        "zope.configuration",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
    ],
    tests_require=[
        "plone.app.testing",
    ],
    extras_require={
        "sphinx": [
            "Sphinx >=1.0",
            "repoze.sphinx.autointerface",
        ],
        "tests": [
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
