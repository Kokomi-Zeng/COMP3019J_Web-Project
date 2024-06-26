from exts import db;

class User(db.Model):
    __tablename__ = "users"

    phone = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(128))
    user_type = db.Column(db.String(10))
    image_src = db.Column(db.String(200))
    status = db.Column(db.String(10))

    # The reason why we do this is to make it easier to query, so that we can query the user through buyer or seller
    buyer = db.relationship("Buyer", backref="user", uselist=False)
    seller = db.relationship("Seller", backref="user", uselist=False)

class Buyer(db.Model):
    __tablename__ = "buyers"

    # It means that the phone in the users table is set as the foreign key of this table
    phone = db.Column(db.String(15), db.ForeignKey("users.phone"), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    balance = db.Column(db.Float)

    comments = db.relationship("Comment", backref="buyer")
    purchases = db.relationship("Purchase", backref="buyer")

class Seller(db.Model):
    __tablename__ = "sellers"

    phone = db.Column(db.String(15), db.ForeignKey("users.phone"), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    products = db.relationship("Product", backref="seller")

class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_phone = db.Column(db.String(15), db.ForeignKey("sellers.phone"))
    price = db.Column(db.Float)
    storage = db.Column(db.Integer)
    product_name = db.Column(db.String(150))
    image_src = db.Column(db.String(200))
    description = db.Column(db.String(500))

    comments = db.relationship("Comment", backref="product")
    purchases = db.relationship("Purchase", backref="product")

class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    commenter_phone = db.Column(db.String(15), db.ForeignKey("buyers.phone"))
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)

class Purchase(db.Model):
    __tablename__ = "purchases"

    purchase_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    buyer_phone = db.Column(db.String(15), db.ForeignKey("buyers.phone"))

    # DateTime type, example: 2111-11-11 11:11:11
    purchase_time = db.Column(db.DateTime)
    image_src_at_time_of_purchase = db.Column(db.String(200))
    purchase_number = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)