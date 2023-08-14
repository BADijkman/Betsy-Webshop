from peewee import (Model,
                    SqliteDatabase,
                    CharField,
                    ForeignKeyField,
                    IntegerField,
                    DecimalField,
                    TextField)

db = SqliteDatabase("betsydb.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField(max_length=50)


class Address(BaseModel):
    street = CharField(max_length=30)
    house_number = IntegerField()
    zip_code = CharField(max_length=6)
    city = CharField(max_length=30)
    country = CharField(max_length=30)


class UserAddresses(BaseModel):
    user_id = ForeignKeyField(User)
    home_address_id = ForeignKeyField(Address)
    billing_address_id = ForeignKeyField(Address)


class Tag(BaseModel):
    tag = CharField(max_length=20)


class Product(BaseModel):
    name = CharField(max_length=30, index=True)
    description = TextField(index=True)
    price_per_unit = DecimalField(
        max_digits=10, decimal_places=2, auto_round=True, index=True)
    amount_in_stock = IntegerField(index=True)


class ProductTag(BaseModel):
    tag_id = ForeignKeyField(Tag)
    product_id = ForeignKeyField(Product)


class UsersOwnProducts(BaseModel):
    user_id = ForeignKeyField(User, backref='products')
    product_id = ForeignKeyField(Product)


class Transaction(BaseModel):
    buyer_id = ForeignKeyField(User)
    seller_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
    quantity = IntegerField()
