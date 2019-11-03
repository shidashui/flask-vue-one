import base64
import os
from hashlib import md5
from datetime import datetime, timedelta

import jwt
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash

# 通用类
from app.extensions import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data

#粉丝关注他人
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),  # 粉丝
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),  # 大神
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

#评论点赞
comments_likes = db.Table(
    'comments_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


class User(PaginatedAPIMixin, db.Model):
    # 设置数据库表名，Post模型中的外键 author_id 会引用 users.id
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # 反向引用，直接查询出当前用户的所有博客文章; 同时，Post实例中会有 author 属性
    # cascade 用于级联删除，当删除user时，该user下面的所有posts都会被级联删除
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    # followeds 是该用户关注了哪些用户列表
    # followers 是该用户的粉丝列表
    followeds = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    # 评论  一对多
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    # token
    # token = db.Column(db.String(32), index=True, unique=True)
    # token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>', format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since.isoformat() + 'Z',
            'last_seen': self.last_seen.isoformat() + 'Z',
            'posts_count': self.posts.count(),
            'followed_posts_count': self.followed_posts.count(),
            'followeds_count': self.followeds.count(),
            'followers_count': self.followers.count(),
            'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128),
                'followeds': url_for('api.get_followeds', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'posts': url_for('api.get_user_posts', id=self.id),
                'followeds_posts': url_for('api.get_user_followeds_posts', id=self.id),
                'comments': url_for('api.get_user_comments', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    # json转换成用户对象
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name', 'location', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # token处理
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    # jwt处理token
    # 现在改用 JWT 实现，它可以在 Token 中添加一些不是隐私的数据 payload，比如我们可以把用户 id 放进去
    def get_jwt(self, expires_in=3600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'user_name': self.name if self.name else self.username,
            'user_avatar': base64.b64encode(self.avatar(24).encode('utf-8')).decode('utf-8'),
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except (
        jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError) as e:
            # token过期，被修改都会失效
            return None
        return User.query.get(payload.get('user_id'))

    def avatar(self, size):
        """头像"""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # 关注
    def is_following(self, user):
        """
        判断当前用户是否关注了user这个用户对象，如果关注了，下面表达式左边是1，否则是0
        :param user:
        :return:
        """
        return self.followeds.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followeds.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followeds.remove(user)

    @property
    def followed_posts(self):
        """
        获取当前用户的关注者的所有博客列表
        :return:
        """
        followed = Post.query.join(followers,
                                   (followers.c.followed_id == Post.author_id)).filter(
            followers.c.follower_id == self.id)
        # 包含当前用户自己的博客列表
        # own = Post.query.filter_by(user_id=self.id)
        # return followed.union(own).order_by(Post.timestamp.desc())
        return followed.order_by(Post.timestamp.desc())


class Post(PaginatedAPIMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    # 外键, 直接操纵数据库当user下面有posts时不允许删除user，下面仅仅是 ORM-level “delete” cascade
    # db.ForeignKey('users.id', ondelete='CASCADE') 会同时在数据库中指定 FOREIGN KEY level “ON DELETE” cascade
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # author = db.relationship('User', backref='posts')

    # 评论  一对多
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'body': self.body,
            'timestamp': self.timestamp,
            'views': self.views,
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_post', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'comments': url_for('api.get_post_comments', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'summary', 'body', 'timestamp', 'views']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''
        target: 有监听事件发生的 Post 实例对象
        value: 监听哪个字段的变化
        '''
        if not target.summary:  # 如果前端不填写摘要，是空str，而不是None
            target.summary = value[:200] + '  ... ...'  # 截取 body 字段的前200个字符给 summary


db.event.listen(Post.body, 'set', Post.on_changed_body)  # body 字段有变化时，执行 on_changed_body() 方法


class Comment(PaginatedAPIMixin, db.Model):
    """
    评论model
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)     #屏蔽显示
    mark_read = db.Column(db.Boolean, default=False)     #是否已读
    #点赞，多对多
    likers = db.relationship('User', secondary=comments_likes, backref=db.backref('liked_comments', lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    #自引用的多级评论实现
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'))
    # 级联删除的 cascade 必须定义在 "多" 的那一侧，所以不能这样定义: parent = db.relationship('Comment', backref='children', remote_side=[id], cascade='all, delete-orphan')
    parent = db.relationship('Comment', backref=db.backref('children', cascade='all, delete-orphan'), remote_side=[id])

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

    def get_descendants(self):
        """获取一级评论的子孙"""
        data = set()

        def descendants(comment):
            if comment.children:
                data.update(comment.children)
                for child in comment.children:
                    descendants(child)
        descendants(self)
        return data

    def is_liked_by(self, user):
        """判断用户user是否已经对该评论点赞"""
        return user in self.likers

    def liked_by(self, user):
        """点赞"""
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        """取消点赞"""
        if self.is_liked_by(user):
            self.likers.remove(user)

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'disabled': self.disabled,
            'mark_read': self.mark_read,
            'likers_id': [user.id for user in self.likers],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'post': {
                'id': self.post.id,
                'title': self.post.title,
                'author_id': self.post.author.id
            },
            'parent_id': self.parent.id if self.parent else None,
            '_links': {
                'self': url_for('api.get_comment', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'post_url': url_for('api.get_post', id=self.post_id),
                'parent_url': url_for('api.get_commet', id=self.parent.id) if self.parent else None,
                'children_url': [url_for('api.get_comment', id=child.id) for child in self.children] if self.children else None
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'disabled', 'timestamp', 'mark_read', 'author_id', 'post_id', 'parent_id']:
            if field in data:
                setattr(self, field, data[field])
