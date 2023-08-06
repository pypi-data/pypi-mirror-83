"""
    philomena.philomena
    ~~~~~~~~~

    This module implements the core elements of this library, namely, the
    orchestrator.

"""
import collections.abc
import http
import typing
from abc import ABC
from abc import abstractmethod
from collections.abc import Container

import requests


# TODO: implement for acceptance testing with selenium
# from selenium import webdriver
# from selenium.webdriver import FirefoxOptions
# from webdriver_manager.firefox import GeckoDriverManager
# from bs4 import BeautifulSoup

# class Soup:
#     """Beautiful Soup implementation for html"""
#
#     def __init__(self, html):
#         self.soup = BeautifulSoup(html)
#
#
class HTML:
    """Abstraction for a HTML element document"""

    def __init__(self, html):
        self.html = html
        # self.client = Soup(self.html)


#
#
# def get_web_driver(headless: bool = True) -> webdriver.Firefox:
#     firefox_options = FirefoxOptions()
#     # if headless:
#     #     firefox_options.add_argument("--headless")
#     web_driver = webdriver.Firefox(
#         executable_path=GeckoDriverManager().install(), options=firefox_options
#     )
#     web_driver.implicitly_wait(1)
#     return web_driver


class UnexpectedHTTPStatusCode(Exception):
    pass


class Page(Container):
    def __init__(self, content: str, url: str, status_code: int):

        # set html
        self.html = HTML(content)

        # set url
        self.url = url

        # set status code
        self.status_code = status_code

        # set http status
        try:
            self.http_status = http.HTTPStatus(self.status_code)
        except ValueError:
            raise ValueError("HTTP status code is not recognised by the http library.")

    @property
    def content(self):
        return self.html.html

    @property
    def informational_response(self):
        return str(self.status_code).startswith("1")

    @property
    def success(self):
        return str(self.status_code).startswith("2")

    @property
    def redirection(self):
        return str(self.status_code).startswith("3")

    @property
    def client_error(self):
        return str(self.status_code).startswith("4")

    @property
    def server_error(self):
        return str(self.status_code).startswith("5")

    def includes(self, includables: typing.Union[str, typing.Iterable]) -> bool:
        if isinstance(includables, str):
            return includables in self.content
        elif isinstance(includables, collections.abc.Iterable):
            return all([i in self.content for i in includables])
        else:
            raise ValueError("includables must be a sequence")

    def __contains__(self, item) -> bool:
        return self.includes(item)

    @classmethod
    def from_response(cls, response: requests.Response):
        page = cls(
            content=response.text, url=response.url, status_code=response.status_code
        )
        return page

    def __eq__(self, other):
        if isinstance(other, Page):
            return self.url == other.url and self.status_code == other.status_code
        else:
            return False


class BaseClient(ABC):
    """base client for browsing the web"""

    # @property
    # @abstractmethod
    # def follow_redirects(self):
    #     raise NotImplementedError()

    @abstractmethod
    def get(self, url):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()


class RequestsClient(BaseClient):
    """A backend client for requests."""

    def __init__(self, follow_redirects: bool = True):
        self._client = requests.Session()
        self._follow_redirects = follow_redirects

    @property
    def follow_redirects(self):
        return self._follow_redirects

    def _get(self, url: str):
        return self._client.get(url, allow_redirects=self.follow_redirects)

    def get(self, url: str):
        resp = self._get(url)
        return Page.from_response(resp)

    def close(self):
        self._client.close()


# class SeleniumClient(BaseClient):
#     def __init__(self):
#         self._client = get_web_driver()
#
#     @property
#     def follow_redirects(self):
#         return True
#
#     def _get(self, url):
#         return self._client.get(url)
#
#     def get(self, url):
#         resp = self._get(url)
#         return Page.from_response(resp)
#
#     def set_up(self):
#         return self
#
#     def tear_down(self):
#         return self._client.close()


class Orchestrator:
    """Core element to the package that visits the web page using whichever
    backend client is used, e.g. requests (and TODO: selenium)

    How to use:
        orchestrator = Orchestrator()
        # this is a test
        orchestrator.visit("https://www.google.com")



    :param client: the name of the browser client e.g. request
    :type: str

    :param host: the url of all routes to be tested by the orchestrator
    :type: str

    :param follow_redirects: whether to follow redirects, when the client is
                             redirected
    :type: bool
    """

    def __init__(
        self, client: str = "requests", host: str = None, follow_redirects: bool = True
    ):

        # set client
        if client.lower() == "requests":
            self.client = RequestsClient(follow_redirects=follow_redirects)
        # elif client.lower() == "selenium":
        #     self._client = SeleniumClient
        else:
            raise ValueError("You can only use requests or selenium right now")

        self.follow_redirects = follow_redirects

        # calling str allows use of url libs that have __str__ method
        # this could be better: TODO: custom URL class?
        if host:
            self.host = str(host)[:-1] if str(host).endswith("/") else str(host)
        else:
            self.host = None

        # save page states
        self._current_page = None
        self._pages = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.client.close()

    def _get_url(self, url):
        if self.host:
            if not url.startswith("/"):
                raise ValueError(
                    "URL paths, when a host is set, must start with a leading slash: /"
                )
            else:
                return self.host + url
        else:
            return url

    def _set_current_page(self, page):
        self._current_page = page
        self._pages.append(page)

    def visit(self, url: str, expected: int = 200):
        try:
            status = http.HTTPStatus(expected)
        except ValueError:
            raise ValueError("HTTP status code is not recognised by the http library.")

        page = self.client.get(self._get_url(url))

        if page.status_code == expected:
            self._set_current_page(page)
            return page
        else:
            raise UnexpectedHTTPStatusCode(
                f"\n"
                f'You expected: {expected} {status.phrase} - "{status.description}"\n'
                f'You received: {page.status_code} {page.http_status.phrase} - "{page.http_status.description}"\n'
                "Because:\n"
                f"{page.content}"
            )
