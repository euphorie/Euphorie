Security
========

The four roles
--------------

Euphorie recognizes four different types of users: 

1. *Manage* users. These are commonly SYSLAB staff members. Managers have
   full access to the entire site.

2. *Country managers*. These are responsible for managing all sectors
   and country-specific content in the site. 

3. *Sector* users. Every sector is an account, and has full edit and publish
   access to itself and all data inside its sector.

4. *Anonymous* visitors. These have no access at all.

Each user type is registered as a *role* in Plone. The standard Plone roles
(Member, Reviewer, Reader, Editor and Contributor) are not used in Euphorie.
The *Sector* role is special: unlike the other roles it is managed as a
local role in a sector object.

Workflows
---------

Data inside a :obj:`euphorie.content.sector.Sector` object has no workflow;
all permissions are inherited from the `Sector` object itself. These are
managed via a single-state `sector` workflow.

This approach has two advantages: it centralizes the management of
permissions in a single location and workflow, and it makes it possible for
the online client to copy the survey to another location with diffferent
security settings, without having to update permissions inside the survey.

