import json
import re
import urllib.error
import urllib.request

REPO = "jmyerston/greCy"
RELEASES_API_URL = f"https://api.github.com/repos/{REPO}/releases?per_page=100"
LATEST_RELEASE_URL = f"https://github.com/{REPO}/releases/latest"
DOWNLOAD_URL = f"https://github.com/{REPO}/releases/download"
TIMEOUT_SECONDS = 30

_LOOKUP_ERRORS = (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError)


class ModelNotFoundError(Exception):
    """No published greCy release contains a wheel for the model."""


class ReleaseLookupError(Exception):
    """GitHub could not be reached, so the available releases are unknown."""


def _open(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "grecy-installer"})
    return urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS)


def _wheel_url_from_api(model: str) -> str | None:
    """Return the wheel in the newest published release that contains the model."""
    with _open(RELEASES_API_URL) as response:
        releases = json.load(response)

    published = [r for r in releases if not r["draft"] and not r["prerelease"]]
    published.sort(key=lambda r: r["published_at"], reverse=True)

    wheel_name = re.compile(re.escape(model) + r"-[^-]+-.+\.whl")
    for release in published:
        for asset in release["assets"]:
            if wheel_name.fullmatch(asset["name"]):
                return asset["browser_download_url"]
    return None


def _wheel_url_from_latest_redirect(model: str) -> str:
    """Build the wheel URL from the tag that GitHub's latest-release page redirects to."""
    with _open(LATEST_RELEASE_URL) as response:
        tag = response.url.rsplit("/tag/", 1)[1]
    version = tag.removeprefix("v")
    return f"{DOWNLOAD_URL}/{tag}/{model}-{version}-py3-none-any.whl"


def find_wheel_url(model: str) -> str:
    """Find the download URL of the most recent wheel published for a model.

    The version comes from GitHub at install time, so a new model release does
    not need a new version of this package.
    """
    try:
        url = _wheel_url_from_api(model)
    except _LOOKUP_ERRORS:
        # Unauthenticated API requests are rate limited, so a failure here does
        # not mean GitHub is unreachable.
        try:
            return _wheel_url_from_latest_redirect(model)
        except (*_LOOKUP_ERRORS, IndexError) as error:
            raise ReleaseLookupError(str(error)) from error

    if url is None:
        raise ModelNotFoundError(model)
    return url
