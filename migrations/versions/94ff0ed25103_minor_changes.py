"""Minor changes

Revision ID: 94ff0ed25103
Revises: dc8adad29609
Create Date: 2023-06-08 13:25:19.494363

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '94ff0ed25103'
down_revision = 'dc8adad29609'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('name', sa.String(length=100), nullable=False))
    op.drop_column('project', 'project_name')
    op.drop_column('user_info', 'favourite')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('favourite', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('project', sa.Column('project_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('project', 'name')
    # ### end Alembic commands ###