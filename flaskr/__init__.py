import os
from flask import Flask

# application factory function
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    # デフォルトのconfigをセット
    app.config.from_mapping(
        SECRET_KEY='dev',  # デプロイ時はランダムの値で上書きされるべし
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  #DBのパス
    )

    if test_config is None:
        # config.pyでデフォルトのconfigを上書き
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
