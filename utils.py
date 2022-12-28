from typing import List, NoReturn

from undetected_chromedriver import Chrome
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

BP_URL = "https://backpack.tf/profiles/76561198263024930"


def close_cookies(browser: Chrome) -> NoReturn:
    WebDriverWait(browser, 60).until(
        expected_conditions.presence_of_element_located((By.XPATH, ".//button[contains(@onclick,'save')]")))
    browser.find_element(By.XPATH, ".//button[contains(@onclick,'save')]").click()


def scroll_to_element(browser: Chrome, element: WebElement) -> NoReturn:
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    browser.execute_script(scroll_by_coord)
    browser.execute_script(scroll_nav_out_of_way)


def get_urls(browser: Chrome) -> List[str]:
    urls = []
    navbar_header = browser.find_element(By.CLASS_NAME, "navbar-header")
    WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "backpack-page")))
    backpack = browser.find_element(By.ID, "backpack")
    backpack_pages = backpack.find_elements(By.CLASS_NAME, "backpack-page")
    actions = ActionChains(browser)
    for backpack_page in backpack_pages:
        scroll_to_element(browser, backpack_page)
        item_list = backpack_page.find_element(By.CLASS_NAME, "item-list")
        items = item_list.find_elements(By.TAG_NAME, "li")
        for item in items:
            if item.get_attribute("class") != "item spacer":
                actions.move_to_element(item).perform()
                WebDriverWait(browser, 60).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, "popover-content")))
                try:
                    links = item_list.find_element(By.CLASS_NAME, "popover.right.in").find_element(By.CLASS_NAME,
                                                                                                   "popover-content").find_element(
                        By.ID, "popover-additional-links").find_elements(By.XPATH, ".//a[contains(@href,'stats')]")
                except NoSuchElementException:
                    links = item_list.find_element(By.CLASS_NAME, "popover.left.in").find_element(By.CLASS_NAME,
                                                                                                  "popover-content").find_element(
                        By.ID, "popover-additional-links").find_elements(By.XPATH, ".//a[contains(@href,'stats')]")
                stats_link = links[0]
                url = stats_link.get_attribute("href")
                if url not in urls and "Tradable" in url and "Non-Tradable" not in url:
                    urls.append(stats_link.get_attribute("href"))
                actions.move_to_element(navbar_header).perform()
    return urls


def save_urls(urls: List[str], item_urls_path: str) -> NoReturn:
    with open(item_urls_path, "w") as txt:
        for url in urls:
            txt.write(f"{url}\n")


def collect_urls(item_urls_path: str) -> NoReturn:
    browser = Chrome()
    browser.get(BP_URL)
    close_cookies(browser)
    urls = get_urls(browser)
    save_urls(urls, item_urls_path)
