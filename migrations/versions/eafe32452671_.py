"""empty message

Revision ID: eafe32452671
Revises: None
Create Date: 2016-10-27 21:37:21.856516

"""

# revision identifiers, used by Alembic.
revision = 'eafe32452671'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('djevents')
    op.drop_table('entries')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('text', mysql.VARCHAR(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_table('djevents',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=4096), server_default=sa.text(u"''"), nullable=False),
    sa.Column('date', mysql.VARCHAR(length=4096), server_default=sa.text(u"''"), nullable=False),
    sa.Column('gist', mysql.VARCHAR(length=4096), server_default=sa.text(u"''"), nullable=False),
    sa.Column('occupancy', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('occupied', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('update_time', mysql.TIMESTAMP(), server_default=sa.text(u'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
