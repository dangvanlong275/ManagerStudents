"""detail_student

Revision ID: 55a62bcec0ee
Revises: 0ad245149ad9
Create Date: 2021-12-04 18:35:11.540145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55a62bcec0ee'
down_revision = '0ad245149ad9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('age', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_address'), 'student', ['address'], unique=True)
    op.create_index(op.f('ix_student_age'), 'student', ['age'], unique=True)
    op.create_index(op.f('ix_student_email'), 'student', ['email'], unique=True)
    op.create_index(op.f('ix_student_name'), 'student', ['name'], unique=True)
    op.create_table('detail_student',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], name='fk_class_detail_student'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_student_detail_student'),
    sa.PrimaryKeyConstraint('student_id', 'class_id')
    )
    op.drop_index('ix_students_address', table_name='students')
    op.drop_index('ix_students_age', table_name='students')
    op.drop_index('ix_students_email', table_name='students')
    op.drop_index('ix_students_name', table_name='students')
    op.drop_table('students')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('age', sa.VARCHAR(length=64), nullable=True),
    sa.Column('address', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_students_name', 'students', ['name'], unique=False)
    op.create_index('ix_students_email', 'students', ['email'], unique=False)
    op.create_index('ix_students_age', 'students', ['age'], unique=False)
    op.create_index('ix_students_address', 'students', ['address'], unique=False)
    op.drop_table('detail_student')
    op.drop_index(op.f('ix_student_name'), table_name='student')
    op.drop_index(op.f('ix_student_email'), table_name='student')
    op.drop_index(op.f('ix_student_age'), table_name='student')
    op.drop_index(op.f('ix_student_address'), table_name='student')
    op.drop_table('student')
    # ### end Alembic commands ###
