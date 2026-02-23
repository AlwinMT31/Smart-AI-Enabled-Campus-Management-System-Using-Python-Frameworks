import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Add spaces around == if missing inside {% if ... %} tags
text = re.sub(r'\{%\s*if\s+([a-zA-Z0-9_\.]+)\s*==\s*([a-zA-Z0-9_\.]+)', r'{% if \1 == \2', text)

# Just to be sure, also replace literal strings
text = text.replace('fac.id==data.allocation.faculty.id', 'fac.id == data.allocation.faculty.id')
text = text.replace('c.id==data.allocation.classroom.id', 'c.id == data.allocation.classroom.id')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Added spaces around ==")
