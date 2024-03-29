"""empty message

Revision ID: c53f6e45af2e
Revises: 
Create Date: 2018-04-22 13:38:34.463453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c53f6e45af2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('option_one', sa.String(), nullable=True),
    sa.Column('option_two', sa.String(), nullable=True),
    sa.Column('option_three', sa.String(), nullable=True),
    sa.Column('option_four', sa.String(), nullable=True),
    sa.Column('answer', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questions')
    # ### end Alembic commands ###
