import configparser
import requests
import time
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from startpage import StartPage

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

filter = (
    "https://maps.",
    "https://policies.",
    "https://www.google.",
    "https://translate.",
    "https://www.bing.",
    "https://yabs.",
    "https://passport.",
    "https://yandexwebcache",
    "https://en.wikipedia.org/",
    "https://r.search.yahoo.com/_ylt=",
    "https://help.yahoo.com/",
    "https://search.yahoo.com/search?ei=UTF-8&",
    "https://r.search.yahoo.com/",
    "https://news.",
    "https://video.",
    "https://images.",
    "https://login.",
    "https://mail.",
    "https://support.",
    "https://company.",
    "https://pastebin.com/u/",
    "https://yandex.com",
    "https://go.microsoft.com/",
    "https://cloud.yandex.",
    "https://store.steampowered",
    "https://steamdb.info",
    "https://steamcharts.com",
    "https://plati.market",
    "https://www.nexusmods.com",
    "https://search.aol.com/aol/",
    "https://r.search.aol.com",
    "https://shopping.search.aol.com/search",
)


def search_ddgs(site, keyword):
    with DDGS() as ddgs:
        for duck in ddgs.text(
            f"{site} {keyword}",
            region="wt-wt",
            safesearch="off",
            timelimit="y",
        ):
            yield duck["href"]


def search_google(site, keyword):
    time.sleep(1)
    Google_url = f"https://www.google.com/search?q={site}+{keyword.replace(' ', '+')}"
    response = requests.get(Google_url, timeout=10, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all("a")
        for link in link_elements:
            href = link.get("href")
            if href and href.startswith("https://"):
                yield href


def search_bing(site, keyword):
    time.sleep(1)
    Bing_url = f"https://www.bing.com/search?q={site}+{keyword.replace(' ', '+')}"
    response = requests.get(Bing_url, timeout=10, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all("a")
        for link in link_elements:
            href = link.get("href")
            if href and href.startswith("https://"):
                yield href


def search_yandex(site, keyword):
    time.sleep(1)
    Yandex_url = f"https://yandex.com/search/?text={site}+{keyword.replace(' ', '+')}"
    response = requests.get(Yandex_url, timeout=10, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all("a")
        for link in link_elements:
            href = link.get("href")
            if href and href.startswith("https://"):
                yield href


def search_ecosia(site, keyword):
    time.sleep(1)
    ecosia_url = f"https://www.ecosia.org/search?q={site}+{keyword.replace(' ', '+')}"
    response = requests.get(ecosia_url, timeout=10, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all("a")
        for link in link_elements:
            href = link.get("href")
            if href and href.startswith("https://") and "ecosia" not in href.lower():
                yield href


def search_yahoo(site, keyword):
    time.sleep(1)
    Yahoo_url = f"https://search.yahoo.com/search?p={site}+{keyword.replace(' ', '+')}"
    response = requests.get(Yahoo_url, timeout=10, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all(
            "span", class_="d-ib p-abs t-0 l-0 fz-14 lh-20 fc-obsidian wr-bw ls-n pb-4"
        )
        print(link_elements)
        for link in link_elements:
            href = link.get_text().replace(" › ", "/")
            yield "https://" + href


def search_aol(site, keyword):
    time.sleep(1)
    aol_url = f"https://search.aol.com/aol/search?q={site}+{keyword.replace(' ', '+')}"
    response = requests.get(aol_url, timeout=10, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        link_elements = soup.find_all("span", class_="fz-ms fw-m fc-12th wr-bw lh-17")
        for link in link_elements:
            href = link.get_text()
            yield "https://" + href


def search_startpage(site, keyword):
    task = StartPage()
    task.search(f"{site} {keyword}", page=1)
    for page_num, results in task.results.items():
        for res in results:
            yield res["link"]


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    search_engines = {
        "DuckDuckGo": search_ddgs,
        "Google": search_google,
        "Bing": search_bing,
        "Yandex": search_yandex,
        "StartPage": search_startpage,
        "Yahoo": search_yahoo,
        "Ecosia": search_ecosia,
        "Aol": search_aol,
    }

    selected_search_engines = []
    for engine_name in search_engines:
        if config.getint(engine_name, "enabled"):
            selected_search_engines.append(search_engines[engine_name])

    if not selected_search_engines:
        print("No search engines are enabled in config.")
        return

    while True:
        option = input(
            "Please select the option you want to use:\n"
            "S for search\n"
            "1. Search only on Pastebin\n"
            "2. Search only on Reddit\n"
            "3. Search only on Youtube\n"
            "4. Search on all sites\n"
            "Choice: "
        )
        if option.lower() == "s":
            r = input("site: ")
            site = f"site:{r}"
            break
        elif option == "1":
            site = "site:pastebin.com"
            break
        elif option == "2":
            site = "site:reddit.com"
            break
        elif option == "3":
            site = "site:youtube.com"
            break
        elif option == "4":
            site = ""
            break
        else:
            print("Invalid option.")

    with open("word_list.txt", "r", encoding="utf-8") as keys:
        key = keys.read().split("\n")

    with open("links.txt", "a", encoding="utf-8") as output_file:
        for keyword in key:
            print(keyword)

            for search_engine in selected_search_engines:
                for link in search_engine(site, keyword):
                    output_file.write(link + "\n")

    print("Scraping process completed.")


def exiting():
    unique_texts = set()
    with open("links.txt", "r") as file:
        for line in file:
            unique_texts.add(line.strip())
    unique_text_list = list(unique_texts)

    with open("links.txt", "w") as file:
        for text in unique_text_list:
            if not text.startswith(filter) and not text == "https://pastebin.com/":
                file.write(text + "\n")


if __name__ == "__main__":
    try:
        main()
        exiting()
    except KeyboardInterrupt:
        exiting()
        print("exiting")
