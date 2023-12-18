from googletrans import Translator

languages = ["es", "fr", "de", "ja", "ru", "ko", "zh-cn", "pt", "it", "nl", "sv", "tr", "pl", "th", "hi", "vi", "fa", "id", "fi", "da", "ar", "he", "el", "hu", "cs", "ro", "sk", "sl", "hr", "bg", "uk", "ms", "tl", "no"]
keys = []

with open("word_list.txt", 'r', encoding='utf-8') as file:
    words = file.read().split("\n")

for word in words:
    if word:
        print(word)
        for language in languages:
            translations = Translator().translate(word, dest=language).text
            keys.append(translations)
            print(translations)



with open("word_list.txt", 'w', encoding='utf-8') as file:
        file.write("\n".join(keys))
