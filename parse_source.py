#!/usr/bin/env python

import json

import bleach
from bs4 import BeautifulSoup
import requests

HUNGARIAN_PROVERBS_SOURCE_URL = 'http://mek.oszk.hu/00200/00242/00242.htm'


raw_content = requests.get(HUNGARIAN_PROVERBS_SOURCE_URL).content
soup = BeautifulSoup(raw_content, 'html5lib')

proverbs = []
for proverb in soup.find_all('li'):
    # Get rid of all HTML but the line breaks...
    cleaned = bleach.clean(proverb.decode(), tags=['br'], strip=True)
    # ...that we can use to split up the proverb lines
    parts = cleaned.strip().split('<br>')
    # Throw away all the parts that don't have any meaning (e.g. extra lines, or the main letters)
    cleaned_parts = [part for part in parts if len(part) > 3 and not part.startswith('\n')]

    # print cleaned_parts
    if len(cleaned_parts) == 2:
        proverbs.append({
            'hun_orig': cleaned_parts[0],
            'eng': cleaned_parts[1],
        })
    elif len(cleaned_parts) == 3:
        proverb_dict = {
            u'hun_orig': cleaned_parts[0],
        }
        # If the second line starts with a parenthesis, it's an explanation in
        # Hungarian, otherwise the English translation
        if cleaned_parts[1].startswith('('):
            proverb_dict.update({
                u'hun_explain': cleaned_parts[1],
                u'eng': cleaned_parts[2],
            })
        else:
            proverb_dict.update({
                u'eng': cleaned_parts[1],
                u'eng_explain': cleaned_parts[2],
            })

        proverbs.append(proverb_dict)
    elif len(cleaned_parts) == 4:
        proverb_dict = {
            u'hun_orig': cleaned_parts[0],
        }
        # If the second line starts with a parenthesis, a dash, or a quote,
        # (or it's a single special case) it's an explanation in Hungarian,
        # otherwise the English translation
        if cleaned_parts[1][0] in ('(', '-', '"') or cleaned_parts[1].startswith('Bors'):
            proverb_dict.update({
                u'hun_explain': cleaned_parts[1],
                u'eng': cleaned_parts[2],
                u'eng_explain': cleaned_parts[3],
            })
        else:
            proverb_dict.update({
                u'eng': cleaned_parts[1],
                u'eng_explain': cleaned_parts[2],
                u'eng_explain2': cleaned_parts[3],
            })
        proverbs.append(proverb_dict)

print json.dumps(proverbs, indent=4, sort_keys=True, ensure_ascii=False).encode('utf-8')
