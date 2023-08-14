# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


# Add your code after this line
from peewee import fn
from setupdb import set_database, populate_test_database, delete_database
from fuzzywuzzy import process


from models import (
    User,
    Tag,
    Product,
    ProductTag,
    UsersOwnProducts,
    Transaction
)


def search(term):
    # select all the products and descriptions for search
    products_for_search = []
    descriptions_for_search = []
    for product in Product.select():
        products_for_search.append(product.name)
        descriptions_for_search.append(product.description)
    # determine ratio hight
    product_terms_to_search = process.extract(
        term, products_for_search)
    descriptions_to_search = process.extract(
        term, descriptions_for_search)
    # add all products to products list by ratio
    products = []
    for product in product_terms_to_search:
        if product[1] > 80:
            if product[0] not in products:
                products.append(product[0])
    for description in descriptions_to_search:
        if description[1] > 60:
            product_description = Product.get(
                Product.description == description[0])
            product_name = product_description.name
            if product_name not in products:
                products.append(product_name)
    # return the products if they exist
    if products:
        return (f'Betsy found this product {products}')
    else:
        return (f'Betsy found No products with the term {term}')


def list_user_products(user_id):
    user_products = []
    # select the products, and 'filter' by user_id.
    for user_product in (Product.select()
                         .join(UsersOwnProducts)
                         .join(User)
                         .where(User.id == user_id)):
        # check amount in stock
        if user_product.amount_in_stock > 0:
            user_products.append(user_product.name)
    # return list of users products if they exist.
    if user_products:
        return (user_products)
    else:
        return ('User has no products')


def list_products_per_tag(tag):
    found_products = []
    # Select products, and 'filter' by tag.
    for product in (Product.select()
                    .join(ProductTag)
                    .join(Tag)
                    .where(fn.LOWER(Tag.tag) == tag.lower())):
        found_products.append(product.name)
    # return list of products if they exist
    if found_products:
        return (found_products)
    else:
        return (f'There are NO products with the tag {tag}')


def add_product_to_catalog(user_id, product, tag_name):
    def Product_create(tag):
        Product.create(name=product[0], description=product[1],
                       price_per_unit=product[2], amount_in_stock=product[3])
        product_id = Product.get(Product.name == product[0])
        ProductTag.create(tag_id=tag, product_id=product_id)
    # check if tag exists if not create tag and product else create product
    if not (Tag.select()
            .where(Tag.tag == tag_name)
            .exists()):
        Tag.create(tag=tag_name)
        tag = Tag.get(Tag.tag == tag_name)
        Product_create(tag)
    else:
        tag = Tag.get(Tag.tag == tag_name)
        Product_create(tag)
    # get user and product
    user = User.get(User.id == user_id)
    new_product = Product.get(Product.name == product[0])
    # create new connection between user and product
    UsersOwnProducts.create(user_id=user, product_id=new_product)


def remove_product(product_id):
    # remove product
    Product.delete_by_id(product_id)
    # remove connection between user an product
    (UsersOwnProducts.delete()
     .where(UsersOwnProducts
     .product_id == product_id)
     .execute())
    # remove connection between product and tag
    ProductTag.delete().where(ProductTag.product_id == product_id).execute()


def update_stock(product_id, new_quantity):
    # update product from a user
    Product.update(amount_in_stock=new_quantity).where(
        Product.id == product_id).execute()

    product = Product.get(Product.id == product_id)
    return (f"product.amount_in_stock = {product.amount_in_stock}")


def purchase_product(product_id, buyer_id, quantity):
    # get product, buyer, seller
    product = Product.get(Product.id == product_id)
    buyer = User.get(User.id == buyer_id)
    seller = User.select().join(UsersOwnProducts).join(
        Product).where(Product.id == product_id)
    # check if there is enough product in stock.
    if quantity > product.amount_in_stock:
        return ('Not enough in stock!')
    else:
        Transaction.create(buyer_id=buyer, seller_id=seller,
                           product_id=product, quantity=quantity)
        new_stock = product.amount_in_stock - quantity
        update_stock(product_id, new_stock)
        return ('Product purchased!')


# ----------------------------------
if __name__ == "__main__":
    delete_database()
    set_database()

    # test
    populate_test_database()
    print("---------")

    print("TEST search")
    print(search("APPLE"))
    print(search("bicycle"))
    print(search("G-star"))
    print(search("bicycle bell"))
    print(search("Bluetooth"))
    print(search("BLEUTOOTH"))
    print(search("size"))
    print("---------")

    print("TEST list_user_products")
    print(list_user_products(1))
    print(list_user_products(2))
    print(list_user_products(3))
    print(list_user_products(4))
    print(list_user_products(5))
    print("---------")

    print("TEST list_products_per_tag")
    print(list_products_per_tag("appel"))
    print(list_products_per_tag("Clothes"))
    print(list_products_per_tag("clothes"))
    print(list_products_per_tag("ELECTRONICS"))
    print(list_products_per_tag("Bikeproducts"))
    print(list_products_per_tag("444"))
    print("---------")

    print("TEST add_product")
    user_id = 3
    product = ('bicycle saddle', 'Selle Italia Diva Gel Superflow ', 89.95, 1)
    tag_name = ('Bikeproducts')
    add_product_to_catalog(user_id, product, tag_name)

    user_id = 1
    product = ('Hammer', 'Fiberglass clawhammer ', 22.95, 2)
    tag_name = ('construction worker tools')
    add_product_to_catalog(user_id, product, tag_name)

    print(search("Fiberglass"))
    print(list_user_products(3))

    print(search("bicycle saddle'"))
    print(list_user_products(1))
    print("---------")

    print("TEST remove_product by id")

    print(list_products_per_tag("Bikeproducts"))
    remove_product(2)
    print(list_products_per_tag("Bikeproducts"))
    print("---------")

    print("TEST update_stock")
    print(update_stock(3, 40))
    print("---------")

    print("TEST purchase_product")

    # user andre bought one Pilot Jacket
    print(purchase_product(4, 1, 1))
    # user yvette bought one Pilot Jacket
    print(purchase_product(4, 2, 1))
    # user esmee bought one Pilot Jacket
    print(purchase_product(4, 4, 1))
    # user andre bought 41 Bicycle Bell
    print(purchase_product(3, 1, 41))
