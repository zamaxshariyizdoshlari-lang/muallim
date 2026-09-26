#!/bin/bash
# ishlatish: bash read_pages.sh 11 16
source venv/Scripts/activate
python -X utf8 manage.py shell -c "
from history_ai.models import Page
for n in range($1,$2+1):
    print('=== BET', n, '==='); print(Page.objects.get(book_id=4, page_number=n).text)
" 2>&1 | grep -v "objects imported"
