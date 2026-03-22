from scrapling.fetchers import StealthySession
from scrapling.engines.toolbelt.custom import Response
import json


def fetch_url(session, url: str) -> Response:
    page = session.fetch(url)
    if page.status == 200:
        return page

    raise ValueError(f"Failed to fetch {url}: {page.status}")

def main():

    with open("config.json", "r") as f:
        config = json.load(f)

    search_url = config["restaurant_url"]
    date = config["date"]
    preferred_times = config["preferred_times"]

    extra_head = {
        "X-Resy-Auth-Token": config["X-Resy-Auth-Token"], 
        "X-Resy-Universal-Auth": config["X-Resy-Universal-Auth"],
        "Authorization": config["Authorization"]
    }
    
    with StealthySession(
        headless=False,
        real_chrome=True,
        block_webrtc=True,
        solve_cloudflare=True,
        google_search=False,
        extra_headers=extra_head,
        useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    ) as session:
        
        page = fetch_url(session, search_url)
        links = page.css("button.ReservationButton.Button.Button--primary")
        
        valid_links = [link for link in links if link.attrib["data-testid"].split("/")[6] in preferred_times]

if __name__ == "__main__":
    main()
