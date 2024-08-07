"""adding abac

Revision ID: e55b6bd6ba9b
Revises: 8a3aa220a172
Create Date: 2024-07-14 20:22:01.628821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e55b6bd6ba9b'
down_revision: Union[str, None] = '8a3aa220a172'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resource_access',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('resource_type', sa.Enum('User', 'DataSource', 'Metadata', name='resourcetype'), nullable=True),
    sa.Column('permission', sa.Enum('Read', 'Write', name='permissiontype'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['data_source.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('data_source', sa.Column('tenant_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('tenant_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'tenant_id')
    op.drop_column('data_source', 'tenant_id')
    op.drop_table('resource_access')
    # ### end Alembic commands ###
