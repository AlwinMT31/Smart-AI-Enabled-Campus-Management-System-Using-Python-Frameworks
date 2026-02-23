import urllib.request
import traceback

try:
    html = urllib.request.urlopen('http://127.0.0.1:8000/courses/?dept=BTECH%20CSE').read().decode('utf-8')
    with open('temp.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fetched successfully")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    html = e.read().decode('utf-8')
    with open('temp.html', 'w', encoding='utf-8') as f:
        f.write(html)
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

import re

try:
    with open("temp.html", "r", encoding="utf-8") as f:
        text = f.read()

    idx = text.find("Exception Value:")
    if idx != -1:
        print("EXCEPTION:", text[idx:idx+200])
    else:
        print("No Exception String found in HTML.")
        m = re.search(r'<title>(.*?)</title>', text)
        if m:
            print("Title:", m.group(1))
        
        # Check for other common Django error markers
        if "TemplateSyntaxError" in text:
            print("TemplateSyntaxError found in text")
            idx2 = text.find("TemplateSyntaxError")
            print(text[max(0, idx2-50):idx2+200])
except Exception as e:
    print(f"Parse error: {e}")
