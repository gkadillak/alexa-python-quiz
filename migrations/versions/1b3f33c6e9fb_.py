"""empty message

Revision ID: 1b3f33c6e9fb
Revises: f87bffe13c7a
Create Date: 2018-04-30 22:40:39.244004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b3f33c6e9fb'
down_revision = 'f87bffe13c7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('games', sa.Column('user_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'games', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_column('games', 'user_id')
    op.drop_table('users')
    # ### end Alembic commands ###