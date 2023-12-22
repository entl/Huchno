"""trigger accept friendship request

Revision ID: 5dfce381d016
Revises: 49d66dfbad6d
Create Date: 2023-12-22 23:27:43.089961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dfce381d016'
down_revision: Union[str, None] = '49d66dfbad6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_accept_date()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.status = 'accepted' THEN
                UPDATE friendships
                SET status = 'accepted', accept_date = NOW()
                WHERE (requester_id = NEW.addressee_id AND addressee_id = NEW.requester_id)
                      OR (requester_id = NEW.requester_id AND addressee_id = NEW.addressee_id);
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER update_accept_date_trigger
        AFTER UPDATE ON friendships
        FOR EACH ROW
        WHEN (NEW.status = 'accepted' AND OLD.status = 'pending')
        EXECUTE FUNCTION update_accept_date();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER update_accept_date_trigger ON friendships")
    op.execute("DROP FUNCTION update_accept_date()")
