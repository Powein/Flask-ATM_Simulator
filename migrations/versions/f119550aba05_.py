"""empty message

Revision ID: f119550aba05
Revises: 2cc633b4b8c3
Create Date: 2024-04-20 19:31:39.581724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f119550aba05'
down_revision = '2cc633b4b8c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('log_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('related_user_id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('log_model', schema=None) as batch_op:
        batch_op.drop_column('related_user_id')

    # ### end Alembic commands ###
