from flask import Flask
from flask import request

import api_handler
from client.constants import ResponseType
import config
from db import db_instance

app = Flask(__name__)


@app.route('/')
def home_page():
    return ""


@app.route('/website', methods=['GET'])
def get_metadata():
    local_request = request
    url = request.args.get('src')
    response_type = local_request.args.get('format')
    if response_type is None:
        response_type = ResponseType.JSON  # Default return format is json
    return api_handler.get_metadata(url, response_type)


if __name__ == '__main__':
    if config.USE_DB:
        db_instance.DbInstance.init_db_instance()
    app.run(debug=config.IS_DEV)
