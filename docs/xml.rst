XML survey format
=================

Euphorie supports import and exporting of surveys via a simple `XML
<http://en.wikipedia.org/wiki/XML>`_ format. The document used is similar to the
structure of a survey as it appears in an Euphorie site. This chapter assumes
that you are already familiar with the basic survey structure.

The current XML format is 1.0 and uses an XML namespace of
``http://xml.simplon.biz/euphorie/survey/1.0``.

.. note::

    It is mandatory to declare the XML namespace in your file. Without the
    namespace Euphorie will not correctly import your data.


sector element
--------------

The root of the XML file is the `sector` element.

.. table:: Allowed elements in ``sector``

   +--------------+-----------+-------------------------------------------+
   | Element      | Mandatory | Description                               |
   +==============+===========+===========================================+
   | ``title``    | No        | Title for the sector organisation         |
   +--------------+-----------+-------------------------------------------+
   | ``account``  | No        | Account login information for this sector |
   +--------------+-----------+-------------------------------------------+
   | ``contact``  | No        | Contact information for the sector        |
   +--------------+-----------+-------------------------------------------+
   | ``logo``     | No        | Inline image with sector logo             |
   +--------------+-----------+-------------------------------------------+
   | ``survey``   | Yes       | Survey                                    |
   +--------------+-----------+-------------------------------------------+

The ``account``, ``contact`` and ``logo`` elements are only used when a new
sector is created from an XML file. This option is only available to site
and country managers in Euphorie.

The ``contact`` element is a container supports optional ``name`` and ``email``
elements.

Example
~~~~~~~

.. code-block:: xml

   <sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
     <title>Information technology</title>
     <account login="coders" password="s3cr3t" />
     <contact>
       <name>Team lead</name>
       <email>leader@example.com</email>
     </contact>
     <survey>
       ...
     </survey>
   </sector>


survey element
--------------

The ``survey`` element defines a survey. It contains all the profile questions,
modules, risks, etc. that make up a survey.

.. table:: Allowed elements in ``survey``

   +-------------------------+-----------+--------------------------------------+
   | Element                 | Mandatory | Description                          |
   +=========================+===========+======================================+
   | ``title``               | Yes       | Title of this survey                 |
   +-------------------------+-----------+--------------------------------------+
   | ``classification-code`` | No        | NACE-based classification code       |
   +-------------------------+-----------+--------------------------------------+
   | ``language``            | Yes       | Language used in the survey          |
   +-------------------------+-----------+--------------------------------------+
   | ``evaluation-optional`` | No        | Inline image with sector logo        |
   +-------------------------+-----------+--------------------------------------+
   | ``profile-question``    | No        | A profile question (can be repeated) |
   +-------------------------+-----------+--------------------------------------+
   | ``module``              | No        | A module (can be repeated)           |
   +-------------------------+-----------+--------------------------------------+

The language must be specified using the ISO 3166 country code, possibly extended with
a two letter alpha code to indicate the region. See the "`Language tags in HTML and XML
<http://www.w3.org/International/articles/language-tags/>`_" document from W3C for more
information on language codes.

The ``evaluation-optional`` element is a boolean and must contain either ``true`` or
``false``.

Example
~~~~~~~

.. code-block:: xml

   <survey>
     <title>Software development</title>
     <classification-code>A.1.2.3</classification-code>
     <language>en</language>
     <evaluation-optional>true</evaluation-optional>
     <profile-question>
       ...
     </profile-question>
     <module>
       ...
     </module>
     <module>
       ...
     </module>
   </survey>


profile-question element
------------------------

The ``profile-question`` element is used to create a profile question. It is
very similar to the ``module`` element.

.. table:: Allowed elements in ``profile-question``

   +-------------------------+-----------+-------------------------------------------+
   | Element                 | Mandatory | Description                               |
   +=========================+===========+===========================================+
   | ``title``               | Yes       | Title of this profile question            |
   +-------------------------+-----------+-------------------------------------------+
   | ``description``         | No        | Description (HTML)                        |
   +-------------------------+-----------+-------------------------------------------+
   | ``question``            | Yes       | Question asked to determine use of profile|
   |                         |           | section in survey.                        |
   +-------------------------+-----------+-------------------------------------------+
   | ``module``              | No        | A module (can be repeated)                |
   +-------------------------+-----------+-------------------------------------------+
   | ``risk``                | No        | A risk (can be repeated)                  |
   +-------------------------+-----------+-------------------------------------------+

