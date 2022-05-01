from typing import List

import httpx

from .constants import API_URL, USER_AGENT

# https://www.mediawiki.org/wiki/API:Query


def search(title, lang="en"):
    """Return
    `{"data":[{ns, title, pageid, size, wordcount, snippet, timestamp}]}` or
    `{"error":"message"}`
    """
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
    }

    rsp = _request(params, lang)

    if rsp.get("error"):
        return rsp
    data = rsp.get("query").get("search", [])
    return {"data": data}


def page(pageid, lang, props_list: List[str]):
    """
    Arguments:
        props_list: Which properties to get for the queried pages.

    Return
    `{"data":[{ns, title, pageid, url, prop1, prop2, ...}]}` or
    `{"error":"message"}`
    """
    params = {
        "action": "query",
        "prop": "|".join(props_list),
        "pageids": pageid,
    }
    # https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&pageids=19450

    rsp = _request(params, lang)

    if rsp.get("error"):
        return rsp
    data = rsp.get("query").get("pages", {}).get(pageid, {})
    data["url"] = _get_page_url(data.get("title"), lang)
    return {"data": data}


def _get_page_url(title, lang):
    return f"https://{lang}.wikipedia.org/wiki/{title}"


def _request(params, lang="en"):
    url = API_URL.replace("{lang}", lang)
    headers = {"User-Agent": USER_AGENT}
    params["format"] = "json"
    params["origin"] = "*"
    try:
        response = httpx.get(url, params=params, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": f"{response.status_code} - {response.reason_phrase}: {str(e)}"}
