"""Initial table creation

Peek Plugin Database Migration Script

Revision ID: db5936c4d50d
Revises: 
Create Date: 2017-03-06 21:33:18.771121

"""

# revision identifiers, used by Alembic.
revision = 'db5936c4d50d'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uniqueId', sa.String(length=100), nullable=False),
    sa.Column('userId', sa.String(length=50), nullable=False),
    sa.Column('dateTime', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('iconPath', sa.String(length=200), nullable=True),
    sa.Column('routePath', sa.String(length=200), nullable=True),
    sa.Column('routeParamJson', sa.String(length=200), nullable=True),
    sa.Column('autoDeleteDateTime', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uniqueId'),
    schema='pl_inbox'
    )
    op.create_table('Setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='pl_inbox'
    )
    op.create_table('Task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uniqueId', sa.String(length=100), nullable=False),
    sa.Column('userId', sa.String(length=50), nullable=False),
    sa.Column('dateTime', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('iconPath', sa.String(length=200), nullable=True),
    sa.Column('routePath', sa.String(length=200), nullable=True),
    sa.Column('routeParamJson', sa.String(length=200), nullable=True),
    sa.Column('onDeliveredPayload', sa.LargeBinary(), nullable=True),
    sa.Column('onCompletedPayload', sa.LargeBinary(), nullable=True),
    sa.Column('onDeletedPayload', sa.LargeBinary(), nullable=True),
    sa.Column('autoComplete', sa.Integer(), server_default='0', nullable=False),
    sa.Column('autoDelete', sa.Integer(), server_default='0', nullable=False),
    sa.Column('stateFlags', sa.Integer(), server_default='0', nullable=False),
    sa.Column('notificationRequiredFlags', sa.Integer(), server_default='0', nullable=False),
    sa.Column('notificationSentFlags', sa.Integer(), server_default='0', nullable=False),
    sa.Column('displayAs', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uniqueId'),
    schema='pl_inbox'
    )
    op.create_table('SettingProperty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('settingId', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=True),
    sa.Column('int_value', sa.Integer(), nullable=True),
    sa.Column('char_value', sa.String(), nullable=True),
    sa.Column('boolean_value', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['settingId'], ['pl_inbox.Setting.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='pl_inbox'
    )
    op.create_index('idx_SettingProperty_settingId', 'SettingProperty', ['settingId'], unique=False, schema='pl_inbox')
    op.create_table('TaskAction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('taskId', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('confirmMessage', sa.String(length=200), nullable=True),
    sa.Column('onActionPayload', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['taskId'], ['pl_inbox.Task.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='pl_inbox'
    )
    op.create_index('idx_TaskAction_taskId', 'TaskAction', ['taskId'], unique=False, schema='pl_inbox')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_TaskAction_taskId', table_name='TaskAction', schema='pl_inbox')
    op.drop_table('TaskAction', schema='pl_inbox')
    op.drop_index('idx_SettingProperty_settingId', table_name='SettingProperty', schema='pl_inbox')
    op.drop_table('SettingProperty', schema='pl_inbox')
    op.drop_table('Task', schema='pl_inbox')
    op.drop_table('Setting', schema='pl_inbox')
    op.drop_table('Activity', schema='pl_inbox')
    # ### end Alembic commands ###