HTML tags used in the description must be properly escaped or wrapped in a CDATA block.

A profile question must contain either modules or risks; it is an error to use both
``module`` and ``risk`` elements as direct children of a ``profile-question``. It is
of course allowed use modules which themselves contain risk elements.

Example
~~~~~~~

.. code-block:: xml

   <profile-question>
     <title>Mobile access</title>
     <question>Do your employees work remotely?</question>
     <description>&lt;p&gt;Working out of the office can introduce many
       new risks that may not be under your direct control.&lt;/p&gt;
     </description>
     <module>
        ...
     </module>
     <module>
        ...
     </module>
   </profile-question>


module element
--------------

A module is used to group a number of risks that belong together. This element
is very similar to the ``profile-question`` element.

.. table:: Allowed elements in ``module``

   +-------------------------+-----------+-------------------------------------------+
   | Element                 | Mandatory | Description                               |
   +=========================+===========+===========================================+
   | ``title``               | Yes       | Title of this profile question            |
   +-------------------------+-----------+-------------------------------------------+
   | ``description``         | No        | Description (HTML)                        |
   +-------------------------+-----------+-------------------------------------------+
   | ``question``            | Yes/No    | Question asked to determine if module     |
   |                         |           | should be skipped                         |
   +-------------------------+-----------+-------------------------------------------+
   | ``solution-direction``  | Yes       | Solution suggestions for action plan     e|
   |                         |           | phase (HTML)                              |
   +-------------------------+-----------+-------------------------------------------+
   | ``module``              | No        | A module (can be repeated)                |
   +-------------------------+-----------+-------------------------------------------+
   | ``risk``                | No        | A risk (can be repeated)                  |
   +-------------------------+-----------+-------------------------------------------+
   | ``image``               | No        | Image for this module                     |
   +-------------------------+-----------+-------------------------------------------+

If a module is optional this can be indicated by setting the ``optional`` attribute
to ``true``. If this attribute is ``false`` or not present a module is assumed to be
mandatory. If a module is optional the ``question`` element is mandatory.

HTML tags used in the description and solution direction must be properly
escaped or wrapped in a CDATA block.

A module must contain either modules or risks; it is an error to use both
``module`` and ``risk`` elements as direct children of a ``module``.
It is of course allowed use modules which themselves contain risk elements.

See the :ref:`image <xml-image-element>` element for how to specify images.


Example
~~~~~~~

.. code-block:: xml

   <module optional="yes">
     <title>Laptops</title>
     <question>Do your employees use laptops?</question>
     <description>
       &lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;
     </description>
     <risk>
       ...
     </risk>
     <risk>
       ...
     </risk>
   </module>


risk element
-------------

The risk element is the workhorse of a survey: it defines a single risk.

.. table:: Allowed elements in ``risk``

   +-------------------------+-----------+-----------------------------------+
   | Element                 | Mandatory | Description                       |
   +=========================+===========+===================================+
   | ``title``               | Yes       | Title of this profile question    |
   +-------------------------+-----------+-----------------------------------+
   | ``problem-description`` | Yes       | Problem description shown if risk |
   |                         |           | is present (HTML)                 |
   +-------------------------+-----------+-----------------------------------+
   | ``description``         | Yes       | Description (HTML)                |
   +-------------------------+-----------+-----------------------------------+
   | ``legal-reference``     | No        | Legal and policy references (HTML)|
   +-------------------------+-----------+-----------------------------------+
   | ``evaluation-method``   | Yes/No    | Risk evaluation method            |
   +-------------------------+-----------+-----------------------------------+
   | ``solutions``           | No        | Container for standard solutions  |
   +-------------------------+-----------+-----------------------------------+
   | ``image``               | No        | Key image for this risk           |
   +-------------------------+-----------+-----------------------------------+

The type of risk is identified with a mandatory ``type`` attribute. This can be
set to ``risk``, ``policy`` or ``top5``. For policy and top-5 risks the 
``evaluation-method`` and ``default-*`` are not used.

For risks of type ``risk`` the ``evaluation-method`` method element must be
present and set to ``calculated`` or ``direct``. Default values for the evaluation
method can be set via attributes. For risks with a calculated evaluation the
attributes are:

