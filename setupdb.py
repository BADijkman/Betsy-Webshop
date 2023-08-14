import os
from models import (
    db,
    User,
    Address,
    UserAddresses,
    Tag,
    Product,
    ProductTag,
    UsersOwnProducts,
    Transaction
)


def set_database():
    # connect to database / create tables
    db.connect()
    db.create_tables(
        [User,
         Address,
         UserAddresses,
         Tag,
         Product,
         ProductTag,
         UsersOwnProducts,
         Transaction
         ]
    )
    print('database was created!')


def populate_test_database():
    # add users
    user_data = ['Andre',
                 'Yvette',
                 'Thomas',
                 'Esmee',
                 'Bob'
                 ]
    for user in user_data:
        User.create(name=user)
    print('Users added!')

    # add addresses
    address_data = [
        ("Abersland", 101, "6605NX", "Wijchen", "The Netherlands"),
        ("Graetheideweg", 62, "6037NN", "Kelpen-oler", "The Netherlands"),
        ("Grashof ", 3, "2262ER", "Leidschendam", "The Netherlands"),
        ("Raminhout", 53, "2719KN", "Zoetermeer", "The Netherlands"),
        ("Dorpsstraat", 88, "1234AB", "Urk", "The Netherlands"),
        ("Kalverstaat", 2, "2266XX", "Amsterdam", "The Netherlands"),
        ("Blaak", 123, "4455YY", "Rotterdam", "The Netherlands")
    ]
    Address.insert_many(address_data, fields=[
                        Address.street,
                        Address.house_number,
                        Address.zip_code,
                        Address.city, Address.country]
                        ).execute()
    print('Addresses added!')

    # add UserAddresses
    user_address_data = [
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 4),
        (4, 5, 5),
        (5, 6, 7)
    ]
    for user_id, home_address_id, billing_address_id in user_address_data:
        user = User.get(User.id == user_id)
        home_address = Address.get(Address.id == home_address_id)
        billing_address = Address.get(Address.id == billing_address_id)
        UserAddresses.create(
            user_id=user, home_address_id=home_address,
            billing_address_id=billing_address)
    print('UsersAdresses added!')

    # add tags
    tags = ['Clothes', 'Electronics', 'Bikeproducts']
    for tag in tags:
        Tag.create(tag=tag)
    print('Tags added!')

    # add products
    products = [
        ('G-star jeans', 'Nice blue slimfit jeans!', 99.99, 1),
        ('JBL Go 3', 'Bluetooth speaker JBL pro sound', 35.98, 2),
        ('Bicycle bell', 'Very loud bell sound with bluetooth ', 3.00, 20),
        ('Pilot Jacket', 'Pilot Jacket black men size XL', 119.95, 2)
    ]
    for name, description, price_per_unit, amount_in_stock in products:
        Product.create(name=name, description=description,
                       price_per_unit=price_per_unit,
                       amount_in_stock=amount_in_stock)
    print('Products added!')

    # connect products to tags
    product_tags = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 1)
    ]
    for product, tag in product_tags:
        product_id = Product.get(Product.id == product)
        tag_id = Tag.get(Tag.id == tag)
        ProductTag.create(product_id=product_id, tag_id=tag_id)
    print('ProductTags added!')

    # add users own products
    user_own_products = [
        (1, 1),
        (1, 3),
        (3, 2),
        (5, 4),
        (5, 2),
        (5, 1)
    ]

    for user, product in user_own_products:
        user_id = User.get(User.id == user)
        product_id = Product.get(Product.id == product)
        UsersOwnProducts.create(user_id=user_id, product_id=product_id)
    print('UserOwnProducts added!')

    # close the database
    db.close()


def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "betsydb.db")
    if os.path.exists(database_path):
        os.remove(database_path)
        print("database was removed!")
