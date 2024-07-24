"""Add payments and accounts test data

Revision ID: 1581f8832b5c
Revises: 2a217f1c002a
Create Date: 2024-07-24 09:08:40.691340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1581f8832b5c'
down_revision: Union[str, None] = '2a217f1c002a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO accounts (owner_id, balance)
        VALUES (
            (SELECT id FROM users WHERE email = 'testuser@example.com'), 
            1000
        )
        """
    )

    # Добавление тестового платежа для тестового пользователя
    op.execute(
        """
        INSERT INTO payments (account_id, amount)
        VALUES (
            (SELECT id FROM accounts WHERE owner_id = (SELECT id FROM users WHERE email = 'testuser@example.com')), 
            500
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM payments WHERE account_id = (SELECT id FROM accounts WHERE owner_id = (SELECT id FROM users WHERE email = 'testuser@example.com'))
        """
    )
    op.execute(
        """
        DELETE FROM accounts WHERE owner_id = (SELECT id FROM users WHERE email = 'testuser@example.com')
        """
    )
