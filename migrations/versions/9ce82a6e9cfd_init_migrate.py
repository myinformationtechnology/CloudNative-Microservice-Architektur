"""init migrate

Revisions-ID: 9ce82a6e9cfd
Überarbeitet: 
Erstellungsdatum: 202-10-15 13:13:21.435558

"""
from alembic import op
import sqlalchemy as sa

# Revisionskennungen, die von Alembic verwendet werden.
revision = '9ce82a6e9cfd'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### Befehle, die von Alembic automatisch generiert wurden - bitte anpassen! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('role', sa.String(length=32), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_active_at', sa.DateTime(), nullable=True),
    sa.Column('failed_auth_at', sa.DateTime(), nullable=True),
    sa.Column('failed_auth_count', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### Ende der Alembic-Befehle ###

def downgrade():
    # ### Befehle, die von Alembic automatisch generiert wurden - bitte anpassen! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.drop_table('user')
    # ### Ende der Alembic-Befehle ###

