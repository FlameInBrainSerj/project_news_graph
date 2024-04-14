"""'initial'

Revision ID: fa3bed8592fd
Revises:
Create Date: 2024-04-14 04:03:11.187443

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fa3bed8592fd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    if "reviews" not in tables:
        op.create_table(
            "reviews",
            sa.Column("user_id", sa.VARCHAR(255), nullable=False),
            sa.Column("score", sa.INTEGER, nullable=False),
            sa.Column("feedback", sa.TEXT, nullable=False),
            sa.PrimaryKeyConstraint("user_id"),
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("reviews")
    # ### end Alembic commands ###
