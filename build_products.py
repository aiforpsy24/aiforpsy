"""Product extension for the existing static AIforPsy site. No payments or client-side entitlements."""
import json,html,re,shutil,argparse
from pathlib import Path
ROOT=Path(__file__).parent
E=html.escape
SLUG='personal-ai-operations-director'

def link(url,label,soft=False): return f'<a class="product-button {"secondary" if soft else ""}" href="{url}">{E(label)} <span aria-hidden="true">↗</span></a>'
def render_card(p,lang):
 c=p['content'][lang]
 return f'<article class="product-card"><div class="product-art" aria-hidden="true"><span>01 / AI</span><div class="art-lines"><i></i><i></i><i></i></div><b>{E(c["art"])}</b></div><div class="product-card-copy"><p class="eyebrow">{E(c["category"])}</p><h2>{E(c["name"])}</h2><p class="product-intro">{E(c["tagline"])}</p><ul class="outcomes">'+''.join(f'<li>{E(x)}</li>' for x in c['results'])+f'</ul>{link(f"/{lang}/products/{p["slug"]}/",c["more"])}</div></article>'

def video(c,url=None):
 if url:
  from urllib.parse import urlparse,parse_qs
  u=urlparse(url); vid=(parse_qs(u.query).get('v') or [''])[0] if u.hostname in ['youtube.com','www.youtube.com'] else u.path.strip('/') if u.hostname=='youtu.be' else ''
  if not re.fullmatch(r'[\w-]{11}',vid): raise ValueError('Use a valid YouTube video URL')
  return f'<div class="video-frame"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(c["watch"])}" allow="fullscreen; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
 return f'<div class="video-frame placeholder" role="img" aria-label="{E(c["soon"])}"><img src="/hero-workspace-v3.png" alt=""><div class="video-shade"></div><div class="video-poster"><span class="eyebrow">AIforPsy / 01</span><h3>{E(c["videoTitle"])}</h3><span class="play-outline" aria-hidden="true">▷</span><p>{E(c["soon"])}</p></div></div>'

def shell(lang,title,body,suffix='',preview=False):
 home=(ROOT/'dist'/lang/'index.html').read_text()
 header=re.search(r'<header.*?</header>',home)[0].replace('href="#about"',f'href="/{lang}/#about"').replace('href="#services"',f'href="/{lang}/#services"')
 other='en' if lang=='ru' else 'ru'
 header=header.replace(f'href="/{other}/"',f'href="/{other}/{suffix}"')
 footer=re.search(r'<footer.*?</footer>',home)[0]
 contact=re.search(r'<template id="contact-content">.*?</template>',home)[0]
 contact=re.sub(r'<button class="copy-selection">.*?</button>','',contact)
 dialog='<dialog><button class="close" aria-label="'+('Закрыть' if lang=='ru' else 'Close')+'">×</button><div id="dialog-content"></div></dialog>'
 banner='<aside class="preview-banner">'+('Локальная проверка · доступ не подтверждает покупку' if lang=='ru' else 'Local preview · this does not confirm a purchase')+'</aside>' if preview else ''
 return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} — AIforPsy</title><meta name="description" content="{E(title)}"><meta name="robots" content="{"noindex,nofollow" if preview else "index,follow"}"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/style.css?v=20261022-1"><link rel="stylesheet" href="/products.css?v=2"><link rel="alternate" hreflang="{other}" href="/{other}/{suffix}"></head><body class="product-page">{header}{banner}<main>{body}</main>{footer}{dialog}{contact}<script src="/products.js?v=2"></script></body></html>'

def write(out,path,content):
 p=out/path/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)

