# -*- coding: utf-8 -*-
"""Build all storefront locales from the shared registry and approved copy."""
import html
import json
import re
from pathlib import Path
from localization import LANGUAGES, DEFAULT_LANGUAGE, UI, language_switcher, language_metadata, require_locales

root = Path(__file__).parent
copy = json.loads((root/'copy-approved.json').read_text())
introductions = json.loads((root/'card-introductions.json').read_text())
require_locales(copy, 'homepage copy')
require_locales(introductions, 'card introductions')
paths = ['<path d="M16 28V10M16 23C5 23 4 13 6 9c8 1 10 7 10 14ZM17 27c11-2 13-10 12-15-8 0-12 7-12 15Z"/>','<circle cx="17" cy="17" r="13"/><path d="M17 8v10l7 4"/>','<path d="m17 5 13 7-13 7L4 12l13-7Zm-13 14 13 7 13-7M4 26l13 7 13-7"/>','<circle cx="17" cy="10" r="4"/><circle cx="6" cy="15" r="3"/><circle cx="28" cy="15" r="3"/><path d="M10 30v-5a7 7 0 0 1 14 0v5ZM2 28v-5a4 4 0 0 1 6-4M32 28v-5a4 4 0 0 0-6-4"/>']
for lang in LANGUAGES:
    text = copy[lang]; ui = UI[lang]
    sections = text.split('\n---\n'); pre = sections[0].split('### 1.')[0]
    intro = next(line for line in pre.splitlines() if line.startswith(ui['introPrefix']))
    cards = []; templates = []
    for i, section in enumerate(sections):
        title = re.search(r'^### \d\. (.+)$', section, re.M)[1].capitalize()
        body = section.split(re.search(r'^### \d\. (.+)$', section, re.M)[1], 1)[1].strip()
        paragraphs = body.split('\n\n'); lead = paragraphs[0].strip('*'); cta = paragraphs[-1].strip('*')
        paras = paragraphs[1:-1]
        lead = introductions[lang].get(str(i), lead)
        if i == 3: paras = [ui['doneForYou']]
        icon = f'<svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[i]}</svg>'
        cards.append(f'<details class="card card-{i}"><summary><span class="icon">{icon}</span><span class="card-title">{html.escape(title)}</span><span class="plus" aria-hidden="true">+</span></summary><div class="card-body"><p class="lead">{html.escape(lead)}</p><p class="preview">{html.escape(paras[0])}</p><button class="read-more" data-service="{i}" aria-haspopup="dialog">{ui["readMore"]} <span aria-hidden="true">→</span></button></div></details>')
        templates.append(f'<template id="service-{i}"><h2>{html.escape(title)}</h2><p class="lead">{html.escape(lead)}</p>'+''.join(f'<p>{html.escape(p)}</p>' for p in paras)+f'<button class="contact-button">{html.escape(cta)}</button></template>')
    navigation = f'<a href="/{lang}/">{ui["home"]}</a><a href="#about">{ui["about"]}</a><a href="#services">{ui["services"]}</a><button class="nav-contact">{ui["contact"]}</button>'
    page = f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AIforPsy</title><meta name="description" content="{html.escape(intro,quote=True)}"><link rel="stylesheet" href="/style.css?v=20261022-1"><link rel="stylesheet" href="/language.css?v=1"><link rel="icon" type="image/svg+xml" href="/favicon.svg">{language_metadata(lang)}</head><body><header class="header wrap"><a class="brand" href="/{lang}/">AIforPsy</a><nav aria-label="{ui["navigation"]}">{navigation}</nav><details class="mobile-menu"><summary aria-label="{ui["menuOpen"]}"><span class="menu-bars" aria-hidden="true"></span><span aria-hidden="true">⌄</span></summary><div class="mobile-menu-links">{navigation}</div></details>{language_switcher(lang)}</header><main><section class="hero" id="about"><img class="hero-photo" src="/hero-workspace-v3.png" alt="{ui["heroAlt"]}"><p class="mobile-wall-caption">{ui["strap"]}</p><div class="hero-inner wrap"><div class="hero-copy"><p class="eyebrow">{ui["experience"]}</p><h1>{ui["headline"]}<span>{ui["accent"]}</span></h1><p class="intro">{html.escape(intro)}</p><a class="hero-link" href="#services">{ui["find"]} <span aria-hidden="true">→</span></a></div></div></section><section class="services wrap" id="services"><div class="section-heading"><p class="eyebrow">{ui["strap"]}</p><h2><span class="desktop-question">{html.escape(ui["question"])}</span><span class="mobile-question">{html.escape(ui["mobileQuestion"])}</span></h2></div><div class="cards">{''.join(cards)}</div></section></main><footer class="wrap"><span>AIforPsy</span><a class="footer-email" href="mailto:support@aiforpsy.net">support@aiforpsy.net</a><a href="/{lang}/privacy/">{ui["privacy"]}</a><span>© 2026</span></footer><dialog aria-label="{ui["details"]}"><button class="close" aria-label="{ui["close"]}">×</button><div id="dialog-content"></div></dialog>{''.join(templates)}<template id="contact-content"><h2>{ui["contactTitle"]}</h2><p>{ui["contactText"]}</p><p><a href="mailto:support@aiforpsy.net">support@aiforpsy.net</a></p><button class="copy-selection" data-copied="{ui["copied"]}">{ui["copySelection"]}</button></template><script src="/app.js?v=20261026-1"></script><script src="/language.js?v=1"></script></body></html>'''
    target = root/'dist'/lang/'index.html'; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(page)
(root/'dist/index.html').write_text((root/'dist'/DEFAULT_LANGUAGE/'index.html').read_text())

from build_products import build as build_products
from build_privacy import build as build_privacy
build_products()
build_privacy()
