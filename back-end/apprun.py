from app import create_app, db
from app.models import User

app = create_app()


#添加flask shell上下文
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User}