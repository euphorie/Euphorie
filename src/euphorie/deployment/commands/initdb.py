"""Create the initial database structure.

This script creates the required tables in a SQL database. It must be run
using a fully initialized environment using ``bin/instance``::

    $ bin/instance init-db
"""

from euphorie.client import model
from z3c.saconfig import Session


def main(app, args):
    model.metadata.create_all(Session.bind, checkfirst=True)


if __name__ == "__main__":
    main(app, ())  # noqa: F821
