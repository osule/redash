"""give query case sensitive treatment in query hash

Revision ID: 9aafdb8de771
Revises: e5c7a4e2df4d
Create Date: 2019-10-16 07:40:38.221138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table

from redash.utils import gen_query_hash

# revision identifiers, used by Alembic.
revision = '9aafdb8de771'
down_revision = 'e5c7a4e2df4d'
branch_labels = None
depends_on = None


def change_query_hash(conn, table, query_text_to):
    for record in conn.execute(table.select()):
        query_text = query_text_to(record.query)
        conn.execute(
            table
            .update()
            .where(table.c.id == record.id)
            .values(query_hash=gen_query_hash(query_text)))


def upgrade():
    queries = table(
        'queries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('query', sa.Text),
        sa.Column('query_hash', sa.String(length=10)))

    conn = op.get_bind()
    change_query_hash(conn, queries, query_text_to=str)


def downgrade():
    queries = table(
        'queries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('query', sa.Text),
        sa.Column('query_hash', sa.String(length=10)))

    conn = op.get_bind()
    change_query_hash(conn, queries, query_text_to=str.lower)
