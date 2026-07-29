"""Add owner_id column in Heroes table

Revision ID: a1d97dc22ca5
Revises: 
Create Date: 2026-07-29 13:33:53.188449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1d97dc22ca5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(table_name='heroes', column=sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        constraint_name='fk_heroes_owner_id_players',
        source_table='heroes',
        referent_table='players',
        local_cols=['owner_id'],
        remote_cols=['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_heroes_owner_id_players', table_name='heroes', type_='foreignkey')
    op.drop_column(table_name='heroes', column_name='owner_id')
