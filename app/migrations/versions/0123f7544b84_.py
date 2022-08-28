"""empty message

Revision ID: 0123f7544b84
Revises: 8cf9e23eb9e6
Create Date: 2022-08-28 23:11:44.837197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0123f7544b84'
down_revision = '8cf9e23eb9e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('asset_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bookings', 'user', ['asset_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.drop_column('bookings', 'asset_id')
    # ### end Alembic commands ###
