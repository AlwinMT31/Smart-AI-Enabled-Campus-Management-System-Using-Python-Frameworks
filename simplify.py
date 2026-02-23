import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'{%\s*if\s+fac\.id\s*==\s*data\.allocation\.faculty\.id\s*%}selected{%\s*endif\s*%}', '', text)
text = re.sub(r'{%\s*if\s+c\.id\s*==\s*data\.allocation\.classroom\.id\s*%}selected{%\s*endif\s*%}', '', text)

# Just to be extremely sure, let's also remove any lingering malformed ones if they exist
text = text.replace('{% if fac.id==data.allocation.faculty.id %}selected{% endif %}', '')
text = text.replace('{% if c.id==data.allocation.classroom.id %}selected{% endif %}', '')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Simplified courses.html")
