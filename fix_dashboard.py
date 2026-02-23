import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\dashboard.html"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix f.max
text = re.sub(r'\{\{\s*f\.max\s*\}\}', '{{ f.max }}', text)

# Just to be absolutely certain we catch the multi-line ones:
text = text.replace('{{ f.max\n                                }}', '{{ f.max }}')
text = text.replace('{{ f.hours }}/{{ f.max\n                                }} hrs', '{{ f.hours }}/{{ f.max }} hrs')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("dashboard template fixed.")
