from pathlib import Path
from typing import NoReturn
from urllib.request import urlopen, Request

from utils import collect_urls

VOTING_CLASS = b"fa fa-chevron-up"
ITEM_URLS_PATH = "item-urls.txt"


def main() -> NoReturn:
    item_urls_path = Path(ITEM_URLS_PATH)
    if not item_urls_path.exists() or not item_urls_path.is_file():
        collect_urls(ITEM_URLS_PATH)
    with open(ITEM_URLS_PATH, 'r') as f:
        item_urls = [line.rstrip("\n") for line in f.readlines()]
        for item_url in item_urls:
            req = Request(url=item_url, headers={"User-Agent": "Mozilla/5.0"})
            webpage = urlopen(req).read()
            if VOTING_CLASS in webpage:
                print(item_url)


if __name__ == "__main__":
    main()
