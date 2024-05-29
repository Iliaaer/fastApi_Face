"""New Migration

Revision ID: d425bd5b0e58
Revises: a084f4be9030
Create Date: 2024-04-02 22:40:02.764644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd425bd5b0e58'
down_revision: Union[str, None] = 'a084f4be9030'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'student', 'group_students', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'student', type_='foreignkey')
    op.drop_column('student', 'group_id')
    # ### end Alembic commands ###
