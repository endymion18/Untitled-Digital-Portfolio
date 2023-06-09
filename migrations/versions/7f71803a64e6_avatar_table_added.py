"""Avatar table added

Revision ID: 7f71803a64e6
Revises: 7ed112062a84
Create Date: 2023-06-06 01:31:08.421791

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7f71803a64e6'
down_revision = '7ed112062a84'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('avatar',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('path', sa.String(length=500), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_column('user_info', 'avatar')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('avatar', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_table('avatar')
    # ### end Alembic commands ###
