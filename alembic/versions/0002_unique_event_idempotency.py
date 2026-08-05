"""Add unique partial index on events (shipment_id, idempotency_key) where idempotency_key IS NOT NULL

This migration enforces at the database level that for a given shipment, the
same idempotency_key cannot be inserted twice. This makes the idempotency
behavior robust under concurrency.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_unique_event_idempotency'
down_revision = '0001_create_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Create a unique index on (shipment_id, idempotency_key) for non-null keys
    op.create_index('uq_events_shipment_id_idempotency_key', 'events', ['shipment_id', 'idempotency_key'], unique=True, postgresql_where=sa.text('idempotency_key IS NOT NULL'))


def downgrade():
    op.drop_index('uq_events_shipment_id_idempotency_key', table_name='events')
