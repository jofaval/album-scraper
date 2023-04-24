"""Request Utils"""

import logging

import cchardet
from requests import get
from validators import url as is_url


def is_valid_url(url: str) -> bool:
    """Detects if the URL is valid for a request"""
    return not url or not is_url(url)


def get_url_content(
    url: str,
    timeout: float = 25,
    should_retry: bool = True,
    retry_times: int = 3
):
    """Retrieves the URL's content"""
    if is_valid_url(url):
        return None

    # https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending?sort=dont-sort
    headers = {
        # "Content-Type": "",
        # "Content-Length": "",
        # "Host": "www.whatismybrowser.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        # "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Referer": "https://www.google.com/",
        # "Upgrade-Insecure-Requests": "1",
        # "Sec-Fetch-Dest": "document",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "same-origin",
        # "Sec-Fetch-User": "?1",
        # "Sec-Gpc": "1",
        # "Te": "trailers",
    }

    # -1 implements a pseudo do-while
    max_retry = retry_times if should_retry else -1
    retry_attempt = 0

    while True:
        if retry_attempt >= 1:
            logging.warning(
                "Retrying %s for the %d failed attempt(s)", url, retry_attempt
            )

        try:
            response = get(
                url,
                timeout=timeout,
                headers=headers,
                allow_redirects=True
            )

            if not response.ok:
                raise Exception(f'Response for "{url}" failed')

            return response.content
        except Exception as error:
            logging.exception(error)
        finally:
            retry_attempt += 1
            if retry_attempt >= max_retry:
                break

        return None
