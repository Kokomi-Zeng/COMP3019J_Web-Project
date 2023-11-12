import config
from blueprints.image import image_bp
from flask import Flask

from blueprints.buyer import buyer_bp
from blueprints.comments import comment_bp
from blueprints.index import bp
from blueprints.products import products_bp
from blueprints.seller import seller_bp
from blueprints.shop import shop_bp
from blueprints.user import user_bp
from exts import db
from blueprints.authorize import bp as authorize_bp
from flask_migrate import Migrate


app = Flask(__name__)

# Load the configuration from config.py (bind the configuration file)
app.config.from_object(config)

# The effect is that: you can not bind with app when creating, you can create first, and then bind
db.init_app(app)

# Register the blueprint
app.register_blueprint(authorize_bp)
app.register_blueprint(buyer_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(bp)
app.register_blueprint(products_bp)
app.register_blueprint(seller_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(image_bp)
app.register_blueprint(user_bp)

# Make migration effective
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()