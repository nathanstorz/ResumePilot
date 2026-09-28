import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)


def extract_with_requests(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    return clean_text(response.text)


def extract_with_playwright(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()

        try:
            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            main_text = page.locator("body").inner_text()

            iframe_text = ""

            for frame in page.frames:
                if frame == page.main_frame:
                    continue

                try:
                    iframe_text += "\n" + frame.locator("body").inner_text()
                except Exception:
                    pass

            return main_text + iframe_text

        finally:
            browser.close()


def extract_job_page(url: str):
    try:
        text = extract_with_requests(url)

        if len(text.strip()) > 500:
            from app.services.llm_service import contains_job_description

            if contains_job_description(text):
                return text

    except Exception:
        pass

    try:
        return extract_with_playwright(url)

    except Exception:
        return ""