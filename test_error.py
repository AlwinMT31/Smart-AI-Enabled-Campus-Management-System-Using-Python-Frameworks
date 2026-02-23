from django.test import Client
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lpu_smart_campus.settings")
django.setup()

c = Client()
response = c.get('/courses/', {'dept': 'BTECH CSE'})
if response.status_code == 500:
    text = response.content.decode()
    idx = text.find("Exception Value:")
    if idx != -1:
        print("EXCEPTION:", text[idx:idx+200])
    else:
        print("Couldn't find exception string, printing some text:", text[:500])
elif response.status_code == 200:
    print("SUCCESS, no error.")
else:
    print("Other status code:", response.status_code)