def build(preview=False):
 config=json.loads((ROOT/'products.json').read_text()); products=[p for p in config['products'] if p['status']=='published'];out=ROOT/('preview-dist' if preview else 'dist')
 if preview:
  if out.exists():shutil.rmtree(out)
  shutil.copytree(ROOT/'dist',out)
 for lang in ['ru','en']:
  ru=lang=='ru'; c=config['ui'][lang];p=products[0];d=p['content'][lang];route=f'{lang}/products/{SLUG}';url='/'+route+'/'
  crumbs=f'<div class="product-breadcrumb"><a href="/{lang}/">{c["home"]}</a><span>/</span><a href="/{lang}/save-time/">{c["direction"]}</a></div>'
  body=f'<div class="wrap product-wrap"><div class="catalog-heading"><p class="eyebrow">{c["category"]}</p><h1>{c["catalogTitle"]}</h1><p class="product-intro">{c["catalogIntro"]}</p></div><div class="product-catalog">'+''.join(render_card(p,lang) for p in products)+'</div></div>'
  write(out,f'{lang}/save-time',shell(lang,c['catalogTitle'],body,'save-time/'))
  buy=f'<button class="product-button" data-checkout="{p["id"]}">{d["buy"]} <span aria-hidden="true">→</span></button>'
  body=f'<div class="wrap product-wrap">{crumbs}<section class="product-hero"><div><p class="eyebrow">{d["category"]}</p><h1>{d["hero"]}</h1><p class="product-intro">{d["heroIntro"]}</p><div class="actions">{buy}{link("#how-it-works",c["watch"],True)}</div><p class="quiet">{c["purchaseNote"]}</p></div><aside class="editorial-note"><span class="eyebrow">{c["noteTitle"]}</span><blockquote>{d["quote"]}</blockquote><span>{c["noteEnd"]}</span></aside></section><section class="product-section"><p class="eyebrow">{c["changeEyebrow"]}</p><h2>{c["changes"]}</h2><div class="benefit-grid">'+''.join(f'<article class="benefit benefit-{i%4}"><span class="index">0{i+1}</span><h3>{E(t)}</h3><p>{E(b)}</p></article>' for i,(t,b) in enumerate(d['benefits']))+f'</div></section><section class="product-section" id="how-it-works"><p class="eyebrow">{c["watchEyebrow"]}</p><h2>{c["watch"]}</h2>{video(c,p["explainerYouTubeUrl"])}<p class="video-description">{c["videoDescription"]}</p></section><section class="testimonial-band"><div><p class="eyebrow">{c["voices"]}</p><h2>{c["testimonials"]}</h2><p>{c["reviewsSoon"]}</p></div>'
  if p['testimonialYouTubeUrl']:body+=(video(c,p['testimonialYouTubeUrl']) if p['testimonialMode']=='embed' else link(p['testimonialYouTubeUrl'],c['reviewButton'],True))
  else:body+=f'<button class="product-button secondary" disabled>{c["reviewButton"]}</button>'
  body+=f'</section><section class="product-section"><p class="eyebrow">{c["includedEyebrow"]}</p><h2>{c["included"]}</h2><div class="included-grid">'+''.join(f'<div><span aria-hidden="true">✓</span>{E(x)}</div>' for x in d['includes'])+f'</div></section><section class="final-cta"><h2>{c["finalTitle"]}</h2>{buy}<p class="quiet">{c["purchaseNote"]}</p></section></div><template id="checkout-note"><h2>{c["checkoutTitle"]}</h2><p>{c["checkoutNote"]}</p><p><a href="mailto:support@aiforpsy.net">support@aiforpsy.net</a></p></template>'
  if preview: body+=f'<div class="wrap">{link(url+"hub/", "Проверить доступ к материалам" if ru else "Preview product access",True)}</div>'
  write(out,route,shell(lang,d['hero'],body,f'products/{SLUG}/',preview))
  # These are status pages, never grants of access. There is no browser-stored purchase flag.
  for state in ['success','cancel']:
   text=c['successNote'] if state=='success' else c['cancelNote']
   body=f'<div class="wrap product-wrap status-page"><p class="eyebrow">AIforPsy</p><h1>{c["statusTitle"]}</h1><p>{text}</p>{link(url,c["back"],True)}</div>'
   write(out,route+'/'+state,shell(lang,c['statusTitle'],body,f'products/{SLUG}/{state}/').replace('content="index,follow"','content="noindex,nofollow"'))
  # Public hub routes show no paid content; future server adapter replaces this guard.
  lock=f'<div class="wrap product-wrap status-page"><h1>{c["accessTitle"]}</h1><p>{c["accessNote"]}</p>{link(url,c["back"])}</div>'
  for path in ['hub','hub/quick-start','hub/full-automation']:
   write(out,route+'/'+path,shell(lang,c['accessTitle'],lock,f'products/{SLUG}/{path}/').replace('content="index,follow"','content="noindex,nofollow"'))
  if preview:build_private(out,lang,config,p,crumbs)
 if not preview:
  for lang in ['ru','en']:
   f=out/lang/'index.html';s=f.read_text()
   s=re.sub(r'<button class="read-more" data-service="1" aria-haspopup="dialog">(.*?)</button>',lambda m:f'<a class="read-more" href="/{lang}/save-time/">{m[1]}</a>',s)
   s=re.sub(r'<template id="service-1">.*?</template>','',s)
   s=s.replace('/app.js?v=20261005-8','/app.js?v=20261022-1')
   f.write_text(s)
  (out/'index.html').write_text((out/'ru/index.html').read_text())

