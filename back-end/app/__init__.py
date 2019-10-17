from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate(db=db)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #允许cors跨域请求
    CORS(app)

    #扩展配置
    db.init_app(app)
    migrate.init_app(app)

    #注册blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


from app import models