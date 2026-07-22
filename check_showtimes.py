import os
import re
import sys

import requests
from playwright.sync_api import sync_playwright

# ---- Configuration -------------------------------------------------------

URL = "https://egy.voxcinemas.com/showtimes?c=city-centre-almaza&m=the-odyssey&d=20260724"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "")
STATE_FILE = "state.txt"

NOT_AVAILABLE_TEXT = "No showtimes could be found"
TIME_PATTERN = re.compile(r"\b\d{1,2}:\d{2}\s?(AM|PM)\b", re.IGNORECASE)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

# ---- Helpers --------------------------------------------------------------


def fetch_page_text() -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-http2"])
        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1366, "height": 900},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        page = context.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        # Give the client-side app time to fetch and render showtimes
        page.wait_for_timeout(8000)
        content = page.inner_text("body")
        browser.close()
    return content


def is_available(page_text: str) -> bool:
    if NOT_AVAILABLE_TEXT in page_text:
        return False
    return bool(TIME_PATTERN.search(page_text))


def send_notification():
    if not NTFY_TOPIC:
        print("NTFY_TOPIC not set, skipping notification (but showtimes ARE available!)")
        return
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data="Friday showtimes for The Odyssey (VOX City Centre Almaza) are open. Book now!".encode("utf-8"),
        headers={
            "Title": "VOX showtimes open!",
            "Priority": "urgent",
            "Tags": "movie_camera,tada",
        },
        timeout=15,
    )
    print("Notification sent.")


def read_state() -> str:
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE).read().strip()
    return "waiting"


def write_state(state: str):
    with open(STATE_FILE, "w") as f:
        f.write(state)


def main():
    try:
        text = fetch_page_text()
    except Exception as e:
        print(f"Error loading page: {e}", file=sys.stderr)
        sys.exit(1)

    available = is_available(text)
    state = read_state()
    print(f"available={available} current_state={state}")

    if available and state != "notified":
        send_notification()
        write_state("notified")
    elif not available and state == "notified":
        # Went back to unavailable (e.g. date rolled over) - reset so we'd notify again
        write_state("waiting")


if __name__ == "__main__":
    main()
