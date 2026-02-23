import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the broken if tag on lines 258-259
broken_if = '{% if fac.id==data.allocation.faculty.id\n                                            %}selected{% endif %}'
fixed_if = '{% if fac.id == data.allocation.faculty.id %}selected{% endif %}'

if broken_if in text:
    text = text.replace(broken_if, fixed_if)

# Fix the same broken if tag for classroom on line 280-281
broken_class_if = '{% if c.id==data.allocation.classroom.id\n                                            %}selected{% endif %}'
fixed_class_if = '{% if c.id == data.allocation.classroom.id %}selected{% endif %}'

if broken_class_if in text:
    text = text.replace(broken_class_if, fixed_class_if)

# Clean up all multi-line {{ variables }}
text = re.sub(r'\{\{([^}]+)\n([^}]+)\}\}', r'{{\1 \2}}', text)
text = re.sub(r'\s+}}', ' }}', text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("courses template fixed.")
