import re
import os
import requests
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor





def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [url.strip() for url in file.readlines()]


def choose_option():
    global choice
    while True:
        choice = input(
            "1. Email:Password\n2. Username:Password\n3. Email - Password\n4. Username - Password\n5. Steam keys\n(Enter 'exit' to quit): "
        ).lower()

        if choice == "1":
            return (
                "none",
                "none",
                r"\w+[A-Za-z0-9._%+-]+\@[A-Za-z]+\.[A-Za-z]+\:[A-Za-z0-9^_.!+-:%$]{4,18}\b",
                "emails_passwords.txt",
            )
        elif choice == "2":
            return (
                "none",
                "none",
                r"\w+[A-Za-z0-9^_.!+-:%$]{4,}:[A-Za-z0-9^_.!+-:%$]{4,18}\b",
                "usernames_passwords.txt",
            )
        elif choice == "3":
            email = r"(?:[Ee][Mm][Aa][Iıİi][Ll]|[Ee][Pp][Oo][Ss][Tt][Aa]|[Ee]-[Pp][Oo][Ss][Tt][Aa]|[Ee]-[Ee][Mm][Aa][Iıİi][Ll]|[Aa][Cc][Cc][Oo][Uu][Nn][Tt]|[Aa][Cc][Cc]|[Ll][Oo][Gg][İiıI][Nn]|\b[İiıI][Dd]\b)(?:\s*[:= -]\s*)+(\w+[A-Za-z0-9._%+-]+\@[A-Za-z0-9]+\.[A-Za-z]+)"
            password = r"(?:[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]|[Pp][Aa][Ss][Ss]\b)\s*[:= -]+\s*(\w[A-Za-z0-9^_.!+-:%$]+)"
            return email, password, f"{email}|{password}", "custom_data.txt"
        elif choice == "4":
            email = r"(?:[Uu][Ss][Ee][Rr][Nn][Aa][Mm][Ee]|[Uu][Ss][Ee][Rr]|[Aa][Cc][Cc][Oo][Uu][Nn][Tt]|\b[Aa][Cc][Cc]\b|\b[İiıI][Dd]\b|\b[Nn][Aa][Mm][Ee]|[Ll][Oo][Gg][İiıI][Nn])(?:\s*[:= -]\s*)([+\-\w.’]+)"
            password = r"(?:[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]|[Pp][Aa][Ss][Ss]\b)\s*[:= -]+\s*(\w[A-Za-z0-9^_.!+-:%$]+)"
            return email, password, f"{email}|{password}", "custom_data.txt"
        elif choice == "5":
            return (
                "none",
                "none",
                r"\w+[A-Za-z0-9]{3,}\-[A-Za-z0-9]{3,6}\-[A-Za-z0-9-]{3,7}\b",
                "Steam_keys.txt",
            )
        elif choice in ("exit", "quit", "q"):
            print("Exiting the program.")
            exit()
        else:
            print("Invalid input. Please choose 1, 2, 3, 4, or 5.")


def process_url(url, email, password, pattern, output_file):
    try:
        print("Connecting to:", url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            plain_text = soup.get_text()
            time.sleep(1)

            with open(output_file, "a") as file:
                if choice in ("3", "4"):
                    if url.startswith("https://pastebin.com/"):
                        if re.findall(pattern, plain_text):
                            file.writelines(url + "\n")
                            acc = []
                            for element in soup.find_all(class_="de1"):
                                acc.append(element.get_text())
                            custom_found_users = re.findall(email, " ".join(acc))
                            custom_found_passwords = re.findall(password, " ".join(acc))
                            if len(custom_found_users) == len(custom_found_passwords):
                                for user_item, pass_item in zip(
                                    custom_found_users, custom_found_passwords
                                ):
                                    file.writelines(f"{user_item}:{pass_item}\n")
                            elif (
                                len(custom_found_users)
                                == len(custom_found_passwords) * 2
                            ):
                                for user_item, pass_item in zip(
                                    custom_found_users[1 : len(custom_found_users) : 2],
                                    custom_found_passwords,
                                ):
                                    file.writelines(f"{user_item}:{pass_item}\n")
                            else:
                                for user_item, pass_item in zip(
                                    custom_found_users, custom_found_passwords
                                ):
                                    file.writelines(f"{user_item}:{pass_item}\n")

                    else:
                        if re.findall(pattern, plain_text):
                            file.writelines(url + "\n")
                            custom_found_users = re.findall(email, plain_text)
                            custom_found_passwords = re.findall(password, plain_text)
                            for user_item, pass_item in zip(
                                custom_found_users, custom_found_passwords
                            ):
                                file.writelines(
                                    f'{user_item.replace("Password" or "password" or "pass" or "Pass", "")}:{pass_item}\n'
                                )
                elif choice == "5":
                    if url.startswith("https://www.realsteamkeys.com/"):
                        custom_found_items = soup.find_all("td", class_="column-3")
                        if custom_found_items:
                            file.writelines(url + "\n")
                            for item in [
                                item.text.strip() for item in custom_found_items
                            ]:
                                file.writelines(item + "\n")
                    elif url.startswith("https://www.validsteamkeys.com/"):
                        custom_found_items = soup.find_all("td", class_="column-2")
                        if custom_found_items:
                            file.writelines(url + "\n")
                            for item in [
                                item.text.strip() for item in custom_found_items
                            ]:
                                file.writelines(item.replace("DX:", "") + "\n")
                    elif url.startswith("https://niftbyte.com/"):
                        custom_found_items = soup.find_all("td", class_="column-3")
                        if custom_found_items:
                            file.writelines(url + "\n")
                            for item in [
                                item.text.strip() for item in custom_found_items
                            ]:
                                file.writelines(item.replace("DX:", "") + "\n")
                    else:
                        custom_found_items = re.findall(pattern, plain_text)
                        if custom_found_items:
                            file.writelines(url + "\n")
                            for item in custom_found_items:
                                file.writelines(item.replace("Steam", "") + "\n")
                else:
                    found_items = re.findall(pattern, plain_text)
                    for item in found_items:
                        file.writelines(item + "\n")

    except requests.exceptions.RequestException:
        print("Couldn't connect to", url)


# def exiting(output_file, filters):
#     unique_texts = set()
#     with open(output_file, "r") as file:
#         for line in file:
#             if not line.strip().startswith(filters):
#                 unique_texts.add(line.strip())
#     unique_text_list = list(unique_texts)

#     with open(output_file, "w") as file:
#         for text in unique_text_list:
#             file.write(text + "\n")


if __name__ == "__main__":
    urls = read_urls_from_file("links.txt")
    email, password, pattern, output_file = choose_option()
    if not os.path.exists(output_file):
        open(output_file, "w").close()
    if choice == "1" or "2":
        with ThreadPoolExecutor(max_workers=3) as executor:
            for url in urls:
                executor.submit(process_url, url, email, password, pattern, output_file)
            # exiting(output_file, filters)

    elif choice == "3" or "4" or "5":
        with ThreadPoolExecutor(max_workers=3) as executor:
            for url in urls:
                executor.submit(process_url, url, email, password, pattern, output_file)
