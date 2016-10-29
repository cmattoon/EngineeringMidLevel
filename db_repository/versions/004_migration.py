from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
feature_request = Table('feature_request', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('title', String(length=255)),
    Column('description', Text),
    Column('client_id', Integer),
    Column('product_area', String),
    Column('client_priority', Integer),
    Column('date_entered', DateTime),
    Column('target_date', DateTime),
    Column('ticket_url', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feature_request'].columns['client_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feature_request'].columns['client_id'].drop()
