from setuptools import find_packages
from setuptools import setup


version = "16.2.4"

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
        "Framework :: Plone :: 6.0",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    python_requires="~= 3.8",
    install_requires=[
        "Plone >=5.2",
        "AccessControl",
        "Products.membrane >=4.999999",
        "SQLAlchemy >=1.2.999999",
        "alembic",
        "anytree",
        "decorator",
        "py-bcrypt",
        "ftw.upgrade",
        "lxml",
        "markdownify",
        "nltk",
        "path.py",
        "plone.app.imagecropping",
        "plone.app.redirector",
        "plone.app.vocabularies",
        "plone.app.z3cform",
        "plone.behavior",
        "plone.dexterity",
        "plone.formwidget.namedfile",
        "plone.memoize",
        "plone.namedfile",
        "plone.api",
        "python-docx",
        "repoze.formapi",
        "setuptools",
        "scikit-learn",
        "sh",
        "stoneagehtml",
        "user_agents",
        "weasyprint",
        "z3c.form",
        "z3c.schema",
        "z3c.saconfig",
        "zope.configuration",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
        "NuPlone >=2.1.4",
        "plone.uuid",
        "openpyxl",
        "Chameleon",
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
