import urllib.request


def access_to(url: str):
    # trying to open
    try:
        urllib.request.urlopen(url)
        return True
    # trying to catch exception when internet is not ON.
    except:
        return False

def get_release(release_: str)->str:

    response = urllib.request.urlopen(release_)
    if not response.status == 200:
        print("The git releases url below is not available. Please check:")
        print(release_)
        exit()

    latest_release = response.url.split("tag/v")[1]
    return latest_release

