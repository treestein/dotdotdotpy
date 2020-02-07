import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import logging

log = logging.getLogger(__name__)

class XDGSupportApplication:
    
    def __init__(self, name: str, legacy_paths: list):
        self.name = name
        self.legacy_paths = legacy_paths

    def get_feedback(self):
        for path in self.legacy_paths:
            path = path.replace("~", os.environ["HOME"])
            if os.path.isfile(path):
                return f"LEGACY: {self.name} - {path}."


class XDGSupportArchWiki:

    URL = "http://wiki.archlinux.org/index.php/XDG_Base_Directory"

    def __init__(self):
        log.info(f"Scraping {XDGSupportArchWiki.URL}")
        with closing(get(XDGSupportArchWiki.URL, stream=True)) as response:
            log.info("Received Response")
            if self.is_good_response(response):
                content = response.content
                log.info("Success")
            else:
                log.error("Invalid response")
                raise Exception("Invalid response")
        self._html = BeautifulSoup(content, "html.parser")

    def get_xdg_applications(self) -> list:
        xdg_apps = []
        tables = self._html.findAll(
                "table", {
                    "class": "wikitable"
                    }
                )
        for table in tables:
            for tr in table.find("tbody").findAll("tr"):
                xdg_apps.append(XDGSupportArchWiki.extract_row(tr))
        return xdg_apps

    @staticmethod
    def extract_row(tr):
        try:
            td = tr.findAll("td")
            name = td[0].find("a").contents[0].strip("\n")
            path = td[1].find("code").contents
            paths = []
            for p in path:
                p = str(p)
                if "<br/>" not in p:
                    paths.append(p.strip("\n"))
            return XDGSupportApplication(name, paths)
                
        except Exception as e:
            pass


    @staticmethod
    def is_good_response(response: object):
        content_type = response.headers["Content-Type"].lower()
        return (response.status_code == 200
                and content_type is not None
                and content_type.find("html") > -1)


if __name__ == "__main__":
    applications = XDGSupportArchWiki().get_xdg_applications()
    print(f"TOTAL: {len(applications)}")
    for application in applications:
        if type(application) is XDGSupportApplication:
            feedback = application.get_feedback()
            if feedback:
                print(feedback)
