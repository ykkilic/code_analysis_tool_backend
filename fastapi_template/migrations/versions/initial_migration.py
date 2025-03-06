"""Initial database setup

Revision ID: 91c123def456
Revises: 
Create Date: 2024-01-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91c123def456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create cves table
    op.create_table(
        'cves',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cve_id', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('published_date', sa.DateTime(), nullable=True),
        sa.Column('last_modified_date', sa.DateTime(), nullable=True),
        sa.Column('base_score', sa.Float(), nullable=True),
        sa.Column('impact_score', sa.Float(), nullable=True),
        sa.Column('vector_string', sa.String(), nullable=True),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('references', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cve_id')
    )
    op.create_index(op.f('ix_cves_cve_id'), 'cves', ['cve_id'], unique=True)
    op.create_index(op.f('ix_cves_id'), 'cves', ['id'], unique=False)

    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('language', sa.Enum('python', 'java', 'javascript', 'sql', name='languagetype'), nullable=True),
        sa.Column('repository_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_index(op.f('ix_projects_name'), 'projects', ['name'], unique=False)

    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_id'), 'analyses', ['id'], unique=False)

    # Create vulnerabilities table
    op.create_table(
        'vulnerabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=True),
        sa.Column('cve_id', sa.Integer(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('line_number', sa.Integer(), nullable=True),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('remediation', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ),
        sa.ForeignKeyConstraint(['cve_id'], ['cves.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vulnerabilities_id'), 'vulnerabilities', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_vulnerabilities_id'), table_name='vulnerabilities')
    op.drop_table('vulnerabilities')
    op.drop_index(op.f('ix_analyses_id'), table_name='analyses')
    op.drop_table('analyses')
    op.drop_index(op.f('ix_projects_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_cves_id'), table_name='cves')
    op.drop_index(op.f('ix_cves_cve_id'), table_name='cves')
    op.drop_table('cves')