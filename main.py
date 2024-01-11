#!/usr/bin/python
# -*- coding: utf-8 -*-
# License: GPLv3 Copyright: 2024, wheynelau

import logging
import os
import urllib.request
from typing import Any, Dict, List

import calibre_plugins.arxiv.xmltodict as xmltodict
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from qt.core import QUrl

LOGS_PATH = os.path.join("logs", "logs.txt")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

os.makedirs(os.path.dirname(LOGS_PATH), exist_ok=True)

file_handler = logging.FileHandler(LOGS_PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def requests_get(url: str, timeout: int = 30):
    try:
        # TODO: Best solution is using requests library, but it is not available in calibre
        # urlencode was giving issues as well
        with urllib.request.urlopen(
            url.replace(" ", "%20"), timeout=timeout
        ) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")
        return None


class ArxivStorePlugin(BasicStoreConfig, StorePlugin):
    def open(self, parent=None, detail_item=None, external=False):
        url = "www.arxiv.org"

        if external or self.config.get("open_external", False):
            open_url(QUrl(detail_item if detail_item else url))
        else:
            d = WebStoreDialog(
                self.gui, url, parent, detail_item, create_browser=self.create_browser
            )
            d.setWindowTitle("Arxiv")
            d.set_tags(self.config.get("tags", ""))
            d.exec()

    def search(
        self, query: str, max_results: int = 10, timeout: int = 10
    ) -> List[Dict]:
        # The logging can be cleaned up

        logger.debug("Searching for: {}".format(query))
        logger.debug("Query type: {}".format(type(query)))
        # The input query is a bytes object, so it needs to be decoded
        # Ex: b'quantum' -> 'quantum'

        if isinstance(query, bytes):
            query = query.decode("utf-8")
        logger.info("Query type: {}".format(type(query)))

        # default search is hardcoded
        url = "http://export.arxiv.org/api/query?search_query=ti:{}".format(
            query
        ) + "&sortBy=relevance&start=0&max_results={}".format(max_results)
        logger.debug("URL: {}".format(url))
        responses = requests_get(url=url, timeout=timeout)
        xml = xmltodict.parse(responses)
        logger.debug("XML: {}".format(len(xml["feed"]["entry"])))
        for result in xml["feed"]["entry"][:max_results]:
            res = self._build_search_result(result)
            logger.debug("Result: {}".format(res.title))
            yield res

    def _build_search_result(self, result: Dict[str, Any]) -> SearchResult:
        # this try except was for debugging, suggest to leave till finalised
        try:
            search_res = SearchResult()
            search_res.store_name = "arxiv"
            search_res.title = result["title"]
            if isinstance(result["author"], dict):
                search_res.author = result["author"]["name"]
            else:
                search_res.author = ", ".join(
                    [author["name"] for author in result["author"]]
                )
            search_res.formats = "PDF"
            search_res.downloads = {"PDF": self._get_link(result["link"], pdf=True)}
            search_res.detail_item = self._get_link(result["link"], pdf=False)
            search_res.drm = search_res.DRM_UNLOCKED
            return search_res
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            exit(1)

    @staticmethod
    def _get_link(links: List[Dict], pdf: bool = True) -> str:
        """
        Returns the link to the pdf or the abstract

        :param links: list of links
        :param pdf: boolean, true if pdf link is required

        :return: link to pdf or abstract
        """
        # returns the link to the pdf or the abstract
        for link in links:
            if link.get("@title") == "pdf" and pdf:
                return link["@href"] + ".pdf"
            elif "/abs/" in link.get("@href") and not pdf:
                return link["@href"]
