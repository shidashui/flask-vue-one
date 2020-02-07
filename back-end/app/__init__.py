import click
from flask import Flask
from app.api import bp as api_bp

from app.extensions import db, migrate, cors, mail
from config import Config




def create_app(config_class=None):
    '''Factory Pattern: Create Flask app.'''
    app = Flask(__name__)

    # Initialization flask app
    configure_app(app, config_class)
    configure_blueprints(app)
    configure_extensions(app)
    # 不使用 Jinja2，用不到模版过滤器和上下文处理器
    # configure_template_filters(app)
    # configure_context_processors(app)
    configure_before_handlers(app)
    configure_after_handlers(app)
    configure_errorhandlers(app)
    configure_commands(app)

    return app

def configure_app(app, config_class):
    app.config.from_object(config_class)
    # 不检查路由中最后是否有斜杠/
    app.url_map.strict_slashes = False

def configure_blueprints(app):
    # 注册 blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

def configure_extensions(app):
    '''Configures the extensions.'''
    # Enable CORS
    cors.init_app(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)
    # Init Flask-Mail
    mail.init_app(app)

def configure_before_handlers(app):
    '''Configures the before request handlers'''
    pass


def configure_after_handlers(app):
    '''Configures the after request handlers'''
    pass

def configure_errorhandlers(app):
    '''Configures the error handlers'''
    pass

def configure_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='先删除后创建')
    def initdb(drop):
        if drop:
            click.confirm('此操作会删除数据库', abort=True)
            db.drop_all()
            click.echo('已删除')
        db.create_all()
        click.echo('初始化数据库')

    @app.cli.command()
    @click.option('--user', default=10, help='用户数量，默认10')
    @click.option('--post', default=50, help='博客数量, 默认50')
    def forge(user, post):
        from app.fakes import fake_admin, fake_users, fake_posts, fake_follow

        db.drop_all()
        db.create_all()
        fake_admin()
        fake_users(count=user)
        fake_posts(count=post)
        fake_follow()
        click.echo('数据填充')