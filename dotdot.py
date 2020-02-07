import os.path
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


class XDGSupportApplication:
    
    def __init__(self, name: str, legacy_path: str):
        self.name = name
        self.legacy_path = legacy_path

    def get_feedback(self):
        legacy = self.find_if_legacy_file()
        if os.path.isfile(self.legacy_path):
            return f"LEGACY: {self.name} - {legacy}."

    def __str__(self):
        return self.get_feedback()


class XDGSupportArchWiki:

    URL = "https://wiki.archlinux.org/index.php/XDG_Base_Directory"

    def __init__(self):
        with closing(get(XDGSupportArchWiki.URL, stream=True)) as response:
            if is_good_response(response):
                self.content = response.content

    def get_xdg_applications(self) -> list:
        return self.get_supported_xdg_applications() + \
                self.get_partial_xdg_applications() + \
                self.get_hardcoded_xdg_applications()

    def get_supported_xdg_applications(self) -> list:
        return []

    def get_partial_xdg_applications(self) -> list:
        return []

    def get_hardcoded_xdg_applications(self) -> list:
        return []


    @staticmethod
    def is_good_response(response: object):
        content_type = response.header["Content-Type"].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find("html") > -1)


if __name__ == "__main__":
    applications = XDGSupportArchWiki().get_xdg_applications()
    for application in applications:
        if type(application) is XDGSupportApplication:
            print(application)
