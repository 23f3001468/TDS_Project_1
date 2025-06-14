from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# -- Set this to the course category URL you want to scrape
DISCUSSION_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

# -- Cookie data you provided
COOKIES = [
    {"name": "_fbp", "value": "fb.2.1705327698189.1824257798"},
    {"name": "_forum_session", "value": "CI51xGpS0GWMO0I3FSkyiT2tXzgJl9RgGfDnAJIpkNlK6AuU4hyDnw%2B276u0ySccKgTUQXBFLmLT28dTHgiK0tgoRmX2%2BIbSHjtLoISFfO8LJGuDfW0l96X8dI3jQvlTLxsLDN2wefghDN3KJqTnRR1oducqRI1zSbd7Wlb1Wo5Xb%2BjMqdjlCr8D9gY8yOl9WDowiCwOCDj21FjjU7tyZMQsI3yD82rfMgHCnAJk9oV%2FsfMQDj3kuoBkMweE%2FE3RmMQHpl%2FWS5dyg8LSx%2B8JsBaMibesfKTWSbVDnQmQ76awXhEWHeI%2Fw7DzzVvfcOdsB%2B33s6975YZOw8JSZ9tQl3mJRJD3YsZ3hIhul05%2F3nF%2BSIQ0rPGvEnS8z0vuTQ%3D%3D--gGQNP254JoY1Klzy--HO2%2Fv9%2FrOTGNEpOGVNkIkQ%3D%3D"},
    {"name": "_ga", "value": "GA1.1.1752193305.1705327698"},
    {"name": "_ga_08NPRH5L4M", "value": "GS2.1.s1749903893$o412$g1$t1749903911$j42$l0$h0"},
    {"name": "_ga_5HTJMW67XK", "value": "GS2.1.s1749903893$o316$g0$t1749903903$j50$l0$h0"},
    {"name": "_ga_K38CF65X4M", "value": "GS1.1.1719855095.1.0.1719855095.0.0.0"},
    {"name": "_gcl_au", "value": "1.1.2038962148.1745251064"},
    {"name": "_t", "value": "fpMwBxk8smdx8sc40jkz%2BJdMK3WYASDoliJizHvlP7tKc9WCK0gSHPGDDm6WXffFsPMmIELT%2Fdf80Cr7iOZiQSnZvWIvd7%2FNS%2F1INCNhfkCxtKM%2BtdCCE%2Bk8SWrI0KNKngkRuziBE7EQTxBEUsDToiKoRfpZuWboc3x1RneDL3ZIUwYvzEvSWomfWs0JbDYnH0dwB9xQxABSE6Y%2FS9soJsKAaBN4UNcsAqKOnxNWABvveqgbPyb%2FspODpaXSoLrtWLjQgtO9WEFoGVx449NiXqrlRo5xh%2F4uBW0VFPy4aWsiArIqi3LnCRjAkgeBAiJ1--BhQ%2FXS%2BZKFPXp8t9--DDx%2BalRNOD87VSjn%2F5P1CQ%3D%3D"},
]

def scrape_with_cookies():
    print("🚀 Starting browser...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    print("Setting cookies...")
    driver.get("https://discourse.onlinedegree.iitm.ac.in")
    for cookie in COOKIES:
        cookie['domain'] = '.onlinedegree.iitm.ac.in'
        driver.add_cookie(cookie)

    print("🌐 Navigating to TDS KB page...")
    driver.get(DISCUSSION_URL)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.select("a.title.raw-link")

    print(f"Found {len(links)} topic links.")
    with open("tds_discourse_scraped.txt", "w", encoding="utf-8") as f:
        for i, link in enumerate(links[:10], start=1):
            title = link.get_text(strip=True)
            href = link["href"]
            full_url = f"https://discourse.onlinedegree.iitm.ac.in{href}"
            print(f"{i}. Scraping: {title}")

            driver.get(full_url)
            time.sleep(3)

            post_soup = BeautifulSoup(driver.page_source, "html.parser")
            posts = post_soup.select("div.cooked")

            f.write(f"## {title}\n\n")
            for post in posts:
                f.write(post.get_text(strip=True) + "\n\n")

    driver.quit()
    print("Done! Content saved to tds_discourse_scraped.txt")

if __name__ == "__main__":
    scrape_with_cookies()
