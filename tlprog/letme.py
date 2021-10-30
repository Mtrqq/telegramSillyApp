from urllib.parse import urlencode

API_ROOT = "https://googlethatforyou.com"


def prepare_google_url(query: str) -> str:
    params = urlencode({"q": query})
    return f"{API_ROOT}/?{params}"
