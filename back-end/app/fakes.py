import random

from app.extensions import db
from app.models import User, Post
from faker import Faker

fake = Faker('zh_CN')


def fake_admin():
    admin = User(
        username='shui',
        email='164635470@qq.com',
        name='CoderShui',
        location='石家庄',
        about_me='nothing',
    )
    admin.set_password('123')
    db.session.add(admin)
    db.session.commit()

def fake_users(count=10):
    for i in range(count):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            name=fake.name(),
            location=fake.city(),
            about_me=fake.sentence()
        )
        user.set_password('123')
        db.session.add(user)
    db.session.commit()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(500),
            author_id=random.randint(0,10)
        )
        db.session.add(post)
    db.session.commit()

def fake_follow():
    user = User.query.get(1)
    for i in range(User.query.count()-1):
        follower = User.query.get(i+2)
        user.follow(follower)
        follower.follow(user)
    db.session.commit()
