
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

from resources.users import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='{prefix}/v{version}'.format(
    prefix=app.config['URL_PREFIX'], version='1'))

from resources.bucket_list import bucket_list_blueprint
app.register_blueprint(bucket_list_blueprint, url_prefix='{prefix}/v{version}'.format(
    prefix=app.config['URL_PREFIX'], version='1'))

if __name__ == '__main__':
    app.run()
