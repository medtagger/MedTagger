"""Add tables for Actions like Surveys

Revision ID: e1d0a4fcf63c
Revises: 39c660178412
Create Date: 2018-04-28 20:09:39.238496

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e1d0a4fcf63c'
down_revision = '39c660178412'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Actions',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('action_type', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_Actions')),
                    )
    op.create_table('ActionResponses',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('action_response_type', sa.String(length=50), nullable=False),
                    sa.Column('action_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['action_id'], ['Actions.id'], name=op.f('fk_ActionResponses_action_id_Actions')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_ActionResponses')),
                    )
    op.create_table('Surveys',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('initial_element_key', sa.String(length=50), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['Actions.id'], name=op.f('fk_Surveys_id_Actions')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_Surveys')),
                    )
    op.create_table('SurveyElements',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('key', sa.String(length=50), nullable=False),
                    sa.Column('instant_next_element', sa.String(length=50), nullable=True),
                    sa.Column('survey_element_type', sa.String(length=50), nullable=False),
                    sa.Column('survey_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['survey_id'], ['Surveys.id'], name=op.f('fk_SurveyElements_survey_id_Surveys')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_SurveyElements')),
                    )
    op.create_table('SurveyResponses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['ActionResponses.id'], name=op.f('fk_SurveyResponses_id_ActionResponses')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_SurveyResponses')),
                    )
    op.create_table('SurveySingleChoiceQuestions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('possible_answers', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['SurveyElements.id'], name=op.f('fk_SurveySingleChoiceQuestions_id_SurveyElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_SurveySingleChoiceQuestions')),
                    )


def downgrade():
    op.drop_table('SurveySingleChoiceQuestions')
    op.drop_table('SurveyResponses')
    op.drop_table('SurveyElements')
    op.drop_table('Surveys')
    op.drop_table('ActionResponses')
    op.drop_table('Actions')
