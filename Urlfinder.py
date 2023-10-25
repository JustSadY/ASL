import configparser
import requests
import time
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from startpage import StartPage
from concurrent.futures import ThreadPoolExecutor


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}


filter = set()
try:
    with open("filter.txt", "r") as filtering:
        for filters in filtering:
            filter.add(filters.strip())
except FileNotFoundError:
    filter = set()


def search_ddgs(site, keyword):
    with DDGS() as ddgs:
        try:
            print(f"Duckduckgo: {keyword}")
            time.sleep(1)
            for duck in ddgs.text(
                f"{site} {keyword}",
                region="wt-wt",
                safesearch="off",
                timelimit="y",
            ):
                output_file.write(duck["href"] + "\n")
        except Exception as e:
            print(f"Error occurred during Duckduckgo search: {e}")


def search_google(site, keyword):
    print(f"Google: {keyword}")
    time.sleep(1)
    response = requests.get(
        f"https://www.google.com/search?q={site}+{keyword.replace(' ', '+')}",
        timeout=5,
        headers=headers,
    )
    if response.status_code == 200:
        link_elements = BeautifulSoup(response.text, "html.parser").find_all(
            "a", jscontroller="M9mgyc", jsname="qOiK6e", jsaction="rcuQ6b:npT2md"
        )
        for link in link_elements:
            href = link.get("href")
            if href and href.startswith("https://"):
                output_file.write(href + "\n")
    else:
        print("Not searching: Google")


def search_bing(site, keyword):
    print(f"Bing: {keyword}")
    time.sleep(1)
    response = requests.get(
        f"https://www.bing.com/search?q={site}+{keyword.replace(' ', '+')}",
        timeout=5,
        headers=headers,
    )
    if response.status_code == 200:
        link_elements = BeautifulSoup(response.text, "html.parser").find_all("cite")
        for link in link_elements:
            output_file.write(link.get_text() + "\n")
    else:
        print("Not searching: Bing")


def search_yandex(site, keyword):
    print(f"Yandex: {keyword}")
    try:
        for page in range(0, pages + 1):
            time.sleep(1)
            response = requests.get(
                f"https://yandex.com/search/?text={site}+{keyword.replace(' ', '+')}&amp;p={page}",
                timeout=5,
                headers=headers,
            )
            if response.status_code == 200:
                link_elements = BeautifulSoup(response.text, "html.parser").find_all(
                    "a", tabindex="0"
                )
                for link in link_elements:
                    href = link.get("href")
                    if href and href.startswith("https://"):
                        output_file.write(href + "\n")
            else:
                break
    except Exception as e:
        print(f"Error occurred during Yandex search: {e}")


def search_ecosia(site, keyword):
    try:
        print(f"Ecosia: {keyword}")
        for page in range(0, pages + 1):
            time.sleep(1)
            response = requests.get(
                f"https://www.ecosia.org/search?q={site}+{keyword.replace(' ', '+')}&p={page}",
                timeout=5,
                headers=headers,
            )
            if response.status_code == 200:
                link_elements = BeautifulSoup(response.text, "html.parser").find_all(
                    "a", class_="result__link link link--as-a link--color-result"
                )
                for link in link_elements:
                    href = link.get("href")
                    output_file.write(href + "\n")
            else:
                break
    except Exception as e:
        print(f"Error occurred during Ecosia search: {e}")


def search_yahoo(site, keyword):
    try:
        print(f"Yahoo: {keyword}")
        for page in range(0, pages + 1):
            time.sleep(1)
            response = requests.get(
                f"https://search.yahoo.com/search?p={site}+{keyword.replace(' ', '+')}&b={((page) * 10)}",
                timeout=5,
                headers=headers,
            )
            if response.status_code == 200:
                link_elements = BeautifulSoup(response.text, "html.parser").find_all(
                    "span",
                    class_="d-ib p-abs t-0 l-0 fz-14 lh-20 fc-obsidian wr-bw ls-n pb-4",
                )
                for link in link_elements:
                    href = link.get_text().replace(" › ", "/")
                    output_file.write("https://" + href + "\n")
            else:
                break
    except Exception as e:
        print(f"Error occurred during Yahoo search: {e}")


