"""Set ON DELETE CASCADE for notifications.user_id foreign key

Revision ID: 20250704_ondelete_cascade_notifications
Revises: 39d040298944_make_roll_number_unique_per_class_not_
Create Date: 2025-07-04 06:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250704_ondelete_cascade_notifications'
down_revision = '39d040298944_make_roll_number_unique_per_class_not_'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the old foreign key constraint
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_constraint('notifications_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'notifications_user_id_fkey',
            'users',
            ['user_id'], ['id'],
            ondelete='CASCADE'
        )

def downgrade():
    # Revert to the old foreign key constraint (no cascade)
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_constraint('notifications_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'notifications_user_id_fkey',
            'users',
            ['user_id'], ['id']
        ) 