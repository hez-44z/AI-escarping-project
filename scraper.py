from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.keys import Keys
import time


def scrape_grailed(search_query):
    """
    Scrapes the first 10 listings from Grailed for a given search query.
    """
    # ChromeDriver setup
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    service = Service("C:/Program Files/ChromeDriver/chromedriver.exe")  # Update your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)


    try:
        # Navigate to Grailed homepage
        url = "https://www.grailed.com/"
        print(f"Navigating to URL: {url}")
        driver.get(url)


        # Allow page to load
        time.sleep(3)


        # Click the search bar to trigger the sign-in pop-up
        search_input = driver.find_element(By.ID, "header_search-input")
        search_input.click()
        print("Clicked on the search bar to trigger the sign-in pop-up.")


        # Dismiss the sign-in pop-up using JavaScript
        try:
            driver.execute_script(
                "document.querySelector('.ReactModal__Overlay').style.display='none';"
            )
            print("Sign-in pop-up removed using JavaScript.")
        except Exception as js_error:
            print(f"JavaScript method failed: {js_error}")


        # Retry clicking the search bar
        search_input.click()
        print("Clicked on the search bar again after dismissing the pop-up.")


        # Enter the search query
        search_input.send_keys(search_query)
        print(f"Entered search query: {search_query}")


        # Submit the search
        search_button = driver.find_element(By.CSS_SELECTOR, "button[title='Submit']")
        search_button.click()
        print("Search button clicked.")


        # Allow results to load
        time.sleep(5)


        # Verify if search results loaded
        results = driver.find_elements(By.CLASS_NAME, "feed-item")
        print(f"Found {len(results)} search results.")


        # Scrape the first 10 listings
        scraped_results = []
        for index, result in enumerate(results[:10]):
            try:
                # Extract Title
                title = result.find_element(By.CSS_SELECTOR, "p.ListingMetadata-module__title___Rsj55").text
            except Exception:
                title = "Not found"


            try:
                # Extract Size
                size = result.find_element(By.CSS_SELECTOR, "p.ListingMetadata-module__size___e9naE").text
            except Exception:
                size = "Not found"


            try:
                # Extract Price
                price = result.find_element(By.CSS_SELECTOR, "span.Price-module__onSale___1pIHp").text
            except Exception:
                price = "Not found"


            try:
                # Extract Image URL
                image_url = result.find_element(By.CSS_SELECTOR, "img.Image-module__crop___nWp1j").get_attribute("src")
            except Exception:
                image_url = "Not found"


            try:
                # Extract Product Link
                product_link = result.find_element(By.CSS_SELECTOR, "a.listing-item-link").get_attribute("href")
            except Exception:
                product_link = "Not found"


            # Append to results
            scraped_results.append({
                "title": title,
                "size": size,
                "price": price,
                "image_url": image_url,
                "product_link": product_link,
            })


        return scraped_results


    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    finally:
        driver.quit()




def scrape_depop(search_query):
    """
    Scrapes the first 10 listings from Depop for a given search query.
    """
    options = Options()
    # options.add_argument("--headless")  # Disable headless mode for visible browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    service = Service("C:/Program Files/ChromeDriver/chromedriver.exe")  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)


    # Build the Depop search URL
    url = f"https://www.depop.com/search/?q={search_query.replace(' ', '+')}"
    print(f"Navigating to URL: {url}")
    driver.get(url)


    # Handle the "Accept" button
    try:
        accept_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='cookieBanner__acceptAllButton']")
        accept_button.click()
        print("Accepted cookies/modal.")
        time.sleep(2)
    except Exception as e:
        print(f"No 'Accept' button found or already handled: {e}")


    # Scroll the page to ensure all elements are visible
    def scroll_page():
        print("Scrolling the page...")
        for _ in range(1):  # Adjust the range if necessary
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)  # Allow time for dynamic loading


    scroll_page()


    # Extract product data
    results = []
    try:
        product_containers = driver.find_elements(By.CSS_SELECTOR, "li.styles__ProductCardContainer-sc-ec533c9e-7")
        print(f"Found {len(product_containers)} product containers.")


        for index, product in enumerate(product_containers[:10]):  # Limit to first 10 results
            print(f"Processing product {index + 1}...")


            # Extract details
            try:
                price = product.find_element(By.CSS_SELECTOR, "p[aria-label='Price'].Price-styles__FullPrice-sc-1c510ed0-0").text
            except Exception:
                price = "Not found"


            try:
                size = product.find_element(By.CSS_SELECTOR, "p[aria-label='Size'].styles__StyledSizeText-sc-ec533c9e-12").text
            except Exception:
                size = "Not found"


            try:
                image_url = product.find_element(By.CSS_SELECTOR, "img.sc-hjbplR").get_attribute("src")
            except Exception:
                image_url = "Not found"


            try:
                brand = product.find_element(By.CSS_SELECTOR, "p.styles__StyledBrandNameText-sc-ec533c9e-21").text
            except Exception:
                brand = "Not found"


            try:
                link = product.find_element(By.CSS_SELECTOR, "a.styles__ProductCard-sc-ec533c9e-4").get_attribute("href")
            except Exception:
                link = "Not found"


            results.append({
                "title": brand,
                "price": price,
                "size": size,
                "image_url": image_url,
                "link": link,
            })
    except Exception as e:
        print(f"Error extracting products: {e}")
    finally:
        driver.quit()


    return results


