# Wikipedia API Docs: https://www.mediawiki.org/wiki/API:Main_page
API_URL = "https://{lang}.wikipedia.org/w/api.php"
USER_AGENT = "oogway/wikipedia"


class PAGE_PROPS:
    """https://www.mediawiki.org/wiki/API:Query"""

    categories = "categories"
    categoryinfo = "categoryinfo"
    cirrusbuilddoc = "cirrusbuilddoc"
    cirruscompsuggestbuilddoc = "cirruscompsuggestbuilddoc"
    cirrusdoc = "cirrusdoc"
    contributors = "contributors"
    deletedrevisions = "deletedrevisions"
    duplicatefiles = "duplicatefiles"
    extlinks = "extlinks"
    extracts = "extracts"
    fileusage = "fileusage"
    globalusage = "globalusage"
    imageinfo = "imageinfo"
    images = "images"
    info = "info"
    iwlinks = "iwlinks"
    langlinks = "langlinks"
    links = "links"
    linkshere = "linkshere"
    mmcontent = "mmcontent"
    pageimages = "pageimages"
    pageprops = "pageprops"
    pageterms = "pageterms"
    pageviews = "pageviews"
    redirects = "redirects"
    revisions = "revisions"
    stashimageinfo = "stashimageinfo"
    templates = "templates"
    transcludedin = "transcludedin"
    transcodestatus = "transcodestatus"
    videoinfo = "videoinfo"
    wbentityusage = "wbentityusage"
    description = "description"