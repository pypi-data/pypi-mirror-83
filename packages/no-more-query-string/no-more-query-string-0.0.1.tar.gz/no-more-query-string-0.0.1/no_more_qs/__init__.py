from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup
from tld import get_fld
from w3lib.url import url_query_cleaner


class NoMoreQS:
    def __init__(self,
                 include_flds: Union[List[str], Tuple[str]] = [],
                 exclude_flds: Union[List[str], Tuple[str]] = [],
                 strict: bool = True):
        self.include_flds = include_flds
        self.exclude_flds = exclude_flds
        self.strict = strict

    def clean(self, url: str, allow_og_url: bool = False, *args, **kwargs) -> str:
        fld = get_fld(url)

        cleaner = _super_cleaner if self.strict else _fbclid_remover

        is_allowed_fld = fld in self.exclude_flds
        is_not_allowed_fld = fld in self.include_flds

        if is_allowed_fld:
            cleaner = _fbclid_remover

        if is_not_allowed_fld:
            cleaner = _super_cleaner

        return cleaner(url, allow_og_url, *args, **kwargs)

    @staticmethod
    def remove_fbclid(url: str):
        return _fbclid_remover(url)


def _super_cleaner(url: str, allow_og_url: bool = False, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    page = BeautifulSoup(response.text, "lxml")

    canonical_url = _get_canonical_url(page)
    if canonical_url:
        return canonical_url

    if allow_og_url:
        og_url = _get_og_url(page)
        if og_url:
            return og_url

    return _fbclid_remover(url)


def _fbclid_remover(url: str, *args, **kwargs) -> str:
    url = url_query_cleaner(url, ("fbclid"), remove=True)
    return url


def _get_canonical_url(page) -> str:
    canonical_url = page.select_one("link[rel='canonical']")
    if canonical_url:
        return canonical_url["href"]
    return ''


def _get_og_url(page) -> str:
    og_url = page.select_one("meta[property='og:url']")
    if og_url:
        return og_url["content"]
    return ''
