"""empty message

Revision ID: 698c20678b0d
Revises: 
Create Date: 2021-06-09 21:18:45.485104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '698c20678b0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=25), nullable=False),
    sa.Column('password', sa.String(length=25), nullable=False),
    sa.Column('phone', sa.String(length=25), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('short_description', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('blog_posted', sa.DateTime(), nullable=True),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('customer', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['blogcategory.id'], ),
    sa.ForeignKeyConstraint(['customer'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('comment_posted', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('short_description', sa.String(length=127), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['category.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('location', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=20), nullable=True),
    sa.Column('city', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city'], ['city.title'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('restaurant')
    op.drop_table('order')
    op.drop_table('comment')
    op.drop_table('blog')
    op.drop_table('user')
    op.drop_table('city')
    op.drop_table('category')
    op.drop_table('blogcategory')
    # ### end Alembic commands ###
