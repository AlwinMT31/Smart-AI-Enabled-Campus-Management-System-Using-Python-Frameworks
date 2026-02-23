import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lpu_smart_campus.settings')
django.setup()

import traceback
from django.test import Client

c = Client(SERVER_NAME='127.0.0.1')
try:
    c.get('/courses/')
    print("Success 200 OK")
except Exception as e:
    with open('error_trace.txt', 'w') as f:
        traceback.print_exc(file=f)
    print("Error saved to error_trace.txt")
