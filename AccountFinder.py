import re
import requests
import time
from bs4 import BeautifulSoup

filters = (
    "xanim:viewmodel",
    "weapon:",
    "game:",
    "Backpack:",
    "Player",
    "Window:",
    "Main:",
    "Aimlocks:",
    "Camera:",
    "KeyDown:",
    "SelectedKey:",
    "SelectedDisableKey:",
)


def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [url.strip() for url in file.readlines()]


def choose_option():
    while True:
        choice = input(
            "1. Email:Password\n2. Username:Password\n3. Email - Password\n4. Username - Password\n5. Steam keys\n(Enter 'exit' to quit): "
        ).lower()

        if choice == "1":
            return (
                r"[A-Za-z0-9._%+-]+\@[A-Za-z]+\.[A-Za-z]+\:[A-Za-z0-9._%+-]{5,18}\w+",
                "emails_passwords.txt",
                "1",
            )
        elif choice == "2":
            return (
                r"[A-Za-z0-9]{4,}\:[A-Za-z0-9]{5,18}\w+",
                "usernames_passwords.txt",
                "2",
            )
        elif choice == "3":
            email = r"(?:[Ee][Mm][Aa][Iıİi][Ll]|[Ee][Pp][Oo][Ss][Tt][Aa]|[Ee]-[Pp][Oo][Ss][Tt][Aa]|[Ee]-[Ee][Mm][Aa][Iıİi][Ll])(?:[ ]|)(?:[:]|[=]|[-])(?:[ ]|)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+\b"
            password = r"(?:[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]|[Pp][Aa][Ss][Ss])(?:[ ]|)(?:[:]|[=]|[-])(?:[ ]|)[A-Za-z0-9._%+-]{5,18}\b"
            return f"{email}|{password}", "custom_data.txt", "3"
        elif choice == "4":
            username = r"(?:[Uu][Ss][Ee][Rr][Nn][Aa][Mm][Ee]|[Uu][Ss][Ee][Rr])(?:[ ]|)(?:[:]|[=]|[-])(?:[ ]|)[A-Za-z0-9._%+-]+\b"
            password = r"(?:[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]|[Pp][Aa][Ss][Ss])(?:[ ]|)(?:[:]|[=]|[-])(?:[ ]|)[A-Za-z0-9._%+-]{5,18}\b"
            return f"{username}|{password}", "custom_data.txt", "4"
        elif choice == "5":
            return (
                r"[A-Za-z0-9]{3,}\-[A-Za-z0-9]{3,}\-[A-Za-z0-9-]{3,18}\w+",
                "Steam_keys.txt",
                "5",
            )
        elif choice in ("exit", "quit", "q"):
            print("Exiting the program.")
            exit()
        else:
            print("Invalid input. Please choose 1, 2, 3, 4, or 5.")


def process_data_and_save(urls, pattern, output_file, choice):
    unique_lines = set()
    with open(output_file, "a") as file:
        for url in urls:
            print("Connecting to:", url)
            time.sleep(1)
            try:
                response = requests.get(url)
                response.raise_for_status()
                content = response.text
                soup = BeautifulSoup(content, "html.parser")
                plain_text = soup.get_text()

                if choice in ("3", "4"):
                    custom_found_items = re.findall(pattern, plain_text)
                    for item in custom_found_items:
                        unique_lines.add(url + "\n")
                elif choice in ("5"):
                    custom_found_items = re.findall(pattern, plain_text)
                    for item in custom_found_items:
                        unique_lines.add(url + " " + item + "\n")
                else:
                    found_items = re.findall(pattern, plain_text)
                    for item in found_items:
                        unique_lines.add(item + "\n")

                with open(output_file, "a") as file:
                    file.writelines(unique_lines)
            except requests.exceptions.RequestException:
                print("Couldn't connect to", url)
    print(f"Found items saved to {output_file}.")


def exiting():
    unique_texts = set()
    with open(output_file, "r") as file:
        for line in file:
            unique_texts.add(line.strip())
    unique_text_list = list(unique_texts)
    with open(output_file, "w") as file:
        for text in unique_text_list:
            if not text.startswith(filters):
                file.write(text + "\n")


if __name__ == "__main__":
    urls = read_urls_from_file("links.txt")
    pattern, output_file, choice = choose_option()
    try:
        process_data_and_save(urls, pattern, output_file, choice)
        exiting()
    except KeyboardInterrupt:
        exiting()
        print("Exiting")
