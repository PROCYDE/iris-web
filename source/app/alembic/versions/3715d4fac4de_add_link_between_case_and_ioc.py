"""Add link between case and IOC

Revision ID: 3715d4fac4de
Revises: 11aa5b725b8e
Create Date: 2024-05-22 16:33:24.146511
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

from app.alembic.alembic_utils import _table_has_column, _has_table

# revision identifiers, used by Alembic.
revision = '3715d4fac4de'
down_revision = 'd5a720d1b99b'
branch_labels = None
depends_on = None


def upgrade():
    # Add case_id column on ioc if it does not exist
    if not _table_has_column('ioc', 'case_id'):
        op.add_column(
            'ioc',
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.case_id'), nullable=True)
        )
        op.execute("COMMIT")

    conn = op.get_bind()

    # Ensure ioc_link table exists (db.create_all only runs on first startup,
    # so on subsequent restarts with existing DB we may need to create it)
    if not _has_table('ioc_link'):
        op.create_table(
            'ioc_link',
            sa.Column('ioc_link_id', sa.BigInteger, primary_key=True),
            sa.Column('ioc_id', sa.Integer, sa.ForeignKey('ioc.ioc_id')),
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.case_id')),
        )

    # For existing IOCs that have case_id set but no ioc_link entry,
    # create the missing link entries
    iocs_with_case = conn.execute(
        text("SELECT ioc_id, case_id FROM ioc WHERE case_id IS NOT NULL")
    ).fetchall()

    existing_links = conn.execute(
        text("SELECT ioc_id, case_id FROM ioc_link")
    ).fetchall()
    existing_pairs = {(r.ioc_id, r.case_id) for r in existing_links}

    for row in iocs_with_case:
        if (row.ioc_id, row.case_id) not in existing_pairs:
            conn.execute(
                text("INSERT INTO ioc_link (ioc_id, case_id) VALUES (:ioc_id, :case_id)"),
                {"ioc_id": row.ioc_id, "case_id": row.case_id}
            )

    op.alter_column('ioc', 'case_id', nullable=True)


def downgrade():
    pass
