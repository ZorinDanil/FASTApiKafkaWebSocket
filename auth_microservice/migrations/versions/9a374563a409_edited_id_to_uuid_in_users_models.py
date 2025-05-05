"""Edited Id to UUID in users models

Revision ID: 9a374563a409
Revises: 729e8d6aeb90
Create Date: 2024-06-13 11:11:34.473724

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '9a374563a409'
down_revision = '729e8d6aeb90'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure the uuid-ossp extension is enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Step 1: Create a new UUID column
    op.add_column('user', sa.Column('uuid_id', UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()")))

    # Step 2: Populate the new column with UUID values
    op.execute('UPDATE "user" SET "uuid_id" = uuid_generate_v4()')

    # Step 3: Drop the old integer column
    op.drop_column('user', 'id')

    # Step 4: Rename the new UUID column to the original column name
    op.alter_column('user', 'uuid_id', new_column_name='id', nullable=False)


def downgrade():
    # Downgrade steps in case you need to revert the migration
    op.alter_column('user', 'id', new_column_name='uuid_id')
    op.add_column('user', sa.Column('id', sa.Integer(), nullable=False, autoincrement=True))
    op.drop_column('user', 'uuid_id')