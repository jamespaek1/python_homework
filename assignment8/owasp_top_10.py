"""
Assignment 8 — owasp_top_10.py
Scrapes the OWASP Top 10 list and writes (Title, URL) pairs to a CSV file.

The OWASP project landing page at /www-project-top-ten/ now links out to the
current release page (/Top10/2025/) where the numbered list actually lives.
We load the release page directly and use XPath to traverse the DOM to the
"Top 10:2025 List" heading, then jump to the following ordered list and pull
each item.

Task covered:
  Task 6 — Scraping Structured Data with XPath
"""

import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


# The OWASP project landing page tells you to go here for the current list.
# If you prefer to start from the landing page, swap in
# "https://owasp.org/www-project-top-ten/" and the XPath below will still find
# the list because both pages render an <ol> of A01..A10 links.
URL = "https://owasp.org/Top10/2025/"


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


def extract_top_10(driver):
    """
    Use XPath to find the heading that introduces the Top 10 list, then walk
    over to its following <ol> sibling and pull each <li><a> entry.

    Why XPath: the page doesn't put a clean class or id on the list itself.
    What we *do* have is a heading whose text starts with "Top 10".  From that
    anchor we use the following-sibling axis to land on the <ol> immediately
    after it.
    """
    # 1. Find any heading element (h1/h2/h3) whose text starts with "Top 10".
    heading_xpath = (
        "//*[self::h1 or self::h2 or self::h3]"
        "[starts-with(normalize-space(.), 'Top 10')]"
    )
    try:
        heading = driver.find_element(By.XPATH, heading_xpath)
    except NoSuchElementException:
        # Fallback: just grab the first <ol> on the page that has 10 <li>s.
        heading = None

    if heading is not None:
        # 2. Walk to the next <ol> sibling after that heading.
        try:
            ol = heading.find_element(By.XPATH, "following-sibling::ol[1]")
        except NoSuchElementException:
            # Sometimes the <ol> is nested in a wrapper; broaden the search.
            ol = heading.find_element(By.XPATH, "following::ol[1]")
    else:
        ol = driver.find_element(By.XPATH, "//ol[count(li)=10][1]")

    # 3. Each <li> holds a single <a> whose text is the vulnerability title.
    link_els = ol.find_elements(By.XPATH, ".//li/a")

    results = []
    for a in link_els:
        title = a.text.strip()
        href = a.get_attribute("href")
        if title and href:
            results.append({"title": title, "url": href})

    return results


def save_csv(rows, path="owasp_top_10.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url"])
        for row in rows:
            writer.writerow([row["title"], row["url"]])
    print(f"Wrote {len(rows)} rows to {path}")


def main():
    driver = make_driver(headless=True)
    try:
        print(f"Loading: {URL}")
        driver.get(URL)
        time.sleep(2)  # be polite, let any JS finish

        top_10 = extract_top_10(driver)

        print(f"\nExtracted {len(top_10)} vulnerabilities:")
        for i, entry in enumerate(top_10, start=1):
            print(f"  {i:>2}. {entry['title']}")
            print(f"      {entry['url']}")

        save_csv(top_10, "owasp_top_10.csv")

    except Exception as e:
        print(f"Exception: {type(e).__name__} {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
