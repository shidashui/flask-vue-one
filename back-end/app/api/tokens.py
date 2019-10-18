from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth

#JWT 没办法回收（不需要 DELETE /tokens），只能等它过期，所以有效时间别设置太长
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    # token = g.current_user.get_token()
    token = g.current_user.get_jwt()
    # 每次用户登录（即成功获取 JWT 后），更新 last_seen 时间
    g.current_user.ping()
    db.session.commit()
    return jsonify({'token':token})


# @bp.route('/tokens', methods=['DELETE'])
# @token_auth.login_required
# def revoke_token():
#     g.current_user.revoke_token()
#     db.session.commit()
#     return '', 204