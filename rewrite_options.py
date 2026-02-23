import os
filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# rewrite the inside of the tables from line 237 to 297
new_lines = []
for i, line in enumerate(lines):
    if "fac.id" in line and "selected" in line and "endif" in line:
        new_lines.append('                                        <option value="{{ fac.id }}" {% if fac.id == data.allocation.faculty.id %}selected{% endif %}>\n')
    elif "c.id" in line and "selected" in line and "endif" in line:
        new_lines.append('                                        <option value="{{ c.id }}" {% if c.id == data.allocation.classroom.id %}selected{% endif %}>\n')
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Rewrote the template options.")
