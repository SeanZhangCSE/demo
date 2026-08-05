"""create shipments and events tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2026-08-05 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shipments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_shipments_external_id'), 'shipments', ['external_id'], unique=False)
    op.create_index(op.f('ix_shipments_status'), 'shipments', ['status'], unique=False)

    op.create_table(
        'events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('shipments.id'), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('occurred_at', sa.DateTime(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('idempotency_key', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_events_shipment_id'), 'events', ['shipment_id'], unique=False)
    op.create_index(op.f('ix_events_event_type'), 'events', ['event_type'], unique=False)
    op.create_index(op.f('ix_events_idempotency_key'), 'events', ['idempotency_key'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_events_idempotency_key'), table_name='events')
    op.drop_index(op.f('ix_events_event_type'), table_name='events')
    op.drop_index(op.f('ix_events_shipment_id'), table_name='events')
    op.drop_table('events')

    op.drop_index(op.f('ix_shipments_status'), table_name='shipments')
    op.drop_index(op.f('ix_shipments_external_id'), table_name='shipments')
    op.drop_table('shipments')
