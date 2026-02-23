import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'rb') as f:
    content = f.read().decode('utf-8')

# Ensure we have pure string without weird inner newlines in tags
content = re.sub(
    r'\{%\s*if\s+fac\.id\s*==\s*data\.allocation\.faculty\.id\s*%\}selected\{%\s*endif\s*%\}',
    '{% if fac.id == data.allocation.faculty.id %}selected{% endif %}',
    content
)

# And similarly for classroom
content = re.sub(
    r'\{%\s*if\s+c\.id\s*==\s*data\.allocation\.classroom\.id\s*%\}selected\{%\s*endif\s*%\}',
    '{% if c.id == data.allocation.classroom.id %}selected{% endif %}',
    content
)

# Let's just aggressively strip newlines from INSIDE any {% %} tag
def clean_tag(match):
    return match.group(0).replace('\n', ' ').replace('\r', '')

content = re.sub(r'\{%(.*?)%\}', clean_tag, content, flags=re.DOTALL)
content = re.sub(r'\{\{(.*?)\}\}', clean_tag, content, flags=re.DOTALL)

with open(filepath, 'wb') as f:
    f.write(content.encode('utf-8'))

print("File normalized")
