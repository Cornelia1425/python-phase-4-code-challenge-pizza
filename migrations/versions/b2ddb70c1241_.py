"""empty message

Revision ID: b2ddb70c1241
Revises: 9eaa429c4279
Create Date: 2024-05-30 16:38:44.163831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2ddb70c1241'
down_revision = '9eaa429c4279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('res_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('pizza_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_res_id_restaurants'), 'restaurants', ['res_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_pizza_id_pizzas'), 'pizzas', ['pizza_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_pizza_id_pizzas'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_res_id_restaurants'), type_='foreignkey')
        batch_op.drop_column('pizza_id')
        batch_op.drop_column('res_id')

    # ### end Alembic commands ###