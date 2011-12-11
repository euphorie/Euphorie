from setuptools import setup, find_packages

version = "3.0"

setup(name="Euphorie",
      version=version,
      description="Euphorie Risk Assessment tool",
      long_description=open("README.rst").read(),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords="",
      author="Wichert Akkerman",
      author_email="wichert@simplon.biz",
      url="http://packages.python.org/Euphorie/",
      license="GPL",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=[],
      paster_plugins=["Babel"],
      message_extractors = {"src": [
            ("euphorie/**.py",    "lingua_python", None),
            ("euphorie/**.pt",    "lingua_xml", None),
            ("euphorie/**.xml",   "lingua_xml", None),
            ]},
      include_package_data=True,
      zip_safe=False,
      setup_requires=[
        "setuptools_git > 0.3",
      ],
      install_requires=[
          "Plone >=4.0b1",
          "Zope2 >=2.12",
          "Products.CMFEditions >=2.0b8",
          "Products.PasswordResetTool >=2.0.3",
          "Products.membrane >=2.0dev-r87748",
          "collective.indexing >=1.1",
          "SQLAlchemy >=0.5.2",
          "decorator",
          "five.grok",
          "htmllaundry [z3cform] >=1.1dev-r11183",
          "lxml",
          "plone.app.dexterity",
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
          "repoze.formapi >=0.4.2",
          "setuptools",
          "simplejson",
          "z3c.form >= 2.1.0",
          "z3c.schema",
          "z3c.saconfig",
          "zope.app.schema",
          "zope.configuration >= 3.6",
          "zope.i18nmessageid",
          "zope.interface",
          "zope.schema",
          "NuPlone >=1.0.1",
          "plone.uuid",
          "pyrtf-ng",
          "z3c.appconfig >=1.0",
          "z3c.zrtresource == 1.2.0",
          "collective.zrtresource",
          "xlwt",
      ],
      tests_require = [
          "collective.testcaselayer",
          "Products.PloneTestCase >=0.9.9",
          'xlrd',
          ],
      extras_require = {
        "sphinx": [ "Sphinx >=1.0",
                    "repoze.sphinx.autointerface",
                  ],
        "tests" : [ "collective.testcaselayer",
                    "Products.PloneTestCase >=0.9.9",
                  ],
      },
      entry_points="""
      [z3c.autoinclude]
      target = plone

      [zopectl.command]
      initdb = euphorie.deployment.commands.initdb:main
      xmlimport = euphorie.deployment.commands.xmlimport:main
      """,
      )
