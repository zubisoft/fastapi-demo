"""initial version

Revision ID: 21164d5d4bdb
Revises: 2dd66efd1572
Create Date: 2023-06-17 22:05:28.256456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21164d5d4bdb'
down_revision = '2dd66efd1572'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_datasets_permissions', sa.Column('type', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_datasets_permissions', 'type')
    # ### end Alembic commands ###