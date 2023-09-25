import config
from flask import Flask
from exts import db
from blueprints.authorize import bp as authorize_bp
from flask_migrate import Migrate



app = Flask(__name__)

# 从config.py中加载配置（绑定配置文件）
app.config.from_object(config)

# 作用在于：可以不要在创建的时候跟app绑定，可以先创建，然后绑定
db.init_app(app)

# 使蓝图生效，产生关联
app.register_blueprint(authorize_bp)

# 使迁移生效
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()