"""Build the existing privacy policy in every supported storefront language."""
import html
import json
from pathlib import Path
from localization import LANGUAGES, DEFAULT_LANGUAGE, language_switcher, language_metadata, require_locales

ROOT=Path(__file__).parent
STYLE="body{margin:0;background:#f7f6f2;color:#26332d;font:18px/1.65 system-ui,sans-serif}main{max-width:850px;margin:auto;padding:48px 24px 80px}a{color:#236451}h1{font-size:clamp(30px,5vw,44px);line-height:1.2;overflow-wrap:anywhere;hyphens:auto}h2{font-size:24px;line-height:1.3;margin-top:32px}nav{display:flex;justify-content:space-between;gap:20px}footer{margin-top:48px;border-top:1px solid #cdd6cf;padding-top:24px}.language-menu{font-size:15px}"

def build():
    content=json.loads((ROOT/'privacy.json').read_text())
    require_locales(content,'privacy policy')
    for lang in LANGUAGES:
        text=content[lang]
        sections=''.join(f'<section><h2>{html.escape(item["title"])}</h2>{item["body"]}</section>' for item in text['sections'])
        page=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(text["title"])} — Event Marketing Assistant</title><style>{STYLE}</style><link rel="stylesheet" href="/language.css?v=1">{language_metadata(lang,"privacy/")}</head><body><main><nav><a href="/{lang}/">AIforPsy</a>{language_switcher(lang,"privacy/")}</nav><h1>{html.escape(text["title"])}</h1><p>{text["byline"]}</p>{sections}<footer>{text["footer"]}</footer></main><script src="/language.js?v=1"></script></body></html>'
        target=ROOT/'dist'/lang/'privacy/index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page)
    alias=ROOT/'dist/privacy/index.html';alias.parent.mkdir(exist_ok=True);alias.write_text((ROOT/'dist'/DEFAULT_LANGUAGE/'privacy/index.html').read_text())

if __name__=='__main__':build()
