import re
import os
import requests
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


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
    "transition-property",
    "text-transform",
    "padding",
    "line-height",
    "scroll-margin-top",
    "fill-origin",
    "margin-block-start",
    "list-style-type",
    "wrap-after",
    "break-before",
    "background-image",
    "font-variant-alternates",
    "vertical-align",
    "text-space-collapse",
    "scroll-padding-inline-end",
    "grid-template-rows",
    "border-bottom-fit-width",
    "border-bottom-left-radius",
    "border-bottom-style",
    "clear",
    "font-synthesis-weight",
    "line-stacking-strategy",
    "background-origin",
    "font-max-size",
    "nav-left",
    "scroll-margin-inline",
    "marker-end",
    "backface-visibility",
    "border-bottom",
    "border-width",
    "bookmark-label",
    "margin-right",
    "font-weight",
    "scroll-snap-align",
    "offset-rotate",
    "cursor",
    "line-clamp",
    "text-emphasis-position",
    "border-image-repeat",
    "border-left-fit-width",
    "border-top-right-fit-length",
    "padding-block",
    "border-block-end",
    "border-spacing",
    "border-left-style",
    "border-bottom-right-fit-width",
    "padding-inline",
    "offset-anchor",
    "marker-knockout-left",
    "text-decoration-skip-ink",
    "border-top-left-fit-width",
    "inset-block-start",
    "mix-blend-mode",
    "line-grid",
    "image-rendering",
    "scroll-padding-inline-end",
    "margin-top",
    "caret",
    "marker-mid",
    "border-bottom-right-radius",
    "marker-start",
    "flex-flow",
    "border-image-width",
    "border-top-style",
    "border-bottom-color",
    "scroll-margin-inline-end",
    "width",
    "fill-size",
    "outline-offset",
    "bookmark-level",
    "text-combine-upright",
    "color",
    "background-repeat",
    "stroke-linejoin",
    "white-space",
    "text-underline-offset",
    "offset-path",
    "mask-origin",
    "block-step-insert",
    "visibility",
    "column-width",
    "marker-pattern",
    "tab-size",
    "align-items",
    "margin-trim",
    "cue-after",
    "list-style-position",
    "resize",
    "stroke-miterlimit",
    "perspective",
    "border-inline",
    "continue",
    "caret-color",
    "font-variation-settings",
    "unicode-bidi",
    "scroll-margin",
    "z-index",
    "border-top-fit-length",
    "grid",
    "scroll-padding-inline",
    "caret-shape",
    "border-style",
    "content",
    "stroke",
    "wrap-through",
    "scroll-margin-block",
    "max-block-size",
    "border-block-color",
    "overflow-inline",
    "shape-outside",
    "mask-position",
    "block-step-align",
    "cue-before",
    "font-synthesis-small-caps",
    "border-collapse",
    "border-top-width",
    "row-gap",
    "counter-reset",
    "scroll-padding-left",
    "perspective-origin",
    "scroll-margin-block-end",
    "marker",
    "column-gap",
    "chains",
    "drop-initial-after-adjust",
    "flex-grow",
    "border-block-start-color",
    "padding-right",
    "scroll-padding-block",
    "background-position",
    "column-rule",
    "dominant-baseline",
    "mask-border-source",
    "border-inline-end-style",
    "transition",
    "text-orientation",
    "isolation",
    "list-style",
    "counter-increment",
    "text-shadow",
    "scroll-margin-right",
    "transform",
    "border-right-color",
    "appearance",
    "stroke-dashcorner",
    "transform-origin",
    "background-color",
    "animation-direction",
    "letter-spacing",
    "fill-break",
    "border-top",
    "border-right-image",
    "marker-knockout-right",
    "margin-block",
    "text-indent",
    "wrap-flow",
    "stroke-alignment",
    "stroke-dashoffset",
    "line-padding",
    "fill",
    "border-right-style",
    "elevation",
    "overflow",
    "min-width",
    "animation-timing-function",
    "border-bottom-right-fit-length",
    "overflow-y",
    "float-reference",
    "grid-auto-flow",
    "font-variant-caps",
    "text-decoration-style",
    "margin-left",
    "display",
    "border-left-width",
    "volume",
    "border-image-outset",
    "filter",
    "outline",
    "image-orientation",
    "table-layout",
    "font-palette",
    "stroke-dasharray",
    "justify-items",
    "nav-down",
    "height",
    "column-rule-style",
    "box-decoration-break",
    "padding-left",
    "stroke-linecap",
    "grid-area",
    "border-top-image",
    "outline-color",
    "mask-mode",
    "hyphens",
    "border-top-color",
    "box-snap",
    "scrollbar-color",
    "line-stacking-ruby",
    "scrollbar-gutter",
    "scroll-padding-top",
    "scroll-behavior",
    "wrap-before",
    "max-inline-size",
    "border-left-color",
    "mask-composite",
    "border-radius",
    "stroke-dashadjust",
    "min-height",
    "right",
    "text-underline-position",
    "offset-before",
    "direction",
    "inset-block",
    "float-defer",
    "nav-right",
    "mask-type",
    "float",
    "mask-border-mode",
    "drop-initial-before-align",
    "stroke-dash-justify",
    "order",
    "stroke-opacity",
    "font-variant-emoji",
    "border",
    "speech-rate",
    "flow",
    "left",
    "fill-image",
    "grid-template-columns",
    "stroke-color",
    "border-inline-color",
    "border-top-right-image",
    "justify-content",
    "mask-repeat",
    "mask-border",
    "string-set",
    "widows",
    "footnote-display",
    "glyph-orientation-vertical",
    "border-image-slice",
    "stroke-origin",
    "text-align",
    "mask-clip",
    "mask-border-width",
    "clip-rule",
    "break-inside",
    "scroll-padding-block-start",
    "text-spacing",
    "contain",
    "border-bottom-image",
    "flood-opacity",
    "inset-block-end",
    "stroke-break",
    "mask-size",
    "grid-row",
    "align-self",
    "mask",
    "border-left",
    "border-image",
    "nav-up",
    "hyphenate-limit-chars",
    "opacity",
    "stroke-dash-corner",
    "border-left-image",
    "text-align-all",
    "grid-template",
    "fill-rule",
    "footnote-policy",
    "margin-inline-start",
    "break-after",
    "word-wrap",
    "border-fit",
    "border-top-right-radius",
    "border-corner-image-transform",
    "ruby-merge",
    "text-overflow",
    "inset",
    "font-stretch",
    "border-inline-start-color",
    "font-size",
    "mask-border-outset",
    "flood-color",
    "empty-cells",
    "text-decoration-line",
    "font-synthesis",
    "animation-iteration-count",
    "border-image-source",
    "padding-top",
    "align-content",
    "text-decoration-color",
    "border-fit-width",
    "border-start-end-radius",
    "fill-repeat",
    "pause-before",
    "border-inline-start-width",
    "marker-side",
    "max-width",
    "transform-style",
    "font-variant-position",
    "border-right-fit-length",
    "scroll-padding-right",
    "animation",
    "list-style-image",
    "border-inline-end-width",
    "border-bottom-width",
    "border-right",
    "flex-direction",
    "text-group-align",
    "page",
    "fill-position",
    "font",
    "shape-image-threshold",
    "max-lines",
    "shape-margin",
    "block-step",
    "outline-style",
    "flow-into",
    "border-image-transform",
    "animation-delay",
    "float-offset",
    "object-position",
    "hyphenate-limit-lines",
    "pause",
    "offset",
    "border-block-end-style",
    "flex",
    "stroke-align",
    "inline-sizing",
    "speak-header",
    "background-clip",
    "region-fragment",
    "stroke-size",
    "initial-letters-align",
    "border-color",
    "border-bottom-right-image",
    "border-top-left-radius",
    "bottom",
    "place-self",
    "text-justify",
    "min-inline-size",
    "grid-template-areas",
    "alignment-adjust",
    "scroll-snap-type",
    "drop-initial-before-adjust",
    "background-size",
    "line-break",
    "shape-inside",
    "border-bottom-left-fit-width",
    "line-stacking",
    "border-top-fit-width",
    "column-rule-width",
    "background-attachment",
    "column-count",
    "border-top-right-fit-width",
    "alignment-baseline",
    "font-variant",
    "richness",
    "writing-mode",
    "font-min-size",
    "block-step-round",
    "text-emphasis",
    "box-sizing",
    "clip",
    "border-top-left-image",
    "bookmark-state",
    "border-block-start-style",
    "pitch",
    "stress",
    "scroll-padding",
    "offset-distance",
    "page-break-inside",
    "font-synthesis-style",
    "clip-path",
    "font-optical-sizing",
    "marker-segment",
    "border-inline-width",
    "stroke-position",
    "animation-fill-mode",
    "border-block-style",
    "position",
    "font-style",
    "text-emphasis-color",
    "caption-side",
    "baseline-shift",
    "mask-image",
    "block-step-size",
    "scroll-padding-bottom",
    "border-right-width",
    "overflow-wrap",
    "scroll-margin-bottom",
    "scroll-snap-stop",
    "orphans",
    "padding-inline-end",
    "border-inline-start-style",
    "mask-border-repeat",
    "block-overflow",
    "azimuth",
    "ruby-align",
    "text-decoration-skip",
    "border-end-end-radius",
    "mask-border-slice",
    "hyphenate-character",
    "lighting-color",
    "box-shadow",
    "offset-end",
    "drop-initial-after-align",
    "page-break-before",
    "text-emphasis-skip",
    "scroll-margin-block-start",
    "overflow-block",
    "place-content",
    "font-kerning",
    "scroll-padding-inline-start",
    "flex-basis",
    "speak-numeral",
    "inline-box-align",
    "word-break",
    "margin-break",
    "text-decoration",
    "offset-position",
    "speak",
    "pitch-range",
    "block-ellipsis",
    "border-block-end-color",
    "drop-initial-size",
    "padding-bottom",
    "stroke-width",
    "font-variant-east-asian",
    "background-blend-mode",
    "hanging-punctuation",
    "user-select",
    "column-span",
    "stroke-repeat",
    "voice-family",
    "border-top-left-fit-length",
    "padding-block-end",
    "border-bottom-fit-length",
    "text-height",
    "page-break-after",
    "fill-opacity",
    "initial-letters-wrap",
    "fill-color",
    "font-family",
    "object-fit",
    "justify-self",
    "font-size-adjust",
    "border-corner-image",
    "pause-after",
    "scroll-margin-inline-start",
    "inset-inline-start",
    "color-adjust",
    "image-resolution",
    "border-inline-end",
    "word-spacing",
    "margin-bottom",
    "speak-punctuation",
    "font-language-override",
    "transform-box",
    "ruby-position",
    "font-feature-settings",
    "border-block-start-width",
    "offset-start",
    "inline-size",
    "stroke-image",
    "margin-block-end",
    "font-variant-ligatures",
    "wrap-inside",
    "border-fit-length",
    "line-stacking-shift",
    "grid-column-end",
    "transition-delay",
    "counter-set",
    "grid-row-end",
    "max-height",
    "quotes",
    "offset-after",
    "columns",
    "grid-auto-columns",
    "padding-block-start",
    "grid-column",
    "background",
    "animation-play-state",
    "scrollbar-width",
    "margin-inline",
    "padding-inline-start",
    "border-break",
    "border-right-fit-width",
    "overflow-x",
    "column-fill",
    "flex-shrink",
    "scroll-margin-left",
    "line-snap",
    "column-rule-color",
    "border-block-start",
    "font-variant-numeric",
    "grid-row-start",
    "margin-inline-end",
    "border-boundary",
    "border-bottom-left-image",
    "border-inline-style",
    "hyphenate-limit-zone",
    "outline-width",
    "text-space-trim",
    "block-size",
    "animation-name",
    "text-decoration-width",
    "grid-column-start",
    "drop-initial-value",
    "transition-duration",
    "text-align-last",
    "grid-auto-rows",
    "text-emphasis-style",
    "border-start-start-radius",
    "border-end-start-radius",
    "running",
    "hyphenate-limit-last",
    "min-block-size",
    "border-block-end-width",
    "animation-duration",
    "play-during",
    "border-inline-end-color",
    "will-change",
    "margin",
    "text-wrap",
    "border-bottoml-eft-fit-length",
    "border-block",
    "place-items",
    "initial-letters",
    "inset-inline-end",
    "transition-timing-function",
    "border-block-width",
    "border-corner-fit",
    "line-height-step",
    "inset-inline",
    "flex-wrap",
    "border-inline-start",
    "color-interpolation-filters",
    "flow-from",
    "border-left-fit-length",
    "weight",
    "align",
    "center",
    "pinterest",
    "twitter",
    "facebook",
    "hover",
    "before",
    "style",
    "italic",
    "nowrap",
    "input",
    "button",
    "loader",
    "sides",
    "0px",
    "break",
    "smoothing",
    "antialiased",
    "beforeSend",
    "function",
    "error",
    "offline",
    "online",
    "XMLHttpRequest",
    "javascript",
    "relative",
    "widget",
    "author",
    "blockquote",
    "Window",
    "block",
    "game",
    "text",
    "object",
    "block",
    "Block",
    "Command",
    "Games",
    "Game",
    "index",
    "image",
    "tool",
    "block",
    "commons",
    "line",
    "GAMES",
    "minecraft",
    "PlayerAdded",
    "NewFarm",
    "Entry",
    "Collect",
    "overflow",
    "block",
    "MainSection",
    "AutoFarm",
    "Section",
    "typesafe",
    "Players",
    "point",
    "color",
    "Play",
    "GAME",
    "display",
    "Text",
    "Client:",
)


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
            email = r"(?:[Uu][Ss][Ee][Rr][Nn][Aa][Mm][Ee]|[Uu][Ss][Ee][Rr]|[Aa][Cc][Cc][Oo][Uu][Nn][Tt]|\b[Aa][Cc][Cc]\b|\b[İiıI][Dd]\b|\b[Nn][Aa][Mm][Ee]|[Ll][Oo][Gg][İiıI][Nn])(?:\s*[:= -]\s*)([+\-\w.’]+)\s"
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


def exiting(output_file, filters):
    unique_texts = set()
    with open(output_file, "r") as file:
        for line in file:
            if not line.strip().startswith(filters):
                unique_texts.add(line.strip())
    unique_text_list = list(unique_texts)

    with open(output_file, "w") as file:
        for text in unique_text_list:
            file.write(text + "\n")


if __name__ == "__main__":
    urls = read_urls_from_file("links.txt")
    email, password, pattern, output_file = choose_option()
    if not os.path.exists(output_file):
        open(output_file, "w").close()
    if choice == "1" or "2":
        with ThreadPoolExecutor(max_workers=3) as executor:
            for url in urls:
                executor.submit(process_url, url, email, password, pattern, output_file)
            exiting(output_file, filters)

    elif choice == "3" or "4" or "5":
        with ThreadPoolExecutor(max_workers=3) as executor:
            for url in urls:
                executor.submit(process_url, url, email, password, pattern, output_file)
