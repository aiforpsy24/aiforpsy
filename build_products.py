"""Product extension for the existing static AIforPsy site. Sales pages only; purchasing and product delivery belong to TA-Next Academy."""
import json,html,re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pathlib import Path
ROOT=Path(__file__).parent
from localization import LANGUAGES, DEFAULT_LANGUAGE, UI, language_switcher, language_metadata, require_locales
E=html.escape
SLUG='personal-ai-operations-director'

def link(url,label,soft=False): return f'<a class="product-button {"secondary" if soft else ""}" href="{url}">{E(label)} <span aria-hidden="true">↗</span></a>'
def purchase_link(product, label, lang):
 """One external destination for both CTAs; never start a local purchase flow."""
 url=product.get('externalPurchaseUrl')
 destination_language=product.get('externalPurchaseLanguages',{}).get(lang,lang)
 if not url or destination_language is None:
  return f'<button class="product-button" disabled>{E(label)} <span aria-hidden="true">→</span></button>'
 parsed=urlparse(url)
 if (parsed.scheme != 'https' or parsed.hostname not in ('ta-next.com','www.ta-next.com')
     or parsed.username or parsed.password or parsed.port not in (None,443)):
  raise ValueError('externalPurchaseUrl must be the verified HTTPS product URL on TA-Next Academy')
 query=dict(parse_qsl(parsed.query,keep_blank_values=True));query["lang"]=destination_language
 url=urlunparse(parsed._replace(query=urlencode(query)))
 return f'<a class="product-button" href="{E(url,quote=True)}">{E(label)} <span aria-hidden="true">→</span></a>'

def render_card(p,lang):
 c=p['content'][lang]
 return f'<article class="product-card"><div class="product-art"><img src="{E(p["productImage"],quote=True)}" alt="{E(c["imageAlt"],quote=True)}" width="480" height="360"></div><div class="product-card-copy"><p class="eyebrow">{E(c["category"])}</p><h2>{E(c["name"])}</h2><p class="product-intro">{E(c["tagline"])}</p><ul class="outcomes">'+''.join(f'<li>{E(x)}</li>' for x in c['results'])+f'</ul>{link(f"/{lang}/products/{p["slug"]}/",c["more"])}</div></article>'

def video(c,url=None):
 if url:
  from urllib.parse import urlparse,parse_qs
  u=urlparse(url); vid=(parse_qs(u.query).get('v') or [''])[0] if u.hostname in ['youtube.com','www.youtube.com'] else u.path.strip('/') if u.hostname=='youtu.be' else ''
  if not re.fullmatch(r'[\w-]{11}',vid): raise ValueError('Use a valid YouTube video URL')
  return f'<div class="video-frame"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(c["watch"])}" allow="fullscreen; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
 return f'<div class="video-frame placeholder" role="img" aria-label="{E(c["soon"])}"><img src="/hero-workspace-v3.png" alt=""><div class="video-shade"></div><div class="video-poster"><span class="eyebrow">AIforPsy / 01</span><h3>{E(c["videoTitle"])}</h3><span class="play-outline" aria-hidden="true">▷</span><p>{E(c["soon"])}</p></div></div>'

def shell(lang,title,body,suffix=''):
 home=(ROOT/'dist'/lang/'index.html').read_text()
 header=re.search(r'<header.*?</header>',home)[0].replace('href="#about"',f'href="/{lang}/#about"').replace('href="#services"',f'href="/{lang}/#services"')
 header=re.sub(r'<details class="language language-menu">.*?</details>',language_switcher(lang,suffix),header)
 footer=re.search(r'<footer.*?</footer>',home)[0]
 contact=re.search(r'<template id="contact-content">.*?</template>',home)[0]
 contact=re.sub(r'<button class="copy-selection"[^>]*>.*?</button>','',contact)
 dialog=f'<dialog><button class="close" aria-label="{UI[lang]["close"]}">×</button><div id="dialog-content"></div></dialog>'
 return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} — AIforPsy</title><meta name="description" content="{E(title)}"><meta name="robots" content="index,follow"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/style.css?v=20261022-1"><link rel="stylesheet" href="/products.css?v=4"><link rel="stylesheet" href="/language.css?v=1">{language_metadata(lang,suffix)}</head><body class="product-page">{header}<main>{body}</main>{footer}{dialog}{contact}<script src="/products.js?v=3"></script><script src="/language.js?v=1"></script></body></html>'