def build_private(out,lang,config,p,crumbs):
 private=json.loads((ROOT.parent/'private-content.json').read_text())[lang];c=config['ui'][lang];ru=lang=='ru';base=f'{lang}/products/{SLUG}'
 cards=''
 for path,title,subtitle,body,cta in private['paths']:
  cards+=f'<article class="path-card"><p class="eyebrow">{subtitle}</p><h2>{title}</h2><p>{body}</p>{link("/"+base+"/hub/"+path+"/",cta)}</article>'
 body=f'<div class="wrap product-wrap">{crumbs}<div class="hub-heading"><p class="eyebrow">{private["welcome"]}</p><h1>{private["title"]}</h1><p class="product-intro">{private["intro"]}</p><button class="product-button secondary" data-hub-video>{private["watchMore"]} <span aria-hidden="true">▷</span></button></div><div class="path-grid">{cards}</div><p class="quiet">{private["fallback"]}</p></div>'
 body+=f'<template id="hub-video"><h2>{private["watchMore"]}</h2>{video(c,p.get("hubYouTubeUrl"))}</template>'
 write(out,base+'/hub',shell(lang,private['title'],body,f'products/{SLUG}/hub/',True))
 for path,title,subtitle,desc,cta in private['paths']:
  content=f'<div class="wrap product-wrap tutorial-wrap"><a class="back-link" href="/{base}/hub/">← {private["back"]}</a><p class="eyebrow">{subtitle}</p><h1>{title}</h1>{video(c,p.get("quickStartYouTubeUrl") if path=="quick-start" else p.get("fullAutomationYouTubeUrl"))}<div class="download-panel">{link("/downloads/"+p["downloads"][0]["filename"],private["download"])}<span>{private["zipNote"]}</span></div><p class="product-intro">{private["quickIntro"] if path=="quick-start" else private["fullIntro"]}</p><div class="step-list">'
  for i,step in enumerate(private[path]):
   st,txt,prompt=step
   content+=f'<details class="tutorial-step" {"open" if i==0 else ""}><summary><span class="step-number">{i+1:02}</span><span>{E(st)}</span><span class="step-plus" aria-hidden="true">+</span></summary><div class="step-content"><p>{E(txt)}</p>'
   if prompt is not None:content+=f'<div class="prompt-block"><div><span>{private["promptLabel"]}</span><button class="copy-prompt">{private["copy"]}</button></div><pre>{E(private["prompts"][prompt])}</pre><span class="copy-status" role="status"></span></div>'
   content+='</div></details>'
  content+=f'</div><details class="troubleshooting"><summary>{private["troubleTitle"]} <span>+</span></summary><div>'+''.join(f'<h3>{E(t)}</h3><p>{E(b)}</p>' for t,b in private['trouble'])+f'</div></details><section class="next-step"><h2>{private["nextTitle"]}</h2><p>{private["nextText"]}</p>{link("https://chatgpt.com",private["openChat"])}</section></div>'
  write(out,base+'/hub/'+path,shell(lang,title,content,f'products/{SLUG}/hub/{path}/',True))
 assets=out/'downloads';assets.mkdir(exist_ok=True)
 shutil.copyfile(ROOT.parent/'personal_ai_operations_director_skill_v2.zip',assets/p['downloads'][0]['filename'])

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--preview',action='store_true');build(a.parse_args().preview)
