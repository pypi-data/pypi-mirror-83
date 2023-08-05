"""Added onDialogConfirmPayload

Peek Plugin Database Migration Script

Revision ID: 543ec701c9f7
Revises: da155db8b8f1
Create Date: 2017-04-17 09:07:21.947217

"""

# revision identifiers, used by Alembic.
revision = '543ec701c9f7'
down_revision = 'da155db8b8f1'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Task',
                  sa.Column('onDialogConfirmPayload', sa.LargeBinary(), nullable=True),
                  schema='pl_inbox')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Task', 'onDialogConfirmPayload', schema='pl_inbox')
    # ### end Alembic commands ###
