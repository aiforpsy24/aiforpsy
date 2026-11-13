"""A permanent EN/RU course-creation card with one replaceable TA-Next event URL."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from build_products import shell, write

ROOT = Path(__file__).parent
E = html.escape
SUFFIX = 'create-your-product/'


def build():
    config = json.loads((ROOT / 'course-event.json').read_text())
    target = urlsplit(config['eventUrl'])
    if (target.scheme != 'https' or target.hostname != 'ta-next.com'
            or not target.path.startswith('/event/') or target.username or target.password
            or target.port not in (None, 443)):
        raise ValueError('Course events must link to an approved TA-Next HTTPS event page')
    # No expiry filter: past events remain visible until the owner replaces eventUrl.
    for lang in config['publishedLanguages']:
        if lang not in ('en', 'ru'):
            raise ValueError('This event is currently published only in English and Russian')
        c = config['content'][lang]
        query = dict(parse_qsl(target.query)); query['lang'] = lang
        url = E(urlunsplit(target._replace(query=urlencode(query))), quote=True)
        body = (f'<div class="wrap product-wrap"><a class="product-breadcrumb" href="/{lang}/">← {E(c["home"])}</a>'
                f'<div class="catalog-heading"><p class="eyebrow">TA-Next Academy</p><h1>{E(c["direction"])}</h1></div>'
                f'<article class="product-card course-event-card"><div class="course-event-art">'
                f'<img src="{E(config["image"],quote=True)}" alt="{E(c["imageAlt"],quote=True)}" width="1600" height="900"></div>'
                f'<div class="product-card-copy"><h2>{E(c["title"])}</h2><p class="product-intro">{E(c["intro"])}</p>'
                f'<a class="product-button" href="{url}" rel="external">{E(c["more"])} <span aria-hidden="true">↗</span></a>'
                '</div></article></div>')
        page = shell(lang, c['direction'], body, SUFFIX)
        # UK has no event/catalog page: its language option returns to the UK homepage.
        page = page.replace(f'href="/uk/{SUFFIX}"', 'href="/uk/"')
        page = re.sub(r'<link rel="alternate" hreflang="(?:uk|x-default)"[^>]*>', '', page)
        page = page.replace('</head>', '<link rel="stylesheet" href="/course-event.css?v=1"></head>')
        write(ROOT / 'dist', f'{lang}/{SUFFIX}', page)
        home = ROOT / 'dist' / lang / 'index.html'
        source = home.read_text()
        source, count = re.subn(r'<button class="read-more" data-service="2" aria-haspopup="dialog">(.*?)</button>',
                                lambda m: f'<a class="read-more" href="/{lang}/{SUFFIX}">{m[1]}</a>', source)
        if count != 1:
            raise ValueError('Expected one course-creation direction action')
        source = re.sub(r'<template id="service-2">.*?</template>', '', source, flags=re.S)
        home.write_text(source)
