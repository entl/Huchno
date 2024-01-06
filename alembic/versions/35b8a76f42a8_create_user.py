"""create user

Revision ID: 35b8a76f42a8
Revises: 
Create Date: 2023-12-17 17:36:40.740166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '35b8a76f42a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('birthdate', sa.DATE(), nullable=False),
    sa.Column('profile_image', sa.String(), server_default='default.jpg', nullable=False),
    sa.Column('registration_date', sa.DATE(), server_default=sa.text('CURRENT_DATE'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('last_login', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('verified', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False, onupdate=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trigger_update_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW EXECUTE FUNCTION update_updated_at();
        """
    )


    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TRIGGER trigger_update_updated_at ON users")
    op.execute("DROP FUNCTION update_updated_at()")
    op.drop_table('users')

    # ### end Alembic commands ###
