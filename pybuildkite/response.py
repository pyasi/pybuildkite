from urllib.parse import urlparse


class Response:
    """
    Response object used for pagination requests
    """

    def __init__(self, body):
        self.body = body
        self.next_page = None
        self.last_page = None
        self.first_page = None
        self.previous_page = None

    def append_pagination_data(self, response_headers):
        """
        Add pagination data to the response based on response headers
        :param respone_headers: dict containing pagination information from the API
        """
        if "Link" in response_headers and len(response_headers["Link"]) > 0:
            for link in response_headers["Link"].split(", "):
                url, page_value = link.split("; ", 1)
                if page_value == 'rel="next"':
                    self.next_page = self._get_page_number_from_url(url)
                elif page_value == 'rel="last"':
                    self.last_page = self._get_page_number_from_url(url)
                elif page_value == 'rel="first"':
                    self.first_page = self._get_page_number_from_url(url)
                elif page_value == 'rel="prev"':
                    self.previous_page = self._get_page_number_from_url(url)
        return self

    def _get_page_number_from_url(self, url):
        """
        Gets the page number for pagination from a given url
        :param url: url to retrieve page from
        :return: int of page in url
        """
        parsed = urlparse(url)
        query_string = parsed.query
        for segment in query_string.split("&"):
            key, value = segment.split("=", 1)
            if key == "page":
                return int(value)
        return 0