.. _workflow-survey:

Workflow
========

A user must go through several phases in a survey:

1. preparation: determine the *profile* of the organisation.
2. identification: determine which risks are present.
3. evaluation: prioritise all present risks.
4. action plan: provide the steps that will be taken to remove the risks
5. reporting: create reports with all collected information

Preparation
-----------

The preparation phase starts with an introduction screen explaining how the
survey tool works. If a sector provided extra introductory text that will
also be included. On this screen the user can also give a title to this
survey.

If the survey has any profile questions they will all be shown in a single
screen, allowing the user to indicate the structure of his organisation. If
no (non-deprecated) profile questions are found this option is skipped.


identification
---------------

During the identification phase all possible risks are shown, along with
any extra information such as legal references, images or explanatory text.
The user can indicate whether a risk is present, or not applicable. 

The identification phase starts with an introduction page with a brief
explanation and an option to print a list of all questions.


Evaluation
----------

During the evaluation phase the priority for possible risks, as determined
during the identification phase, is determined. There are three possible ways
to determine the priority:

* policy and top-5 risks will have priority, and do not need to be evaluated

* for risks with a *direct* priority the user can immediately select the
  priority

* for risks with a *calculated* priority the risk is determined using the
  effect, frequency and probability of a risk. The values of those three
  factors, as determined by the :obj:`euphorie.content.question.IQuestion`
  interface, are multiplied. If the resulting value is below or equal to 15
  the priority is low, if the value is between 15 and 50 (included) the
  priority is medium, and values above 50 indicate a high priority.

.. note::
   Changing the effect/frequency/probability factors here will reset the
   priority, even if the user has changed it during the action plan phase.

The evaluation phase may be skipped by users if allowed.


Action plan
-----------

During the action plan phase users indicate what they plan to do to prevent a
risk from (re)occurring. This can be done by selecting pre-defined solutions
(if known) or adding their own solutions.

A priority also has to be assigned. The default priority is determined by
the evaluation.

If a module has a *solution direction* text this will be shown when the user
enters a module. This makes the action plan phase the only phase during which a
module will present information to the user.

