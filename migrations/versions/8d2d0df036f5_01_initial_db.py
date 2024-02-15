"""01_initial-db

Revision ID: 8d2d0df036f5
Revises: 
Create Date: 2024-02-15 13:42:11.008881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d2d0df036f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('work_center', sa.String(), nullable=False),
    sa.Column('squad', sa.String(), nullable=False),
    sa.Column('shift', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('nomenclature', sa.String(), nullable=False),
    sa.Column('code_ekn', sa.String(), nullable=False),
    sa.Column('work_center_id', sa.String(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('is_closed', sa.Boolean(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('batch_id', sa.Integer(), nullable=False),
    sa.Column('is_aggregated', sa.Boolean(), nullable=True),
    sa.Column('aggregated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('batches')
    # ### end Alembic commands ###
