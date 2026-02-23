import re
import os

filepath = r"core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix spacing around ==
content = re.sub(r'fac\.id==data\.allocation\.faculty\.id', 'fac.id == data.allocation.faculty.id', content)
content = re.sub(r'c\.id==data\.allocation\.classroom\.id', 'c.id == data.allocation.classroom.id', content)

# Fix multi-line {% if %} issues: bring %}selected{% endif %} up to the same line
content = re.sub(r'\{%\s*if\s+([^%]+?)\n\s*%\}selected\{%\s*endif\s*%\}', r'{% if \1 %}selected{% endif %}', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template fixed.")
