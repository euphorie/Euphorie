"""Create the initial database structure.

This script creates the required tables in a SQL database. It must be run
using a fully initialized environment::

    $ bin/instance run src/Euphorie/dbsetup.py

"""

from euphorie.client import model
from z3c.saconfig import Session

model.metadata.create_all(Session.bind, checkfirst=True)

