"""
Assignment 8 — get_books.py
Scrapes search results from Durham County Library (BiblioCommons) for the
query "learning spanish" and saves the data to CSV and JSON.

Tasks covered:
  Task 3 — Extract book data (title, author(s), format-year)
  Task 4 — Write data out to CSV and JSON

Diagnostic mode:
  If the script finds the result <li>s but can't pull a Title out of the
  first one, it dumps the innerHTML of that first <li> and exits. Paste
  that HTML to me and I'll fix the inner selectors. Without that diagnostic,
  failures look like silent empty strings.
"""

import json
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


SEARCH_URL = (
    "https://durhamcounty.bibliocommons.com/v2/search"
    "?query=learning%20spanish&searchType=smart"
)


# ----- driver setup ---------------------------------------------------------

def make_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )


# ----- robust field extraction ---------------------------------------------
#
# For each field (title, author, format-year) we try a list of candidate CSS
# selectors in order; the first one that finds something wins. This way the
# script is resilient if BiblioCommons changes one class name.

TITLE_SELECTORS = [
    "span.title-content",
    'span[testid="bib_link"]',
    "a.title",
    "h2 a",
]

AUTHOR_SELECTORS = [
    "a.author-link",
    'a[testid="author_search"]',
    ".author-link",
]

# The format/year text (e.g. "Book - 2018") lives in one of these:
FORMAT_SELECTORS = [
    "span.display-info-primary",
    "div.cp-format-info span",
    ".format-info",
    "span.cp-format",
]


def first_text(parent, selectors):
    """Try each CSS selector; return the text of the first match, or ''."""
    for sel in selectors:
        try:
            el = parent.find_element(By.CSS_SELECTOR, sel)
            text = el.text.strip()
            if text:
                return text
        except NoSuchElementException:
            continue
    return ""


def all_texts(parent, selectors):
    """Try each CSS selector; return texts from the first selector that hits."""
    for sel in selectors:
        els = parent.find_elements(By.CSS_SELECTOR, sel)
        texts = [e.text.strip() for e in els if e.text.strip()]
        if texts:
            return texts
    return []


# ----- Task 3: scrape the results ------------------------------------------

def extract_books(driver):
    """
    Find every search-result <li> on the page and pull title / author /
    format-year out of each. Returns a list of dicts.

    Outer <li> selector (confirmed from dev-tools inspection of the actual page):
        li[data-test-id="searchResultItem"]
    """
    RESULT_LI = 'li[data-test-id="searchResultItem"]'

    # Give the JS-rendered results time to populate.
    time.sleep(3)

    items = driver.find_elements(By.CSS_SELECTOR, RESULT_LI)
    print(f"Found {len(items)} search-result entries on this page.")

    if len(items) == 0:
        # If we got zero items, BiblioCommons may have changed the outer
        # selector — try a fallback.
        items = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
        print(f"Fallback selector found {len(items)} entries.")

    if len(items) == 0:
        print("\nNo results found. Dumping the <body> outer HTML so you can")
        print("paste it back to me to fix the outer selector:")
        body = driver.find_element(By.TAG_NAME, "body")
        print(body.get_attribute("outerHTML")[:3000])
        return []

    # Diagnostic: try extracting the title from the FIRST item only. If that
    # fails, dump the item's HTML and abort — there's no point processing
    # the rest with broken selectors.
    first_title = first_text(items[0], TITLE_SELECTORS)
    if not first_title:
        print("\n!! Could not find the title in the first result. !!")
        print("Inner HTML of the first <li> (paste this back to me):\n")
        print(items[0].get_attribute("innerHTML"))
        return []

    print(f"Sanity check OK — first title: {first_title!r}")

    results = []
    for i, item in enumerate(items, start=1):
        title = first_text(item, TITLE_SELECTORS)

        # Authors: may be 0, 1, or many. Join multiple with '; '.
        authors = all_texts(item, AUTHOR_SELECTORS)
        author = "; ".join(authors)

        format_year = first_text(item, FORMAT_SELECTORS)

        entry = {
            "Title": title,
            "Author": author,
            "Format-Year": format_year,
        }
        results.append(entry)

        # Incremental print so you can sanity-check each row as it's scraped.
        print(f"  [{i:>2}] {entry}")

    return results


# ----- Task 4: write the data out ------------------------------------------

def save_csv(df: pd.DataFrame, path: str = "get_books.csv"):
    df.to_csv(path, index=False)
    print(f"Wrote {len(df)} rows to {path}")


def save_json(results: list, path: str = "get_books.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Wrote {len(results)} entries to {path}")


def main():
    driver = make_driver(headless=True)
    try:
        print(f"Loading: {SEARCH_URL}")
        driver.get(SEARCH_URL)

        results = extract_books(driver)

        if not results:
            print("No results extracted — nothing to write.")
            return

        df = pd.DataFrame(results)
        print("\n--- DataFrame ---")
        print(df)

        save_csv(df, "get_books.csv")
        save_json(results, "get_books.json")

    except Exception as e:
        print(f"Exception: {type(e).__name__} {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
