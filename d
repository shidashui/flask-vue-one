[33mcommit 5f66c5b497f666a88dc395346ad1edbb3d3ada96[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;33mtag: v0.1[m[33m, [m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: shui <164635470@qq.com>
Date:   Wed Oct 16 09:46:04 2019 +0800

    fflask项目初始化

[1mdiff --git a/.gitignore b/.gitignore[m
[1mnew file mode 100644[m
[1mindex 0000000..573c686[m
[1m--- /dev/null[m
[1m+++ b/.gitignore[m
[36m@@ -0,0 +1,6 @@[m
[32m+[m[32m.idea/[m
[32m+[m[32m__pycache__/[m
[32m+[m[32mvenv/[m
[32m+[m[32m.env[m
[32m+[m[32mapp.db[m
[32m+[m[32m*.log[m
\ No newline at end of file[m
[1mdiff --git a/back-end/app/__init__.py b/back-end/app/__init__.py[m
[1mnew file mode 100644[m
[1mindex 0000000..f8b5a36[m
[1m--- /dev/null[m
[1m+++ b/back-end/app/__init__.py[m
[36m@@ -0,0 +1,13 @@[m
[32m+[m[32mfrom flask import Flask[m
[32m+[m[32mfrom config import Config[m
[32m+[m
[32m+[m
[32m+[m[32mdef create_app(config_class=Config):[m
[32m+[m[32m    app = Flask(__name__)[m
[32m+[m[32m    app.config.from_object(config_class)[m
[32m+[m
[32m+[m
[32m+[m[32m    #注册blueprint[m
[32m+[m[32m    from app.api import bp as api_bp[m
[32m+[m[32m    app.register_blueprint(api_bp, url_prefix='/api')[m
[32m+[m[32m    return app[m
\ No newline at end of file[m
[1mdiff --git a/back-end/app/api/__init__.py b/back-end/app/api/__init__.py[m
[1mnew file mode 100644[m
[1mindex 0000000..1b1e506[m
[1m--- /dev/null[m
[1m+++ b/back-end/app/api/__init__.py[m
[36m@@ -0,0 +1,6 @@[m
[32m+[m[32mfrom flask import Blueprint[m
[32m+[m
[32m+[m[32mbp = Blueprint('api', __name__)[m
[32m+[m
[32m+[m
[32m+[m[32mfrom  app.api import ping[m
[1mdiff --git a/back-end/app/api/ping.py b/back-end/app/api/ping.py[m
[1mnew file mode 100644[m
[1mindex 0000000..b951542[m
[1m--- /dev/null[m
[1m+++ b/back-end/app/api/ping.py[m
[36m@@ -0,0 +1,7 @@[m
[32m+[m[32mfrom flask import jsonify[m
[32m+[m[32mfrom app.api import bp[m
[32m+[m
[32m+[m
[32m+[m[32m@bp.route('/ping', methods=['GET'])[m
[32m+[m[32mdef ping():[m
[32m+[m[32m    return jsonify('Pong!')[m
\ No newline at end of file[m
[1mdiff --git a/back-end/apprun.py b/back-end/apprun.py[m
[1mnew file mode 100644[m
[1mindex 0000000..7368d5a[m
[1m--- /dev/null[m
[1m+++ b/back-end/apprun.py[m
[36m@@ -0,0 +1,3 @@[m
[32m+[m[32mfrom app import create_app[m
[32m+[m
[32m+[m[32mapp = create_app()[m
\ No newline at end of file[m
[1mdiff --git a/back-end/config.py b/back-end/config.py[m
[1mnew file mode 100644[m
[1mindex 0000000..ce9ec34[m
[1m--- /dev/null[m
[1m+++ b/back-end/config.py[m
[36m@@ -0,0 +1,12 @@[m
[32m+[m[32mimport os[m
[32m+[m[32mfrom dotenv import load_dotenv[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mbasedir = os.path.abspath(os.path.dirname(__file__))[m
[32m+[m[32m# print(os.path.join(basedir,'.env'))[m
[32m+[m[32mload_dotenv(os.path.join(basedir,'.env'))[m
[32m+[m
[32m+[m
[32m+[m[32mclass Config(object):[m
[32m+[m[32m    pass[m
\ No newline at end of file[m
[1mdiff --git a/back-end/requirements.txt b/back-end/requirements.txt[m
[1mnew file mode 100644[m
[1mindex 0000000..0d17425[m
[1m--- /dev/null[m
[1m+++ b/back-end/requirements.txt[m
[36m@@ -0,0 +1,7 @@[m
[32m+[m[32mClick==7.0[m
[32m+[m[32mFlask==1.1.1[m
[32m+[m[32mitsdangerous==1.1.0[m
[32m+[m[32mJinja2==2.10.3[m
[32m+[m[32mMarkupSafe==1.1.1[m
[32m+[m[32mpython-dotenv==0.10.3[m
[32m+[m[32mWerkzeug==0.16.0[m