def scrape_poshmark(search_query):
    """
    Scrapes the first 10 listings from Poshmark for a given search query.
    """
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    service = Service("C:/Program Files/ChromeDriver/chromedriver.exe")  # Update your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)


    # Build the Poshmark search URL
    url = f"https://poshmark.com/search?query={search_query.replace(' ', '%20')}&type=listings&src=dir"
    print(f"Navigating to URL: {url}")
    driver.get(url)


    results = []


    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card"))
        )
        product_containers = driver.find_elements(By.CSS_SELECTOR, "div.card")
        print(f"Found {len(product_containers)} product containers.")


        # Scrape up to the first 10 listings
        for index, container in enumerate(product_containers[:10]):
            print(f"Processing product {index + 1}...")


            try:
                title = container.find_element(By.CSS_SELECTOR, "a.tile__title").text.strip()
            except Exception as e:
                title = "Not found"
                print(f"  Title Error: {e}")


            try:
                price = container.find_element(By.CSS_SELECTOR, "span.p--t--1.fw--bold").text.strip()
            except Exception as e:
                price = "Not found"
                print(f"  Price Error: {e}")


            try:
                size = container.find_element(By.CSS_SELECTOR, "a.tile__details__pipe__size").text.strip().replace("Size: ", "")
            except Exception as e:
                size = "Not found"
                print(f"  Size Error: {e}")


            try:
                raw_link = container.find_element(By.CSS_SELECTOR, "a.tile__title").get_attribute("href")
                link = f"https://poshmark.com{raw_link}" if raw_link.startswith("/") else raw_link
            except Exception as e:
                link = "Not found"
                print(f"  Link Error: {e}")


            try:
                image_url = container.find_element(By.CSS_SELECTOR, "img.ovf--h.d--b").get_attribute("src")
            except Exception as e:
                image_url = "Not found"
                print(f"  Image URL Error: {e}")


            results.append({
                "title": title,
                "price": price,
                "size": size,
                "link": link,
                "image_url": image_url,
            })


    except Exception as e:
        print(f"Error extracting data: {e}")


    finally:
        driver.quit()


    return results




def scrape_ebay(search_query):
    """
    Scrapes the first 10 listings from eBay for a given search query.
    """
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    service = Service("C:/Program Files/ChromeDriver/chromedriver.exe")  # Update your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)


    # Build the eBay search URL
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_sop=12"
    print(f"Navigating to URL: {url}")
    driver.get(url)


    results = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-item__wrapper"))
        )
        product_wrappers = driver.find_elements(By.CSS_SELECTOR, "div.s-item__wrapper")
        print(f"Found {len(product_wrappers)} potential product wrappers.")


        for index, wrapper in enumerate(product_wrappers):
            print(f"Processing wrapper {index + 1}...")
            try:
                title = wrapper.find_element(By.CSS_SELECTOR, ".s-item__title").text.strip()
                if not title or "Shop on eBay" in title:
                    continue


                try:
                    price = wrapper.find_element(By.CSS_SELECTOR, "span.s-item__price").text.strip()
                except Exception:
                    price = "Not found"


                try:
                    image_url = wrapper.find_element(By.CSS_SELECTOR, "div.s-item__image-wrapper img").get_attribute("src")
                except Exception:
                    image_url = "Not found"


                try:
                    item_url = wrapper.find_element(By.CSS_SELECTOR, "a.s-item__link").get_attribute("href")
                except Exception:
                    item_url = "Not found"


                results.append({
                    "title": title,
                    "price": price,
                    "image_url": image_url,
                    "item_url": item_url,
                })


                if len(results) == 10:
                    break


            except Exception as e:
                print(f"Error processing wrapper {index + 1}: {e}")


    except Exception as e:
        print(f"Error locating product wrappers: {e}")
    finally:
        driver.quit()


    return results


def scrape_all_platforms(search_query):
    """
    Unified scraper that runs scrapers for all platforms concurrently.
    """
    platforms = {
        "Grailed": scrape_grailed,
        "Depop": scrape_depop,
        "Poshmark": scrape_poshmark,
        "eBay": scrape_ebay,
    }


    results = []


    def scrape_platform(name, scraper_function):
        try:
            platform_results = scraper_function(search_query)
            print(f"{name}: Retrieved {len(platform_results)} results.")
            for result in platform_results:
                result["platform"] = name  # Add platform identifier
            return platform_results
        except Exception as e:
            print(f"Error scraping {name}: {e}")
            return []


    # Use ThreadPoolExecutor for concurrency
    with ThreadPoolExecutor(max_workers=len(platforms)) as executor:
        futures = {executor.submit(scrape_platform, name, func): name for name, func in platforms.items()}
        for future in futures:
            results.extend(future.result())


    # Shuffle results for a randomized mix
    import random
    random.shuffle(results)
    return results