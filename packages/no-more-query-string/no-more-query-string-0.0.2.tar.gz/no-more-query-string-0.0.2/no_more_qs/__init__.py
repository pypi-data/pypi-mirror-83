from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup
from tld import get_fld
from w3lib.url import url_query_cleaner

__author__ = "Elton H.Y. Chou"

__license__ = "MIT"
__version__ = "0.0.2-beta"
__maintainer__ = "Elton H.Y. Chou"
__email__ = "plscd748@gmail.com"


class NoMoreQS:
    """No more query string"""

    def __init__(self,
                 include_flds: Union[List[str], Tuple[str]] = [],
                 exclude_flds: Union[List[str], Tuple[str]] = [],
                 strict: bool = True):
        """
        Parameters
        ----------
        include_flds : Union[List[str], Tuple[str]], optional
            first-level domains list which are allowed to clean query string., by default []

        exclude_flds : Union[List[str], Tuple[str]], optional
            first-level domains which are disallowed to clean query string., by default []

        strict : bool, optional
            mode of clean, by default True
        """
        self.include_flds = include_flds
        self.exclude_flds = exclude_flds
        self.strict = strict

    def clean(self, url: str, allow_og_url: bool = False, **kwargs) -> str:
        """
        clean

        Parameters
        ----------
        url : str
            Any useable url.

        allow_og_url : bool, optional
            return og-url if page can't find canonical-url, by default False

        kwargs : dict, optional
            Optional arguments that ``request`` takes

        Returns
        -------
        str
            cleaned url, fbclid is always be cleaned.
        """
        fld = get_fld(url)

        cleaner = _super_cleaner if self.strict else _fbclid_cleaner

        is_allowed_fld = fld in self.exclude_flds
        if is_allowed_fld:
            cleaner = _fbclid_cleaner

        is_not_allowed_fld = fld in self.include_flds
        if is_not_allowed_fld:
            cleaner = _super_cleaner

        return cleaner(url, allow_og_url, **kwargs)

    @staticmethod
    def remove_fbclid(url: str) -> str:
        """
        remove fbclid
        if you affraid the power of super cleaner,
        you can just clean the fbclid easily with thie method.

        Parameters
        ----------
        url : str
            Any useable url.

        Returns
        -------
        str
            cleaned url, fbclid is always be cleaned.
        """
        return _fbclid_cleaner(url)


def _super_cleaner(url: str, allow_og_url: bool = False, **kwargs):
    """
    super cleaner

    Parameters
    ----------
    url : str
        Any useable url.

    allow_og_url : bool, optional
        return og-url if page can't find canonical-url, by default False

    kwargs : dict, optional
        Optional arguments that ``request`` takes.

    Returns
    -------
    str
        cleaned url, fbclid is always be cleaned.
    """
    response = requests.get(url, **kwargs)

    if response.status_code > 400:
        return _fbclid_cleaner(url)

    page = BeautifulSoup(response.text, "lxml")

    canonical_url = _get_canonical_url(page)
    if canonical_url:
        return canonical_url

    if allow_og_url:
        og_url = _get_og_url(page)
        if og_url:
            return og_url

    return _fbclid_cleaner(url)


def _fbclid_cleaner(url: str, *args, **kwargs) -> str:
    """
    [summary]

    Parameters
    ----------
    url : str
        Any useable url.

    Returns
    -------
    str
        cleaned url, fbclid is always be cleaned.
    """
    url = url_query_cleaner(url, ("fbclid"), remove=True)
    return url


def _get_canonical_url(page: BeautifulSoup) -> str:
    """
    get canonical url

    Parameters
    ----------
    page : BeautifulSoup
        BeautiifulSoup object

    Returns
    -------
    str
        link[canonical url]
    """
    canonical_url = page.select_one("link[rel='canonical']")
    if canonical_url:
        return canonical_url["href"]
    return ''


def _get_og_url(page: BeautifulSoup) -> str:
    """
    get og:url

    Parameters
    ----------
    page : BeautifulSoup
        BeautiifulSoup object

    Returns
    -------
    str
        meta[og:url]
    """
    og_url = page.select_one("meta[property='og:url']")
    if og_url:
        return og_url["content"]
    return ''