def write(out,path,content):
 p=out/path/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)

def build():
 config=json.loads((ROOT/'products.json').read_text()); products=[p for p in config['products'] if p['status']=='published'];out=ROOT/'dist'
 require_locales(config['ui'],'product interface')
 for item in products:require_locales(item['content'],'published product')
 for lang in LANGUAGES:
  c=config['ui'][lang];p=products[0];d=p['content'][lang];route=f'{lang}/products/{SLUG}'
  crumbs=f'<div class="product-breadcrumb"><a href="/{lang}/">{c["home"]}</a><span>/</span><a href="/{lang}/save-time/">{c["direction"]}</a></div>'
  body=f'<div class="wrap product-wrap"><div class="catalog-heading"><p class="eyebrow">{c["category"]}</p><h1>{c["catalogTitle"]}</h1><p class="product-intro">{c["catalogIntro"]}</p></div><div class="product-catalog">'+''.join(render_card(p,lang) for p in products)+'</div></div>'
  write(out,f'{lang}/save-time',shell(lang,c['catalogTitle'],body,'save-time/'))
  buy=purchase_link(p,d["buy"],lang)
  notice=c["purchaseNote"] if not p.get("externalPurchaseUrl") else p.get("externalPurchaseNotices",{}).get(lang,"")
  purchase_note=f'<p class="quiet">{E(notice)}</p>' if notice else ""
  body=f'<div class="wrap product-wrap">{crumbs}<section class="product-hero"><div><p class="eyebrow">{d["category"]}</p><h1>{d["hero"]}</h1><p class="product-intro">{d["heroIntro"]}</p><div class="actions">{buy}{link("#how-it-works",c["watch"],True)}</div>{purchase_note}</div><aside class="editorial-note"><span class="eyebrow">{c["noteTitle"]}</span><blockquote>{d["quote"]}</blockquote><span>{c["noteEnd"]}</span></aside></section><section class="product-section"><p class="eyebrow">{c["changeEyebrow"]}</p><h2>{c["changes"]}</h2><div class="benefit-grid">'+''.join(f'<article class="benefit benefit-{i%4}"><span class="index">0{i+1}</span><h3>{E(t)}</h3><p>{E(b)}</p></article>' for i,(t,b) in enumerate(d['benefits']))+f'</div></section><section class="product-section" id="how-it-works"><p class="eyebrow">{c["watchEyebrow"]}</p><h2>{c["watch"]}</h2>{video(c,p["explainerYouTubeUrl"])}<p class="video-description">{c["videoDescription"]}</p></section><section class="testimonial-band"><div><p class="eyebrow">{c["voices"]}</p><h2>{c["testimonials"]}</h2><p>{c["reviewsSoon"]}</p></div>'
  if p['testimonialYouTubeUrl']:body+=(video(c,p['testimonialYouTubeUrl']) if p['testimonialMode']=='embed' else link(p['testimonialYouTubeUrl'],c['reviewButton'],True))
  else:body+=f'<button class="product-button secondary" disabled>{c["reviewButton"]}</button>'
  body+=f'</section><section class="final-cta"><h2>{c["finalTitle"]}</h2>{buy}{purchase_note}</section></div>'
  write(out,route,shell(lang,d['hero'],body,f'products/{SLUG}/'))
 for lang in LANGUAGES:
  f=out/lang/'index.html';s=f.read_text()
  s=re.sub(r'<button class="read-more" data-service="1" aria-haspopup="dialog">(.*?)</button>',lambda m:f'<a class="read-more" href="/{lang}/save-time/">{m[1]}</a>',s)
  s=re.sub(r'<template id="service-1">.*?</template>','',s)
  s=s.replace('/app.js?v=20261005-8','/app.js?v=20261022-1')
  f.write_text(s)
 (out/'index.html').write_text((out/DEFAULT_LANGUAGE/'index.html').read_text())

if __name__ == "__main__":
 build()
