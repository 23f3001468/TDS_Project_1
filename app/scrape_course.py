from playwright.sync_api import sync_playwright
import time

def scrape_with_playwright():
    print("Launching Playwright browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("Navigating to page...")
            page.goto("https://tds.s-anand.net/#/2025-01/", timeout=60000)

            print("Waiting for sidebar to load...")
            page.wait_for_selector("aside a", timeout=15000)
            time.sleep(1)

            sidebar_links = page.query_selector_all("aside a")
            print(f"Found {len(sidebar_links)} sidebar items.")

            all_contents = []
            visited_titles = set()

            for i in range(len(sidebar_links)):
                sidebar_links = page.query_selector_all("aside a")
                link = sidebar_links[i]

                try:
                    title = link.inner_text().strip()

                    if not title or title in visited_titles:
                        continue
                    visited_titles.add(title)

                    print(f"Clicking: {title}")

                    link.scroll_into_view_if_needed()
                    box = link.bounding_box()
                    if not box or box['height'] == 0:
                        print(f"Skipping non-visible: {title}")
                        continue

                    link.click(timeout=5000)
                    page.wait_for_selector("main", timeout=10000)
                    time.sleep(1)

                    main_content = page.inner_text("main").strip()
                    all_contents.append(f"\n\n--- {title} ---\n\n{main_content}")

                except Exception as e:
                    print(f"Error processing '{title}': {e}")
                    continue

        except Exception as e:
            print(f"Top-level error: {e}")

        finally:
            print("Saving scraped content (even if partial)...")
            try:
                with open("all_course_sections.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(all_contents))
                print("Saved to all_course_sections.txt")
            except Exception as file_err:
                print(f"Failed to write file: {file_err}")

            browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    scrape_with_playwright()
