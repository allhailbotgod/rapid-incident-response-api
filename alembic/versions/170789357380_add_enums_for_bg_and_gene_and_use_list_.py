"""add enums for bg and gene and use list for conditions and allergies

Revision ID: 170789357380
Revises: 89b56736377a
Create Date: 2026-08-13 15:48:02.943973

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "170789357380"
down_revision: Union[str, Sequence[str], None] = "89b56736377a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


blood_group_enum = postgresql.ENUM(
    "Ap",
    "An",
    "Bp",
    "Bn",
    "ABp",
    "ABn",
    "Op",
    "On",
    name="blood_group_enum",
)

genotype_enum = postgresql.ENUM(
    "AA",
    "AS",
    "SS",
    "CC",
    "AC",
    "SC",
    name="genotype_enum",
)


def upgrade() -> None:
    """Upgrade schema."""

    blood_group_enum.create(op.get_bind(), checkfirst=True)
    genotype_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "medic_profile",
        "blood_group",
        existing_type=sa.VARCHAR(),
        type_=blood_group_enum,
        existing_nullable=True,
        postgresql_using="blood_group::blood_group_enum",
    )

    op.alter_column(
        "medic_profile",
        "genotype",
        existing_type=sa.VARCHAR(),
        type_=genotype_enum,
        existing_nullable=True,
        postgresql_using="genotype::genotype_enum",
    )

    op.alter_column(
        "medic_profile",
        "conditions",
        existing_type=sa.VARCHAR(),
        type_=postgresql.ARRAY(sa.String()),
        existing_nullable=True,
        postgresql_using="conditions::varchar[]",
    )

    op.alter_column(
        "medic_profile",
        "allergies",
        existing_type=sa.VARCHAR(),
        type_=postgresql.ARRAY(sa.String()),
        existing_nullable=True,
        postgresql_using="allergies::varchar[]",
    )

    op.drop_constraint(
        op.f("sos_phone_key"),
        "sos",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_sos_owner_phone",
        "sos",
        ["owner_id", "phone"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_sos_owner_phone",
        "sos",
        type_="unique",
    )

    op.create_unique_constraint(
        op.f("sos_phone_key"),
        "sos",
        ["phone"],
        postgresql_nulls_not_distinct=False,
    )

    op.alter_column(
        "medic_profile",
        "allergies",
        existing_type=postgresql.ARRAY(sa.String()),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="allergies::text",
    )

    op.alter_column(
        "medic_profile",
        "conditions",
        existing_type=postgresql.ARRAY(sa.String()),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="conditions::text",
    )

    op.alter_column(
        "medic_profile",
        "genotype",
        existing_type=genotype_enum,
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="genotype::text",
    )

    op.alter_column(
        "medic_profile",
        "blood_group",
        existing_type=blood_group_enum,
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="blood_group::text",
    )

    genotype_enum.drop(op.get_bind(), checkfirst=True)
    blood_group_enum.drop(op.get_bind(), checkfirst=True)
