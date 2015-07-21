from flask import Response as FlaskResponse

from constants import StatusCode
from db import db_instance
from db import exceptions


def cache_metadata(url, json_data):
    try:
        db_instance.DbInstance.db.add_value(url, json_data)
    except exceptions.MagpieDbError:
        # TODO: Log database error
        return


def get_cached_data_from_db(url):
    try:
        data = db_instance.DbInstance.db.get_metadata(url)
        if data.metadata is not None:
            response = FlaskResponse(response=data.metadata, status=StatusCode.OK, mimetype="application/json")
            return response
    except db_instance.MagpieDbError:
        # TODO: Log this error somewhere
        return None
    return None
