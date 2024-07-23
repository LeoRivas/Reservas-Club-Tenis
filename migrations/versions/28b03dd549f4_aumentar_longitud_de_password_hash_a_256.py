from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28b03dd549f4'
down_revision = '224e010e8eca'
branch_labels = None
depends_on = None


def upgrade():
    # Paso 1: Crear una nueva columna
    op.add_column('user', sa.Column('new_password_hash', sa.String(256)))

    # Paso 2: Copiar los datos de la columna antigua a la nueva columna
    op.execute('UPDATE "user" SET new_password_hash = password_hash')

    # Paso 3: Eliminar la columna antigua
    op.drop_column('user', 'password_hash')

    # Paso 4: Renombrar la nueva columna
    op.alter_column('user', 'new_password_hash', new_column_name='password_hash')


def downgrade():
    # Paso inverso para downgrade

    # Paso 1: Crear la columna antigua
    op.add_column('user', sa.Column('old_password_hash', sa.String(128)))

    # Paso 2: Copiar los datos de la nueva columna a la columna antigua
    op.execute('UPDATE "user" SET old_password_hash = password_hash')

    # Paso 3: Eliminar la nueva columna
    op.drop_column('user', 'password_hash')

    # Paso 4: Renombrar la columna antigua
    op.alter_column('user', 'old_password_hash', new_column_name='password_hash')
