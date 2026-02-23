import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "fac.id" in line and "selected" not in line and "<option" in line:
        new_lines.append('                                        <option value="{{ fac.id }}" {% if True %}selected{% endif %}>\n')
    elif "c.id" in line and "selected" not in line and "<option" in line:
        new_lines.append('                                        <option value="{{ c.id }}" {% if True %}selected{% endif %}>\n')
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
