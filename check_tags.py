import re

filepath = r"d:\ALWIN\PROGRAMS\Python\Project 4\core\templates\core\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
stack = []

for i, line in enumerate(lines):
    tags = re.findall(r'{%\s*(if|endif|for|endfor|empty)\b[^%]*%}', line)
    for tag in tags:
        print(f"Line {i+1}: {tag}")
        if tag in ('if', 'for'):
            stack.append((tag, i+1))
        elif tag == 'endif':
            if not stack or stack[-1][0] != 'if':
                print(f"ERROR: Unbalanced endif at line {i+1}! Stack: {stack}")
            else:
                stack.pop()
        elif tag == 'endfor':
            if not stack or stack[-1][0] != 'for':
                print(f"ERROR: Unbalanced endfor at line {i+1}! Stack: {stack}")
            else:
                stack.pop()
        elif tag == 'empty':
            if not stack or stack[-1][0] != 'for':
                print(f"ERROR: Unbalanced empty at line {i+1}! Stack: {stack}")

if stack:
    print(f"ERROR: Unclosed tags remaining: {stack}")
else:
    print("All tags balanced successfully!")
