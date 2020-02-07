from threading import Thread

from flask import current_app
from flask_mail import Message

from app.extensions import mail

def send_async_email(app, msg):
    '''异步发送邮件'''
    # 由于开启了新的线程，所以需要推送 Flask应用上下文（ 使用 with app.app_context()），
    # 不然 Flask-Mail 将找不到配置项，因为它的相关配置存储在 app.config 对象中
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=True):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        # 附件
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        # 同步发送
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
