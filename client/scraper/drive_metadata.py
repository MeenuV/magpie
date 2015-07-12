from client import config
from metadata import Metadata
import json
import requests
import re

request_url = "https://www.googleapis.com/drive/v2/files/"


class DriveMetadata(Metadata):
    prop_map = {}

    def get_json_response(self, document_id):
        response = requests.get(request_url + document_id + "?key=" + config.drive_api_key)
        return response.json()

    def parse_content(self, response):

        m = re.search(r"([-\w]{25,})", response.url)
        document_id = m.group()

        response_json = self.get_json_response(document_id)

        if response_json.get("error"):
            return self.to_json(response_json)

        self.prop_map["title"] = response_json["title"]
        self.prop_map["image"] = response_json["iconLink"]
        self.prop_map["ownerNames"] = response_json["ownerNames"]

        return self.to_json(self.prop_map)

    def to_json(self, prop_map):
        return json.dumps(prop_map)
