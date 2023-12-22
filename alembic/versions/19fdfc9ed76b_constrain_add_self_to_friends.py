"""constrain add self to friends

Revision ID: 19fdfc9ed76b
Revises: 5dfce381d016
Create Date: 2023-12-22 23:29:59.037184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19fdfc9ed76b'
down_revision: Union[str, None] = '5dfce381d016'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE friendships
        ADD CONSTRAINT restrict_add_yourself_friend
        CHECK (requester_id <> addressee_id);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE friendships
        DROP CONSTRAINT restrict_add_yourself_friend;
        """
    )
