"""add password reset fields to users"""

from alembic import op
import sqlalchemy as sa

# Revisões
revision = '0001_add_password_reset_fields'
down_revision = None  # Coloque o ID da migração anterior se houver
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password_reset_token', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('password_reset_token_expiration', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password_reset_token_expiration')
    op.drop_column('users', 'password_reset_token')
