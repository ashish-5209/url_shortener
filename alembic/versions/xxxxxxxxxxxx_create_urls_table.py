from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision = 'xxxxxxxxxxxx'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('short_url', sa.String, unique=True, index=True),
        sa.Column('original_url', sa.String, nullable=False),
        sa.Column('expiry_time', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('urls')
