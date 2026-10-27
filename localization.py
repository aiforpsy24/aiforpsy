"""Shared locale registry, route links and strict translation validation."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / 'locales.json').read_text())
LANGUAGES = tuple(item['code'] for item in CONFIG['languages'])
DEFAULT_LANGUAGE = CONFIG['default']
UI = CONFIG['ui']
assert DEFAULT_LANGUAGE in LANGUAGES
assert set(UI) == set(LANGUAGES)
assert all(set(UI[lang]) == set(UI[DEFAULT_LANGUAGE]) for lang in LANGUAGES)


def language_switcher(lang, suffix=''):
    items = []
    for item in CONFIG['languages']:
        code = item['code']
        current = ' aria-current="page"' if code == lang else ''
        items.append(f'<a href="/{code}/{suffix}" lang="{code}" hreflang="{code}" aria-label="{html.escape(item["label"],quote=True)}"{current}>{html.escape(item["label"])}</a>')
    selected = next(item for item in CONFIG['languages'] if item['code'] == lang)
    return (f'<details class="language language-menu"><summary aria-label="{UI[lang]["languageMenu"]}">'
            f'{selected["short"]} <span aria-hidden="true">⌄</span></summary>'
            f'<div class="language-options">{"".join(items)}</div></details>')


def language_metadata(lang, suffix=''):
    return (f'<link rel="canonical" href="https://aiforpsy.net/{lang}/{suffix}">'
            + ''.join(f'<link rel="alternate" hreflang="{code}" href="/{code}/{suffix}">' for code in LANGUAGES)
            + f'<link rel="alternate" hreflang="x-default" href="/{DEFAULT_LANGUAGE}/{suffix}">')


def require_locales(values, name):
    if set(values) != set(LANGUAGES):
        raise ValueError(f'{name}: translations must cover exactly {LANGUAGES}')
    reference = values[DEFAULT_LANGUAGE]
    for lang in LANGUAGES:
        if isinstance(reference, dict) and set(values[lang]) != set(reference):
            raise ValueError(f'{name}/{lang}: missing or extra translation keys')
