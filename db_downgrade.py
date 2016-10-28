#!flask/bin/python
"""Downgrades one DB version

To roll back one version:
    ./db_downgrade.py   
    ./db_downgrade.py -1

To roll back to version 5:
    ./db_downgrade 5
"""
import sys
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI as URI
from config import SQLALCHEMY_MIGRATE_REPO as REPO

if __name__ == '__main__':
    v1 = api.db_version(URI, REPO)

    try:
        target_version = sys.argv[1]

        if target_version.startswith('-'):
            target_version = v1 - 1

    except IndexError:
        target_version = v1 - 1

    print("Attempting to downgrade from %s to %s" %
          (str(v1), str(target_version)))

    api.downgrade(URI, REPO, target_version)

    v2 = api.db_version(URI, REPO)

    print("Downgraded DB from %s to %s" % (str(v1), str(v2)))