* ``default-probability``: one of ``small``, ``medium`` or ``large``
* ``default-frequency``: one of ``almost-never``, ``regular`` or ``constant``
* ``default-effect``: one of ``weak``, ``significant`` or ``high``

The attributes for risks with a direct evaluation method are:

* ``default-priority``: one of ``low``, ``medium`` or ``high``

Standard solutions for a risk can be provided in a ``solutions`` container.

Up to four images for a risk can be defined by using :ref:`image
<xml-image-element>` element. 


Example
~~~~~~~

.. code-block:: xml

   <risk type="risk">
     <title>Are your desks at the right height?</title>
     <problem-description>
       &lt;p&gt;Not all desks have the correct height.&lt;/p&gt;
     </problem-description>
     <description>
       &lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;
     </description>
     <evaluation-method default-probability="small" default-frequency="regular"
        default-effect="high">calculated</evaluation-method>
     <solutions>
       <solution> ... </solution>
     </solutions>
   </risk>


solution element
----------------

Standard solutions for a risk are defined using the ``solution`` element

.. table:: Allowed elements in ``solution``

   +-------------------------+-----------+-------------------------------+
   | Element                 | Mandatory | Description                   |
   +=========================+===========+===============================+
   | ``description``         | Yes       | Description                   |
   +-------------------------+-----------+-------------------------------+
   | ``action-plan``         | No        | Text for the action plan      |
   +-------------------------+-----------+-------------------------------+
   | ``prevention-plan``     | No        | Text for the prevention plan  |
   +-------------------------+-----------+-------------------------------+
   | ``requirements``        | No        | Text for the requirements     |
   +-------------------------+-----------+-------------------------------+


Example
~~~~~~~

.. code-block:: xml

   <solution>
     <description>Use height-adjustable desks</description>
     <action-plan>Order height-adjustable desks for desk workers.</action-plan>
   </solution>


.. _xml-image-element:

image element
-------------

The ``image`` element is used in ``module`` and ``risk`` elements to add
extra images. The element has three optional attributes:

``caption``
  The caption for the image.

``content-type``
  The MIME content type for the image. This is generally one of ``image/gif``,
  ``image/png`` or ``image/jpeg``.

``filename``
  The original filename for the image. If ``content-type`` is not provided
  this is used to guess the MIME type.


The contents of the element is the `Base64 <http://en.wikipedia.org/wiki/Base64>`_
encoded raw image data.

Example
~~~~~~~

.. code-block:: xml

   <image content-type="image/gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>


Full example
------------

The XML document below demonstrates all elements documented here.

.. code-block:: xml

   <?xml version="1.0"?>
   <sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
     <title>Information technology</title>
     <account login="coders" password="s3cr3t" />
     <contact>
       <name>Team lead</name>
       <email>leader@example.com</email>
     </contact>
     <survey>
       <title>Software development</title>
       <classification-code>A.1.2.3</classification-code>
       <language>en</language>
       <evaluation-optional>true</evaluation-optional>

       <profile-question>
         <title>Mobile access</title>
         <question>List your remote locations</question>
         <description>&lt;p&gt;Working out of the office can introduce many
           new risks that may not be under your direct control.&lt;/p&gt;
         </description>

         <module optional="yes">
           <title>Laptops</title>
           <question>Do your employees use laptops?</question>
           <description>
             &lt;p&gt;Laptops are very common in the modern workplace.&lt;/p&gt;
           </description>
         </module>
       </profile-question>

       <module>
         <title>Office environment</title>
         <image content-type="image/gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
         <description>
           &lt;p&gt;Your employees have to use office equipment every day.&t;/p&gt;
         </description>
         <solution-direction>
           &lt;p&gt;The standard health and safetety guidelines have
           many useful tips for improving the office environment.&lt;/p&gt;
         </solution-direction>

         <risk type="risk">
           <title>Are your desks at the right height?</title>
           <problem-description>
             &lt;p&gt;Not all desks have the correct height.&lt;/p&gt;
           </problem-description>
           <description>
             &lt;p&gt;The right height is important to prevent back problems.&lt;/p&gt;
           </description>
           <evaluation-method default-probability="small" default-frequency="regular"
              default-effect="high">calculated</evaluation-method>
           <solutions>
             <solution>
               <description>Use height-adjustable desks</description>
               <action-plan>Order height-adjustable desks for desk workers.</action-plan>
             </solution>
           </solutions>
         </risk>
       </module>
     </survey>
   </sector>

