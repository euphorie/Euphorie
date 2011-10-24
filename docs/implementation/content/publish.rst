Survey publication
==================

Publication of surveys is handled via the ``survey`` workflow. The workflow
itself is very simple: it manages the ``Delete objects`` permission, prevent
deletion of content in published surveys.

Extra behaviour is added via workflow event handlers:

* :py:func:`euphorie.content.surveygroup.handleSurveyPublish` updates the
  currently published survey instance variable on the survey group.
* :py:func:`euphorie.client.publish.handleSurveyPublish` copies the survey
  to the client.
* :py:func:`euphorie.content.survey.handleSurevyPublish` archives the
  published version.
