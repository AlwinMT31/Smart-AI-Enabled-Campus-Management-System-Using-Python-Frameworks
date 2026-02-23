import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace faculty split
content = re.sub(
    r'\{%\s*if\s+fac\.id==data\.allocation\.faculty\.id\s*\n\s*%\}selected\{%\s*endif\s*%\}',
    r'{% if fac.id == data.allocation.faculty.id %}selected{% endif %}',
    content
)

# Replace classroom split
content = re.sub(
    r'\{%\s*if\s+c\.id==data\.allocation\.classroom\.id\s*\n\s*%\}selected\{%\s*endif\s*%\}',
    r'{% if c.id == data.allocation.classroom.id %}selected{% endif %}',
    content
)

# Replace any generic split if tag
content = re.sub(
    r'\{%\s*if\s+([^\n]+)\s*\n\s*%\}selected\{%\s*endif\s*%\}',
    r'{% if \1 %}selected{% endif %}',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated")
