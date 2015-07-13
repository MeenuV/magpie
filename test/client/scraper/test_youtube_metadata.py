import unittest
import json
from mock import patch
from client.scraper.youtube_metadata import YoutubeMetadata
from client.response import Response
from client.constants import UrlTypes


class TestYoutubeMetadata(unittest.TestCase):

    @patch.object(YoutubeMetadata, 'get_json_response')
    def test_drive(self, response_json):
        with open("test/mocks/youtube.json", "r") as testFile:
            data = testFile.read()

        response_json.return_value = json.loads(data)
        scraper = YoutubeMetadata()

        url_data = Response()
        url_data.set_content("", data, "", "", UrlTypes.YOUTUBE)

        response = json.loads(scraper.parse_content(url_data))
        self.assertEqual(response.get("title"), "Cutest Baby Talk Ever!")

if __name__ == '__main__':
    unittest.main()
