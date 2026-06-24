import os
import glob
import re

for filepath in glob.glob('templates/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find {{ url_for('static', filename='uploads/' + VAR) }}
    # and replace with:
    # {{ VAR if VAR.startswith('data:image') else url_for('static', filename='uploads/' + VAR) }}

    def repl(m):
        var = m.group(1).strip()
        return f"{{{{ {var} if {var} and {var}.startswith('data:image') else url_for('static', filename='uploads/' + {var}) }}}}"

    # Handle `+` or `~` string concatenation
    new_content = re.sub(
        r'\{\{\s*url_for\s*\(\s*[\'"]static[\'"]\s*,\s*filename\s*=\s*[\'"]uploads/[\'"]\s*(?:\+|~)\s*([^\}]+?)\s*\)\s*\}\}',
        repl,
        content
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Modified {filepath}")
