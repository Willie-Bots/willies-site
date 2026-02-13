#!/usr/bin/env python3
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests

RSS_URL = 'https://www.paymentsdive.com/feeds/news/'
OUT = Path(__file__).resolve().parents[1] / 'data' / 'paymentsdive-newsletter.json'


def clean(s: str) -> str:
    s = re.sub(r'<[^>]+>', '', s or '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def make_summary(articles):
    if not articles:
        return 'No new articles found today.'
    themes = []
    joined = ' '.join((a['title'] + ' ' + a.get('description', '')) for a in articles).lower()
    if any(k in joined for k in ['fraud', 'scam', 'security', 'breach']):
        themes.append('fraud/security')
    if any(k in joined for k in ['regulation', 'cfpb', 'fed', 'law', 'compliance']):
        themes.append('regulation')
    if any(k in joined for k in ['ai', 'fintech', 'wallet', 'real-time', 'instant']):
        themes.append('product + fintech innovation')
    if not themes:
        themes.append('payments industry updates')
    return f"Today’s PaymentsDive recap: {len(articles)} new stories, with focus on {', '.join(themes[:2])}."


def main():
    resp = requests.get(RSS_URL, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    items = root.findall('./channel/item')[:8]

    articles = []
    for item in items:
        title = clean(item.findtext('title'))
        link = clean(item.findtext('link'))
        desc = clean(item.findtext('description'))
        pub = clean(item.findtext('pubDate'))
        if title and link:
            articles.append({
                'title': title,
                'link': link,
                'description': desc,
                'published': pub,
            })

    now = datetime.now(timezone.utc)
    payload = {
        'source': RSS_URL,
        'generated_at': now.isoformat().replace('+00:00', 'Z'),
        'generated_date': now.strftime('%Y-%m-%d'),
        'summary': make_summary(articles),
        'articles': articles,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    print(f'Wrote {OUT} with {len(articles)} articles')


if __name__ == '__main__':
    main()