def search_aol(site, keyword):
    try:
        print(f"Aol: {keyword}")
        time.sleep(1)
        response = requests.get(
            f"https://search.aol.com/aol/search?q={site}+{keyword.replace(' ', '+')}",
            timeout=5,
            headers=headers,
        )
        if response.status_code == 200:
            link_elements = BeautifulSoup(response.text, "html.parser").find_all(
                "span", class_="fz-ms fw-m fc-12th wr-bw lh-17"
            )
            for link in link_elements:
                href = link.get_text()
                output_file.write("https://" + href + "\n")
    except Exception as e:
        print(f"Error occurred during AOL search: {e}")


def search_startpage(site, keyword):
    try:
        print(f"Startpage: {keyword}")
        time.sleep(1)
        task = StartPage()
        task.search(f"{site} {keyword}", page=pages)
        for page_num, results in task.results.items():
            for res in results:
                output_file.write(res["link"] + "\n")
    except Exception as e:
        print(f"Error occurred during StartPage search: {e}")


def Search_Ramber(site, keyword):
    try:
        print(f"Ramber: {keyword}")
        time.sleep(1)
        response = requests.get(
            f"https://nova.rambler.ru/search?query={site}+{keyword.replace(' ', '+')}",
            timeout=5,
            headers=headers,
        )
        if response.status_code == 200:
            link_elements = BeautifulSoup(response.text, "html.parser").find_all(
                class_="Serp__url--3NdzA components__colored_link--9ft9T"
            )
            for link in link_elements:
                href = link.get("href")
                if href and href.startswith("https://"):
                    output_file.write(href + "\n")
    except Exception as e:
        print(f"Error occurred during Ramber search: {e}")


def Search_Ask(site, keyword):
    try:
        print(f"Ask: {keyword}")
        for page in range(0, pages + 1):
            time.sleep(1)
            response = requests.get(
                f"https://www.ask.com/web?q={site}+{keyword.replace(' ', '+')}&page={page}",
                timeout=5,
                headers=headers,
            )
            if response.status_code == 200:
                link_elements = BeautifulSoup(response.text, "html.parser").find_all(
                    "a", class_="PartialSearchResults-item-title-link result-link"
                )
                for link in link_elements:
                    href = link.get("href")
                    if href and href.startswith("https://"):
                        output_file.write(href + "\n")
            else:
                break
    except Exception as e:
        print(f"Error occurred during Ask.com search: {e}")


def main():
    global output_file
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
        "Ramber": Search_Ramber,
        "Ask": Search_Ask,
    }

    selected_search_engines = []
    for engine_name in search_engines:
        if config.getint(engine_name, "enabled"):
            selected_search_engines.append(search_engines[engine_name])

    if not selected_search_engines:
        print("No search engines are enabled in config.")
        return

    while True:
        global option
        try:
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
        except:
            print("Invalid input. Please enter a valid number.")

    while True:
        global pages
        try:
            pages = int(input("Pages: "))
            if -1 < pages < 5:
                break
        except:
            print("Invalid input. Please enter a valid number.")

    with open("word_list.txt", "r", encoding="utf-8") as keys:
        key = keys.read().split("\n")

    with open("links.txt", "a", encoding="utf-8") as output_file:
        for keyword in key:
            with ThreadPoolExecutor(
                max_workers=len(selected_search_engines)
            ) as executor:
                futures = []
                for search_engine in selected_search_engines:
                    future = executor.submit(search_engine, site, keyword)
                    futures.append(future)

                for future in futures:
                    future.result()

    print("Scraping process completed.")


def exiting():
    unique_texts = set()
    with open("links.txt", "r", encoding="utf-8") as file:
        for line in file:
            if option == "1":
                if line.startswith("https://pastebin.com") or line.startswith(
                    "https://www.pastebin.com"
                ):
                    unique_texts.add(line.strip())
            elif option == "2":
                if line.startswith("https://reddit.com") or line.startswith(
                    "https://www.reddit.com"
                ):
                    unique_texts.add(line.strip())
            elif option == "3":
                if line.startswith("https://youtube.com") or line.startswith(
                    "https://www.youtube.com"
                ):
                    unique_texts.add(line.strip())
            else:
                if not any(
                    line.startswith(prefix) for prefix in filter
                ) and not line == (
                    "https://pastebin.com/" and "https://pastebin.com/faq"
                ):
                    unique_texts.add(line.strip())
    unique_text_list = list(unique_texts)
    unique_text_list.sort()

    with open("links.txt", "w", encoding="utf-8") as file:
        for text in unique_text_list:
            file.write(text + "\n")


if __name__ == "__main__":
    try:
        main()
        exiting()
    except KeyboardInterrupt:
        print("Just Wait")
        exiting()
        print("exiting")
