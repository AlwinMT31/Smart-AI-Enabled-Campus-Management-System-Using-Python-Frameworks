import re

with open("temp.html", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("Exception Value:")
if idx != -1:
    print("EXCEPTION:", text[idx:idx+200])
else:
    print("No Exception String found in HTML.")
    print("Does it have a title?", re.search(r'<title>(.*?)</title>', text))
