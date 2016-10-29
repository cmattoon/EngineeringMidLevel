from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client = Table('client', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
)

feature_request = Table('feature_request', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=255)),
    Column('description', TEXT),
    Column('client_id', INTEGER),
    Column('product_area_id', INTEGER),
    Column('client_priority', INTEGER),
    Column('date_entered', DATETIME),
    Column('target_date', DATETIME),
    Column('ticket_url', TEXT),
)

feature_request = Table('feature_request', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('title', String(length=255)),
    Column('description', Text),
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
    post_meta.tables['client'].create()
    pre_meta.tables['feature_request'].columns['client_id'].drop()
    pre_meta.tables['feature_request'].columns['product_area_id'].drop()
    post_meta.tables['feature_request'].columns['product_area'].create()
    post_meta.tables['feature_request'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client'].drop()
    pre_meta.tables['feature_request'].columns['client_id'].create()
    pre_meta.tables['feature_request'].columns['product_area_id'].create()
    post_meta.tables['feature_request'].columns['product_area'].drop()
    post_meta.tables['feature_request'].columns['user_id'].drop()
