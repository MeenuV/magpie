import requests

request_url = "http://www.youtube.com/oembed?url="

def scrape(url):
    request = request_url + url
    response = requests.get(request)
    data = response.json()
    print "Image: {0}".format(data["thumbnail_url"])
    print "Title: {0}".format(data["title"])
    print "HTML: {0}".format(data["html"])

# For testing purposes:
# Remove later if needed
if __name__ == "__main__":
    scrape("https://www.youtube.com/watch?v=ptOLEwYrrEc")
