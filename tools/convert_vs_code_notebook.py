import re
import json
import sys
from pathlib import Path

inp = Path(r"e:\Null class internship\NullClassInternship.ipynb")
if not inp.exists():
    print("Input file not found:", inp)
    sys.exit(1)
text = inp.read_text(encoding='utf-8')

# Regex to capture VSCode.Cell blocks
pattern = re.compile(r"<VSCode.Cell\s+id=\"(?P<id>[^\"]+)\"\s+language=\"(?P<lang>[^\"]+)\">\n(?P<body>.*?)</VSCode.Cell>", re.S)

cells = []
for m in pattern.finditer(text):
    cell_id = m.group('id')
    lang = m.group('lang')
    body = m.group('body')
    # normalize line endings
    body = body.replace('\r\n', '\n').rstrip('\n')
    lines = body.split('\n')
    # Trim a single leading blank line if present (common in the export)
    if len(lines) and lines[0].strip()=='' and len(lines)>1:
        lines = lines[1:]
    # Jupyter cells expect lists of strings with trailing newlines
    source = [ln + '\n' for ln in lines]
    if lang.lower() == 'markdown':
        cell = {
            "cell_type": "markdown",
            "metadata": {"id": cell_id, "language": "markdown"},
            "source": source
        }
    else:
        cell = {
            "cell_type": "code",
            "metadata": {"id": cell_id, "language": lang},
            "execution_count": None,
            "outputs": [],
            "source": source
        }
    cells.append(cell)

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python", "version": "3.x"}
    },
    "cells": cells
}

out = inp.with_suffix('.ipynb')
backup = inp.with_suffix('.ipynb.bak')
# backup original (rename)
try:
    inp.rename(backup)
    print('Backed up original to', backup)
except Exception as e:
    print('Could not backup original:', e)

out.write_text(json.dumps(nb, indent=2), encoding='utf-8')
print('Wrote converted notebook to', out)
