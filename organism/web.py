"""Polite web ingestion — how the organism "feeds" on the internet.

Good manners are not optional: we honour robots.txt, set an honest User-Agent,
rate-limit ourselves, and cap how much we read. Uses only the standard library
so it runs anywhere; if `requests` is installed it will be used automatically.
"""
from __future__ import annotations

import time
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urlparse

from . import config

try:  # optional nicety
    import requests  # type: ignore
    _HAVE_REQUESTS = True
except Exception:  # pragma: no cover
    _HAVE_REQUESTS = False

_last_fetch: dict[str, float] = {}


class _TextExtractor(HTMLParser):
    """Strips tags and pulls out human-readable text + the page title."""

    _SKIP = {"script", "style", "noscript", "head", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self.chunks: list[str] = []
        self.title = ""
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title and not self.title:
            self.title = text
        self.chunks.append(text)


def _allowed(url: str) -> bool:
    """Ask the site's robots.txt whether our agent may fetch this URL."""
    try:
        parts = urlparse(url)
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(config.USER_AGENT, url)
    except Exception:
        # If robots.txt can't be read, err on the side of being allowed but polite.
        return True


def _throttle(host: str) -> None:
    last = _last_fetch.get(host, 0.0)
    wait = config.CRAWL_DELAY_SECONDS - (time.time() - last)
    if wait > 0:
        time.sleep(wait)
    _last_fetch[host] = time.time()


def _raw_get(url: str) -> str:
    headers = {"User-Agent": config.USER_AGENT}
    if _HAVE_REQUESTS:
        resp = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text[: config.MAX_PAGE_BYTES]
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=config.REQUEST_TIMEOUT) as r:
        raw = r.read(config.MAX_PAGE_BYTES)
    return raw.decode("utf-8", errors="replace")


def fetch(url: str) -> dict:
    """Fetch and clean a page. Returns {ok, title, text, error}."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    host = urlparse(url).netloc

    if not _allowed(url):
        return {"ok": False, "error": f"robots.txt disallows fetching {url}", "url": url}

    _throttle(host)
    try:
        html = _raw_get(url)
    except Exception as e:  # network, http error, etc.
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "url": url}

    parser = _TextExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass
    text = "\n".join(parser.chunks)
    return {"ok": True, "title": parser.title or host, "text": text, "url": url}
