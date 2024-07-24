"""Add test data

Revision ID: 2a217f1c002a
Revises: 44341ebfee6e
Create Date: 2024-07-23 17:33:28.503398

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2a217f1c002a'
down_revision: Union[str, None] = '44341ebfee6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO users (email, full_name, hashed_password, is_admin)
        VALUES ('testuser@example.com', 'Test User', '$2a$10$Ba9ANE5c8PeIXg6L925ONeVnYGPE7XqYwWBBuCzE0LkT7bPSrOv8e', FALSE)
        """
    )
    op.execute(
        """
        INSERT INTO users (email, full_name, hashed_password, is_admin)
        VALUES ('adminuser@example.com', 'Admin User', '$2a$10$rnnXyJFAgilKCJ5g7mWXD.HGhD6GJ3FtNSYdXt24apNL2OexOBEuy', TRUE)
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
    op.execute(
        """
        DELETE FROM users WHERE email IN ('testuser@example.com', 'adminuser@example.com')
        """
    )
