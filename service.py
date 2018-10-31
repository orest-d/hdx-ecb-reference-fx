import logging
from flask import Flask, Response
from urllib.request import urlopen
import ecbfx_blueprint

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app.register_blueprint(ecbfx_blueprint.app, url_prefix='/ecbfx')

if __name__ == '__main__':
    app.run(debug=True)
