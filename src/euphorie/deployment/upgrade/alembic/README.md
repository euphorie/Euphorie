# Alembic tips and tricks

We use *alembic* to apply upgrades to the relational DB.
To do that we plug in *alembic* in the package requirements and have a customized
`env.py` that reads the `Euphorie` sqlalchemy configuration.

Alembic applies upgrades sequentially from one version (or revision) to the other.
By default alembic uses hexadecimal hashes to indicate the revision.
We can modify those upgrade steps to match the profile id.
The important thing is that the revision filename should match the pattern
`$REVISION_$WHATEVER.py`.


In the `env.py` we also instruct *alembic* to store the current
DB version in the table `euphorie_alembic_version`.

If you have a customer package that extends the `Euphorie` models,
they can similarly have an `env.py` that imports their models and store
the reached version in `$CLIENT_alembic_version`.

Given that *alembic* upgrade steps might have to deal with years old databases,
you might find that some upgrades will fail.
In that case you might want to consider to adapt the upgrade scripts
by modifying them manually.


## Generating the upgrade steps manually

You can autogenerate the upgrade steps automatically running the command:
```
./bin/alembic --config path/to/alembic.ini revision --autogenerate --rev-id $YOURPROFILEVERSION
```

The file `alembic.ini` should look contain the following values:
```
[alembic]
...
script_location = /$PATHTO/Euphorie/src/euphorie/deployment/upgrade/alembic
sqlalchemy.url = $DB_URI
...
```

If everything is properly configured you will find a new upgrade script:
```
/$PATHTO/Euphorie/src/euphorie/deployment/upgrade/alembic/versions/$YOURPROFILEVERSION_.py
```

Also check that the upgrade script is correct and that it will not harm your DB:
alembic stays a tool and might not do what you want.
For example if you rename a column the propose upgrade is just to remove the
old one and and a new one, without copying the data.

During development you might find yourself modifying the schema multiple times.
In that case try to merge the upgrade scripts in to one,
so that everything will be run cleanly on prodcution.

You might need to adjust the `euphorie_alembic_version.version_num`
value to make the upgrade script run again.


## Running the upgrade in the command line

```
./bin/alembic --config path/to/alembic.ini upgrade $YOURPROFILEVERSION
```

## Make Plone run the alembic upgrade

Just register a regular upgrade step that does something similar:
```
from euphorie.deployment.upgrade.utils import alembic_upgrade_to

def upgrade_to_new_profile(context):
    ...
    alembic_upgrade_to("$ALEMBIC_TARGET_REVISION")
    ...
```
