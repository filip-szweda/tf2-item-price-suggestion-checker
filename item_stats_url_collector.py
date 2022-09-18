from typing import List, NoReturn

from selenium.webdriver import Firefox
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

BP_URL = ""
GECKODRIVER_PATH = ""


def close_cookies(firefox: Firefox) -> NoReturn:
    WebDriverWait(firefox, 60).until(
        expected_conditions.presence_of_element_located((By.XPATH, ".//button[contains(@onclick,'save')]")))
    firefox.find_element(By.XPATH, ".//button[contains(@onclick,'save')]").click()


def scroll_to_element(firefox: Firefox, element: WebElement) -> NoReturn:
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    firefox.execute_script(scroll_by_coord)
    firefox.execute_script(scroll_nav_out_of_way)


def get_urls(firefox: Firefox) -> List[str]:
    urls = []
    navbar_header = firefox.find_element(By.CLASS_NAME, "navbar-header")
    WebDriverWait(firefox, 60).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "backpack-page")))
    backpack = firefox.find_element(By.ID, "backpack")
    backpack_pages = backpack.find_elements(By.CLASS_NAME, "backpack-page")
    actions = ActionChains(firefox)
    for backpack_page in backpack_pages:
        scroll_to_element(firefox, backpack_page)
        item_list = backpack_page.find_element(By.CLASS_NAME, "item-list")
        items = item_list.find_elements(By.TAG_NAME, "li")
        for item in items:
            actions.move_to_element(item).perform()
            WebDriverWait(firefox, 60).until(
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
            if url not in urls and "Tradable" in stats_link.get_attribute("href"):
                urls.append(stats_link.get_attribute("href"))
            actions.move_to_element(navbar_header).perform()
    return urls


def save_urls(urls: List[str], item_urls_path: str) -> NoReturn:
    with open(item_urls_path, "w") as txt:
        for url in urls:
            txt.write(f"{url}\n")


def collect_urls(item_urls_path: str) -> NoReturn:
    firefox = Firefox(executable_path=GECKODRIVER_PATH)
    firefox.get(BP_URL)
    close_cookies(firefox)
    urls = get_urls(firefox)
    save_urls(urls, item_urls_path)
