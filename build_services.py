"""Add localized service pages without changing approved direction cards or globals."""
import json, re, html
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from build_products import shell, write, video
from localization import LANGUAGES, DEFAULT_LANGUAGE, UI, require_locales
ROOT=Path(__file__).parent
E=html.escape

def booking_action(service,lang):
 c=service['content'][lang]
 target=service.get('bookingUrl')
 if not target:
  return '<button class="product-button" disabled>'+E(c['preparing'])+'</button>'
 parsed=urlsplit(target)
 if parsed.scheme!='https' or parsed.hostname!='ta-next.com' or parsed.username or parsed.password or parsed.port not in (None,443):
  raise ValueError('Booking must use an approved TA-Next URL')
 query=dict(parse_qsl(parsed.query));query['lang']=lang
 target=urlunsplit(parsed._replace(query=urlencode(query)))
 return '<a class="product-button" href="'+E(target,quote=True)+'" rel="external">'+E(c['bookingCta'])+' <span aria-hidden="true">→</span></a>'

def card(service,lang):
 c=service['content'][lang]
 if service.get('externalUrl'):
  parsed=urlsplit(service['externalUrl'])
  if parsed.scheme!='https' or parsed.hostname!='ananasik.ai' or parsed.username or parsed.password or parsed.port not in (None,443):
   raise ValueError('External service must use the approved Ananasik URL')
  query=dict(parse_qsl(parsed.query));query['lang']=lang
  target=E(urlunsplit(parsed._replace(query=urlencode(query))),quote=True)
  return f'<a class="product-card external-service" href="{target}" rel="external"><div class="product-art"><img src="{E(service["image"],quote=True)}" alt="{E(c["imageAlt"],quote=True)}" width="480" height="360"></div><div class="product-card-copy"><h2>{E(c["name"])}</h2><p class="product-intro">{E(c["short"])}</p><span class="product-button">{E(c["more"])} <span aria-hidden="true">↗</span></span></div></a>'
 return f'<article class="product-card"><div class="product-art"><img src="/hero-workspace-v3.png" alt="{E(c["room"],quote=True)}" width="480" height="360"></div><div class="product-card-copy"><h2>{E(c["name"])}</h2><p class="product-intro">{E(c["short"])}</p><a class="product-button" href="/{lang}/services/{service["slug"]}/">{E(c["more"])} <span aria-hidden="true">→</span></a></div></article>'

def build():
 config=json.loads((ROOT/'services.json').read_text());out=ROOT/'dist'
 for service in config['services']:
  require_locales(service['content'],'service content')
  if service.get('externalUrl'):continue
  for lang in LANGUAGES:
   c=service['content'][lang];suffix=f'services/{service["slug"]}/'
   def section(title,body,cls=''):
    return f'<section class="photo-section {cls}"><h2>{E(title)}</h2>{body}</section>'
   def paras(text):return f'<p>{E(text)}</p>'
   def bullets(items):return '<ul>'+''.join(f'<li>{E(v)}</li>' for v in items)+'</ul>'
   body=f'<div class="wrap photo-page"><a class="product-breadcrumb" href="/{lang}/services/">← {E(c["backLabel"])}</a><section class="photo-hero"><div><p class="eyebrow">AIforPsy</p><h1>{E(c["name"])}</h1><p class="product-intro">{E(c["hero"])}</p><p>{E(c["physical"])}</p><a class="product-button" href="#ways">{E(c["choose"])} ↓</a></div><img src="/hero-workspace-v3.png" alt="{E(c["room"])}" width="640" height="440"></section>'
   body+=section(c['photos'],paras(c['minimum'])+'<div class="photo-columns"><div>'+bullets(c['good'])+'</div><div><h3>'+E(c['badTitle'])+'</h3>'+bullets(c['bad'])+'</div></div><div class="photo-collage" role="img" aria-label="'+E(c['collage'])+'">'+E(c['collage'])+'</div>')
   body+=section(c['references'],paras(c['referenceText'])+'<h3>'+E(c['trust'])+'</h3>'+paras(c['trustText']))
   body+='<aside class="photo-note"><h2>'+E(c['variation'])+'</h2>'+paras(c['variationText'])+'</aside>'
   body+='<section id="ways" class="photo-section"><h2>'+E(c['choose'])+'</h2><div class="photo-ways">'
   body+='<article class="photo-way"><h3>'+E(c['self'])+'</h3>'+paras(c['selfText'])+'<div class="photo-prices"><p>'+E(c['five'])+' <strong>$5</strong></p><p>'+E(c['ten'])+' <strong>$7</strong></p></div><a class="product-button secondary" href="'+E(service['studioUrl'],quote=True)+'" rel="external">'+E(c['studio'])+' ↗</a><p class="quiet">'+E(c['studioNote'])+'</p></article>'
   body+='<article class="photo-way"><h3>'+E(c['assisted'])+'</h3>'+paras(c['assistedText'])+'<div class="photo-package"><h4>'+E(c['standard'])+'</h4><strong class="photo-price">$49</strong>'+paras(c['standardDetails'])+'</div><div class="photo-package"><h4>'+E(c['object'])+'</h4><strong class="photo-price">$74</strong>'+paras(c['objectDetails'])+paras(c['objectText'])+'<p><strong>'+E(c['objectCount'])+'</strong></p>'+paras(c['objectRange'])+'</div>'+booking_action(service,lang)+'</article></div></section>'
   body+=section(c['booking'],paras(c['bookingText']))
   body+=section(c['video'],'<div class="photo-video" role="img" aria-label="'+E(c['videoSoon'])+'"><span aria-hidden="true">▷</span>'+paras(c['videoSoon'])+'</div>')
   # Empty gallery stays hidden: never invent testimonials or client images.
   if service['gallery']:raise ValueError('Gallery requires reviewed client consent before publication')
   body+='</div>'
   page=shell(lang,c['name'],body,suffix).replace('</head>','<link rel="stylesheet" href="/photoshoot.css?v=1"></head>')
   write(out,f'{lang}/{suffix}',page)
 # The fourth direction is a service catalog, not a contact/support dialog.
 # Keep the homepage's approved text and mobile accordion; only its action changes.
 for lang in LANGUAGES:
  ui=UI[lang];offers=[s for s in config['services'] if s['section']==3]
  if not offers:raise ValueError('Published service catalog cannot be empty')
  title=offers[0]['content'][lang]['backLabel']
  body=f'<div class="wrap product-wrap"><a class="product-breadcrumb" href="/{lang}/">← {E(ui["home"])}</a><div class="catalog-heading"><p class="eyebrow">{E(ui["services"])}</p><h1>{E(title)}</h1><p class="product-intro">{E(ui["doneForYou"])}</p></div><div class="product-catalog service-catalog">'+''.join(card(s,lang) for s in offers)+'</div></div>'
  write(out,f'{lang}/services/',shell(lang,title,body,'services/').replace('/products.css?v=4','/products.css?v=ananasik-1'))
  home=out/lang/'index.html';s=home.read_text()
  s,count=re.subn(r'<button class="read-more" data-service="3" aria-haspopup="dialog">(.*?)</button>',lambda m:f'<a class="read-more" href="/{lang}/services/">{m[1]}</a>',s)
  if count!=1:raise ValueError('Expected exactly one homepage service action')
  s=re.sub(r'<template id="service-3">.*?</template>','',s,flags=re.S)
  home.write_text(s)
 (out/'index.html').write_text((out/DEFAULT_LANGUAGE/'index.html').read_text())
if __name__=='__main__':build()
