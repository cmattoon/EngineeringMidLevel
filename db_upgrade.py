#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI as URI
from config import SQLALCHEMY_MIGRATE_REPO as REPO

v1 = api.db_version(URI, REPO)

api.upgrade(URI, REPO)

v2 = api.db_version(URI, REPO)
print("Upgraded DB from %s to %s" % (str(v1), str(v2)))
