import unittest
import json
from mock import patch
from client.scraper.drive_metadata import DriveMetadata
from client.response import Response
from client.constants import UrlTypes


class TestDriveMetadata(unittest.TestCase):

    doc_url = "https://docs.google.com/document/d/1FUo-Him4W6qR96_a6Ftx8skefgAe1vHjDPCfUIxtADM/edit"

    @patch.object(DriveMetadata, 'get_json_response')
    def test_drive(self, response_json):
        with open("test/mocks/drive.json", "r") as testFile:
            data = testFile.read().replace('\n', '')

        response_json.return_value = json.loads(data)
        scraper = DriveMetadata()

        url_data = Response()
        url_data.set_content("", data, "", self.doc_url, UrlTypes.DRIVE)

        response = json.loads(scraper.parse_content(url_data))
        self.assertEqual(response.get("title"), "Dummy page")
        self.assertEqual(response.get("ownerNames"), ["Samiya Akhtar"])

if __name__ == '__main__':
    unittest.main()
