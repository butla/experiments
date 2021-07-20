FILE_TO_SORT = 'addresses.txt'

# ==========================

import sys
from pathlib import Path

file_to_sort = Path(__file__) / '..' / FILE_TO_SORT
file_to_sort = file_to_sort.resolve()

print('Gonna be sorting file', file_to_sort)

if not file_to_sort.exists():
    sys.exit(f"ERROR! Can't find the file for sorting: {file_to_sort}")

contents = file_to_sort.read_text()

fragments = [fragment.strip() for fragment in contents.split('\n\n')]
cleaned_fragments = (fragment for fragment in fragments if fragment)
sorted_fragments = sorted(cleaned_fragments)

sorted_text = '\n\n'.join(sorted_fragments)

file_to_sort.write_text(sorted_text)
print('Sorting done')
