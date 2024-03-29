"""empty message

Revision ID: b27290eedad9
Revises: 1b3f33c6e9fb
Create Date: 2018-07-13 22:52:48.180161

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b27290eedad9'
down_revision = '1b3f33c6e9fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('asked_questions', postgresql.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'asked_questions')
    # ### end Alembic commands ###
