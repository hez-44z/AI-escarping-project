import json
import time
from playwright.sync_api import sync_playwright

def scroll_down(page, scroll_step=1000, max_scrolls=5, pause=2):
    """
    Scrolls down the page to load more items in case of infinite scroll.
    - scroll_step: how many pixels to scroll each time.
    - max_scrolls: how many times we scroll down.
    - pause: how many seconds to wait after each scroll.
    """
    for i in range(max_scrolls):
        page.mouse.wheel(0, scroll_step * (i + 1))
        time.sleep(pause)
    # Final wait to ensure dynamic content is fully loaded
    time.sleep(3)

def scrape_depop(search_query="vintage t-shirt"):
    """
    Searches Depop for the given query using the selectors verified in DevTools.
    Returns a list of items (price, image, link, etc.) as dictionaries.
    """
    url = f"https://www.depop.com/search/?q={search_query}"

    with sync_playwright() as p:
        # 1) Launch browser (non-headless to debug visually)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 2) Go to Depop search page
        page.goto(url, timeout=15000)

        # 3) Attempt to handle cookie/consent overlays
        accept_selectors = [
            "button:has-text('Accept')",
            "#onetrust-accept-btn-handler",
            "button:has-text('Agree')",
        ]
        for sel in accept_selectors:
            try:
                page.wait_for_selector(sel, timeout=3000)
                page.click(sel)
                time.sleep(2)
                print(f"Clicked accept button -> {sel}")
                break
            except:
                pass

        # 4) Scroll down to load more results
        scroll_down(page, scroll_step=1000, max_scrolls=5, pause=2)

        # 5) Additional wait to ensure products are rendered
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # 6) Each product is in a div with this class
        product_selector = "div.styles_productCardRoot__DaYPT"

        try:
            # Wait for at least one product card
            page.wait_for_selector(product_selector, timeout=5000)
        except:
            print("No product cards found. Possibly site changed or blocked.")
            browser.close()
            return []

        product_cards = page.query_selector_all(product_selector)
        print(f"Found {len(product_cards)} product cards.")

        results = []
        for product in product_cards:
            try:
                # ---- Link ----
                link_el = product.query_selector("a.styles_unstyledLink__DsttP")
                if link_el:
                    href = link_el.get_attribute("href")
                    link = "https://www.depop.com" + href if href else "No link"
                else:
                    link = "No link"

                # ---- Price ----
                price_el = product.query_selector("p.styles_price__H8qdh")
                price = price_el.inner_text() if price_el else "No price"

                # ---- Image ----
                img_el = product.query_selector("img._mainImage_e5j9l_11")
                image = img_el.get_attribute("src") if img_el else "No image"

                # ---- (Optional) More Info ----
                # For example, the next <p> elements might be size or brand.
                # We'll collect them all:
                p_tags = product.query_selector_all("p._text_bevez_41")
                # The first p might be the price already, but if you want the next lines:
                # e.g. second p is the size, third p might be brand/category
                size = brand = None
                if len(p_tags) >= 2:
                    # p_tags[1] could be size
                    size = p_tags[1].inner_text()
                if len(p_tags) >= 3:
                    # p_tags[2] could be brand / other info
                    brand = p_tags[2].inner_text()

                results.append({
                    "price": price,
                    "image": image,
                    "link": link,
                    "size": size or "Unknown",
                    "brand_or_category": brand or "Unknown"
                })
            except Exception as e:
                print(f"Error scraping a product: {e}")

        browser.close()
        return results

if __name__ == "__main__":
    data = scrape_depop("vintage t-shirt")
    print(json.dumps(data[:10], indent=4))
