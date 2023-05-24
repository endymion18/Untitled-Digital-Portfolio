"""Models added

Revision ID: ac96a6ec1d83
Revises: df4b792f7b01
Create Date: 2023-05-07 17:58:14.735243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac96a6ec1d83'
down_revision = 'df4b792f7b01'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('project_name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(length=1000), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('is_designer', sa.Boolean(), nullable=False),
    sa.Column('city', sa.String(length=150), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('avatar', sa.String(length=500), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('favourite', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favourite'], ['project.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('user_username_key', 'user', type_='unique')
    op.drop_column('user', 'first_name')
    op.drop_column('user', 'username')
    op.drop_column('user', 'last_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.drop_table('user_info')
    op.drop_table('image')
    op.drop_table('project')
    op.drop_table('tag')
    # ### end Alembic commands ###
