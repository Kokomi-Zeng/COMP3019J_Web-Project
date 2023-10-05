from exts import db;

class User(db.Model):
    __tablename__ = "users"

    phone = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(128))
    user_type = db.Column(db.String(10))

    # 这里这么做是为了方便查询，使得可以反向查询，即通过buyer或者seller查询到user
    buyer = db.relationship("Buyer", backref="user", uselist=False)
    seller = db.relationship("Seller", backref="user", uselist=False)

class Buyer(db.Model):
    __tablename__ = "buyers"

    # 表示将users表中的phone设置为这个表的外键
    phone = db.Column(db.String(15), db.ForeignKey("users.phone"), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    # 余额
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

    comments = db.relationship("Comment", backref="product")
    purchases = db.relationship("Purchase", backref="product")

class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    buyer_phone = db.Column(db.String(15), db.ForeignKey("buyers.phone"))
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)

class Purchase(db.Model):
    __tablename__ = "purchases"

    purchase_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    buyer_phone = db.Column(db.String(15), db.ForeignKey("buyers.phone"))
    purchase_number = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)