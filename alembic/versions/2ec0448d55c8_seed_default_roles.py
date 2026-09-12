"""seed default roles

Revision ID: 2ec0448d55c8
Revises: 19c960f6d088
Create Date: 2026-09-12 13:34:08.025185

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2ec0448d55c8"
down_revision: Union[str, Sequence[str], None] = "19c960f6d088"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert default roles if they do not already exist."""

    roles_table = sa.table(
        "roles",
        sa.column("id", sa.UUID()),
        sa.column("name", sa.String()),
    )

    connection = op.get_bind()

    existing_roles = connection.execute(sa.select(roles_table.c.name)).scalars().all()

    roles_to_insert = []

    if "regular" not in existing_roles:
        roles_to_insert.append(
            {
                "id": uuid4(),
                "name": "regular",
            }
        )

    if "admin" not in existing_roles:
        roles_to_insert.append(
            {
                "id": uuid4(),
                "name": "admin",
            }
        )

    if "dispatcher" not in existing_roles:
        roles_to_insert.append(
            {
                "id": uuid4(),
                "name": "dispatcher",
            }
        )

    if roles_to_insert:
        op.bulk_insert(
            roles_table,
            roles_to_insert,
        )


def downgrade() -> None:
    """Remove the default roles if they are not referenced."""

    connection = op.get_bind()

    connection.execute(sa.text("""
            DELETE FROM roles
            WHERE name IN ('regular', 'admin', 'dispatcher')
            """))
