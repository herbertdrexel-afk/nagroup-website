#!/usr/bin/env python3
"""Erzeugt alle HTML-Seiten in public/ aus src/content.py.

Aufruf:  python3 build.py
Danach Änderungen auf GitHub hochladen und im cPanel deployen (siehe README).
"""
import hashlib
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from content import (LANGS, LANG_LABEL, UI, DESCRIPTION, CEOS, HQ, HOME, COMPANY, ADVANTAGES,  # noqa: E402
                     CATALOG_INTRO, CATEGORIES, PRODUCTS, ROLES, MEMBERS, CONTACT, TITLE_SUFFIX)

BASE = "https://nagroup.biz"
OUT = os.path.join(os.path.dirname(__file__), "public")
IMG = "/assets/img/"
LEGAL = {"de": ("impressum.html", "datenschutz.html"), "en": ("legal-notice.html", "privacy.html")}
CAT = {c["id"]: c for c in CATEGORIES}


def ver(rel):
    with open(os.path.join(OUT, rel.lstrip("/")), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def legal_lang(lang):
    return "de" if lang == "de" else "en"


def legal_link(lang, kind):
    l2 = legal_lang(lang)
    return f"/{l2}/{LEGAL[l2][kind]}"


def u(lang, page):
    """URL einer Seite in einer Sprache. page '' = Startseite."""
    return f"/{lang}/{page}"


def stripe():
    return '<div class="stripe" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'


# ------------------------------------------------------------------ Rahmen
def head(lang, title, page):
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{u(l, page)}">' for l in LANGS)
    full = f"{title} – {TITLE_SUFFIX}" if title else f"{TITLE_SUFFIX} – Natural Advantage"
    return f"""<!doctype html>
<html lang="{'zh-Hans' if lang == 'zh' else lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{DESCRIPTION[lang]}">
<link rel="canonical" href="{BASE}{u(lang, page)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{BASE}{u('en', page)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css?v={ver('/assets/css/style.css')}">
</head>
<body>"""


NAV = [("", "home"), ("company.html", "company"), ("products.html", "products"),
       ("sourcing.html", "sourcing"), ("advantages.html", "advantages"), ("contact.html", "contact")]


def header(lang, page, section):
    nav = "".join(
        f'<a href="{u(lang, p)}"' + (' aria-current="page"' if key == section else "") + f">{UI[key][lang]}</a>"
        for p, key in NAV)
    langs = "".join(
        f'<a href="{u(l, page)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == lang else "") + f">{LANG_LABEL[l]}</a>"
        for l in LANGS)
    return f"""<a class="skip" href="#main">{UI['skip'][lang]}</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="logo" href="{u(lang, '')}"><img src="{IMG}na-logo.webp" width="74" height="64" alt="NA Group – Natural Advantage"></a>
    <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Menü">
    <label for="navtoggle" class="burger" aria-hidden="true"><span></span></label>
    <div class="navwrap">
      <div class="lang">{langs}</div>
      <nav class="nav" aria-label="{UI['home'][lang]}">{nav}</nav>
    </div>
  </div>
  {stripe()}
</header>"""


def footer(lang):
    links = "".join(f'<a href="{u(lang, p)}">{UI[k][lang]}</a>' for p, k in NAV[1:])
    return f"""<footer class="site-footer">
  {stripe()}
  <div class="wrap foot">
    <div class="foot-brand"><img src="{IMG}na-logo.webp" width="74" height="64" alt="NA Group" loading="lazy"><address>{'<br>'.join(HQ)}</address></div>
    <nav class="foot-nav" aria-label="Footer">{links}</nav>
    <div class="foot-legal"><a href="{legal_link(lang, 0)}">{UI['imprint'][lang]}</a><a href="{legal_link(lang, 1)}">{UI['privacy'][lang]}</a><span>© NA Group</span></div>
  </div>
</footer>
<script src="/assets/js/main.js?v={ver('/assets/js/main.js')}" defer></script>
</body>
</html>
"""


def page_header(lang, title, crumbs, img="hero-3.webp"):
    trail = " › ".join([f'<a href="{u(lang, "")}">NA Group</a>'] + [f'<a href="{h}">{t}</a>' for t, h in crumbs[:-1]] + [crumbs[-1][0]])
    return f"""<section class="page-head" style="background-image:url('{IMG}{img}')">
  <div class="wrap"><div class="page-title"><h1>{title}</h1><p class="crumbs">{trail}</p></div></div>
</section>"""


def page(lang, page_path, section, title, body):
    return head(lang, title, page_path) + header(lang, page_path, section) + f'\n<main id="main">\n{body}\n</main>\n' + footer(lang)


def write(rel, html):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)


# ------------------------------------------------------------------ Bausteine
def member_cards(lang):
    return "".join(f"""<a class="mcard" href="{u(lang, 'sourcing/' + m['id'] + '.html')}">
  <span class="mcard-logo"><img src="{IMG}{m['logo']}" alt="{m['name']}" loading="lazy"></span>
  <strong>{m['name']}</strong><span class="mcard-loc">{m['loc'][lang]}</span>
  <span class="mcard-text">{m['short'][lang]}</span><span class="more">{UI['details'][lang]} ›</span>
</a>""" for m in MEMBERS)


def cat_cards(lang):
    return "".join(f"""<a class="ccard" href="{u(lang, 'products.html')}#{c['id']}">
  <img src="{IMG}{c['img']}" alt="" loading="lazy"><span class="ccard-label"><strong>{c['name'][lang]}</strong><em>{UI['see_products'][lang]} ›</em></span>
</a>""" for c in CATEGORIES)


def product_cards(lang, items, prefix=""):
    return "".join(f"""<a class="pcard" href="{prefix}{p['id']}.html">
  <img src="{IMG}p-{p['img']}-1.webp" alt="" loading="lazy"><span>{p['name'][lang]}</span>
</a>""" for p in items)


def request_box(lang):
    return f"""<div class="request"><p>{UI['request_text'][lang]}</p><a class="btn" href="{u(lang, 'contact.html')}#formular">{UI['request'][lang]} ›</a></div>"""


# ------------------------------------------------------------------ Seiten
def page_home(lang):
    welcome = "".join(f"<p>{p[lang]}</p>" for p in HOME["welcome"])
    body = f"""<section class="hero">
  <div class="slides" aria-hidden="true">
    <img src="{IMG}hero-1.webp" alt="" fetchpriority="high"><img src="{IMG}hero-2.webp" alt="" loading="lazy"><img src="{IMG}hero-3.webp" alt="" loading="lazy">
  </div>
  <div class="wrap hero-inner">
    <div class="hero-box">
      <p class="eyebrow">{HOME['eyebrow'][lang]}</p>
      <h1>{HOME['h1'][lang]}</h1>
      <p>{HOME['lead'][lang]}</p>
      <div class="btns"><a class="btn btn-light" href="{u(lang, 'products.html')}">{UI['products'][lang]} ›</a><a class="btn btn-ghost" href="{u(lang, 'contact.html')}">{UI['contact'][lang]}</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow center">
    <h2 class="title">{HOME['welcome_h'][lang]}</h2>
    {welcome}
  </div>
</section>

<section class="section soft">
  <div class="wrap">
    <h2 class="title">{HOME['sourcing_h'][lang]}</h2>
    <p class="intro">{HOME['sourcing'][lang]}</p>
    <div class="mgrid">{member_cards(lang)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="title">{HOME['products_h'][lang]}</h2>
    <div class="cgrid">{cat_cards(lang)}</div>
  </div>
</section>

<section class="cta">
  <div class="wrap cta-inner">
    <p>{CONTACT['lead'][lang]}</p>
    <a class="btn btn-light" href="{u(lang, 'contact.html')}">{UI['contact'][lang]} ›</a>
  </div>
</section>"""
    return page(lang, "", "home", "", body)


def page_company(lang):
    secs = "".join(
        f'<div class="block"><h2>{h[lang]}</h2>' + "".join(f"<p>{p[lang]}</p>" for p in ps) + "</div>"
        for h, ps in COMPANY["sections"])
    areas = "".join(f'<li><a href="{u(lang, "products.html")}#{c["id"]}">{c["name"][lang]}</a></li>' for c in CATEGORIES)
    body = page_header(lang, UI["company"][lang], [(UI["company"][lang], "")]) + f"""
<section class="section">
  <div class="wrap two">
    <div class="prose"><p class="lead-text">{COMPANY['intro'][lang]}</p>{secs}</div>
    <aside class="side-box">
      <h3>{UI['products'][lang]}</h3><ul class="arrow">{areas}</ul>
      <h3>{UI['sourcing'][lang]}</h3><ul class="arrow">{''.join(f'<li><a href="{u(lang, "sourcing/" + m["id"] + ".html")}">{m["name"]}</a></li>' for m in MEMBERS)}</ul>
    </aside>
  </div>
</section>"""
    return page(lang, "company.html", "company", UI["company"][lang], body)


ICONS = [
    '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>',
    '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
    '<path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
]


def page_advantages(lang):
    items = "".join(
        f'<div class="adv"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[i]}</svg><h2>{h[lang]}</h2><p>{t[lang]}</p></div>'
        for i, (h, t) in enumerate(ADVANTAGES["items"]))
    body = page_header(lang, UI["advantages"][lang], [(UI["advantages"][lang], "")], "hero-1.webp") + f"""
<section class="section">
  <div class="wrap">
    <p class="intro big">{ADVANTAGES['intro'][lang]}</p>
    <div class="advgrid">{items}</div>
    {request_box(lang)}
  </div>
</section>"""
    return page(lang, "advantages.html", "advantages", UI["advantages"][lang], body)


def page_products(lang):
    intro = "".join(f"<p>{p[lang]}</p>" for p in CATALOG_INTRO)
    cats = "".join(f"""<section class="catsec" id="{c['id']}">
  <div class="cathead"><img src="{IMG}{c['img']}" alt="" loading="lazy"><div><h2>{c['name'][lang]}</h2><p>{c['text'][lang]}</p></div></div>
  <div class="pgrid">{product_cards(lang, [p for p in PRODUCTS if p['cat'] == c['id']], 'products/')}</div>
</section>""" for c in CATEGORIES)
    body = page_header(lang, UI["products"][lang], [(UI["products"][lang], "")], "cat-bettwaren.webp") + f"""
<section class="section">
  <div class="wrap">
    <div class="prose narrow">{intro}</div>
    {cats}
    {request_box(lang)}
  </div>
</section>"""
    return page(lang, "products.html", "products", UI["products"][lang], body)


def product_sidebar(lang, current):
    out = []
    for c in CATEGORIES:
        items = "".join(
            f'<li><a href="{p["id"]}.html"' + (' aria-current="page"' if p["id"] == current else "") + f'>{p["name"][lang]}</a></li>'
            for p in PRODUCTS if p["cat"] == c["id"])
        out.append(f'<details class="sidecat"' + (" open" if any(p["id"] == current and p["cat"] == c["id"] for p in PRODUCTS) else "") +
                   f'><summary>{c["name"][lang]}</summary><ul>{items}</ul></details>')
    return '<aside class="sidebar">' + "".join(out) + "</aside>"


def page_product(lang, p):
    c = CAT[p["cat"]]
    imgs = [f"{IMG}p-{p['img']}-{i}.webp" for i in range(1, p["n"] + 1)]
    thumbs = "".join(
        f'<button type="button" class="thumb" data-src="{s}" aria-label="{p["name"][lang]} {i + 1}"><img src="{s}" alt="" loading="lazy"></button>'
        for i, s in enumerate(imgs))
    others = [x for x in PRODUCTS if x["cat"] == p["cat"] and x["id"] != p["id"]][:4]
    body = page_header(lang, p["name"][lang], [(UI["products"][lang], u(lang, "products.html")),
                                                (c["name"][lang], u(lang, "products.html") + "#" + c["id"]),
                                                (p["name"][lang], "")], c["img"]) + f"""
<section class="section">
  <div class="wrap with-side">
    {product_sidebar(lang, p['id'])}
    <div class="content">
      <h2 class="ptitle">{p['name'][lang]}</h2>
      <p class="lead-text">{p['desc'][lang]}</p>
      <figure class="gallery"><img class="gallery-main" src="{imgs[0]}" alt="{p['name'][lang]}"></figure>
      <div class="thumbs">{thumbs}</div>
      <p class="muted">{UI['selection'][lang]}</p>
      {request_box(lang)}
      <h3 class="subtitle">{UI['other_products'][lang]}</h3>
      <div class="pgrid small">{product_cards(lang, others)}</div>
    </div>
  </div>
</section>"""
    return page(lang, f"products/{p['id']}.html", "products", p["name"][lang], body)


def page_sourcing(lang):
    body = page_header(lang, UI["sourcing"][lang], [(UI["sourcing"][lang], "")], "hero-2.webp") + f"""
<section class="section">
  <div class="wrap">
    <p class="intro big">{HOME['sourcing'][lang]}</p>
    <div class="mgrid">{member_cards(lang)}</div>
  </div>
</section>"""
    return page(lang, "sourcing.html", "sourcing", UI["sourcing"][lang], body)


def page_member(lang, m):
    side = "".join(
        f'<li><a href="{x["id"]}.html"' + (' aria-current="page"' if x["id"] == m["id"] else "") + f'>{x["name"]}</a></li>'
        for x in MEMBERS)
    text = "".join(f"<p>{p[lang]}</p>" for p in m["text"])
    since = f'<p class="badge">{UI["since"][lang].format(y=m["since"])}</p>' if m["since"] else ""
    image = f'<img class="member-img" src="{IMG}{m["image"]}" alt="" loading="lazy">' if m.get("image") else ""
    team = "".join(
        f'<div class="tm"><img src="{IMG}{photo}" alt="{name}" width="120" height="120" loading="lazy"><strong>{name}</strong><span>{ROLES[role][lang]}</span></div>'
        for name, role, photo in m["team"])
    phones = "".join(f'<br>{UI["phone"][lang]} <a href="tel:{ph.split(" (")[0].replace(" ", "")}">{ph}</a>' for ph in m["phones"])
    web = f'<br><a href="{m["web"]}" rel="noopener">{m["web"].replace("https://", "")}</a>' if m.get("web") else ""
    body = page_header(lang, m["name"], [(UI["sourcing"][lang], u(lang, "sourcing.html")), (m["name"], "")], "hero-2.webp") + f"""
<section class="section">
  <div class="wrap with-side">
    <aside class="sidebar"><div class="sidecat static"><p class="sidecat-h">{UI['sourcing'][lang]}</p><ul>{side}</ul></div></aside>
    <div class="content">
      <div class="member-head"><span class="mcard-logo big"><img src="{IMG}{m['logo']}" alt="{m['name']}"></span><div><h2 class="ptitle">{m['name']}</h2><p class="muted">{m['loc'][lang]}</p>{since}</div></div>
      <div class="prose">{text}</div>
      {image}
      <h3 class="subtitle">{UI['team'][lang]}</h3>
      <div class="team">{team}</div>
      <div class="contact-box"><h3>{UI['contact_h'][lang]}</h3><address>{'<br>'.join(m['address'])}{phones}<br><a href="mailto:{m['email']}">{m['email']}</a>{web}</address></div>
      <p><a href="{u(lang, 'sourcing.html')}">‹ {UI['back'][lang]}</a></p>
    </div>
  </div>
</section>"""
    return page(lang, f"sourcing/{m['id']}.html", "sourcing", m["name"], body)


def page_contact(lang):
    people = "".join(
        f'<div class="person"><img src="{IMG}{c["photo"]}" alt="{c["name"]}" width="96" height="96" loading="lazy"><div><strong>{c["name"]}</strong><span>{UI["ceo"][lang]}</span>'
        f'<a href="tel:{c["phone"].replace(" ", "")}">{c["phone"]}</a><a href="mailto:{c["email"]}">{c["email"]}</a></div></div>'
        for c in CEOS)
    hint = CONTACT["f_hint"][lang].format(privacy=f'<a href="{legal_link(lang, 1)}">{CONTACT["privacy_link"][lang]}</a>')
    mem = "".join(
        f'<div class="mini"><img src="{IMG}{m["logo"]}" alt="" loading="lazy"><div><a href="{u(lang, "sourcing/" + m["id"] + ".html")}"><strong>{m["name"]}</strong></a><span>{m["loc"][lang]}</span><a href="mailto:{m["email"]}">{m["email"]}</a></div></div>'
        for m in MEMBERS)
    body = page_header(lang, UI["contact"][lang], [(UI["contact"][lang], "")], "hero-1.webp") + f"""
<section class="section">
  <div class="wrap two">
    <div>
      <h2 class="title left">{CONTACT['h'][lang]}</h2>
      <p class="lead-text">{CONTACT['lead'][lang]}</p>
      <div class="people">{people}</div>
      <address class="hq">{'<br>'.join(HQ)}</address>
    </div>
    <form class="form" id="formular" action="/kontakt.php" method="post">
      <h2>{CONTACT['form_h'][lang]}</h2>
      <p class="notice ok" id="form-ok" role="status" hidden>{CONTACT['f_ok'][lang]}</p>
      <p class="notice err" id="form-err" role="alert" hidden>{CONTACT['f_err'][lang]}</p>
      <input type="hidden" name="lang" value="{lang}"><input type="hidden" name="ts" value="">
      <label>{CONTACT['f_name'][lang]}<input type="text" name="name" required maxlength="120" autocomplete="name"></label>
      <label>{CONTACT['f_company'][lang]}<input type="text" name="company" maxlength="160" autocomplete="organization"></label>
      <label class="full">{CONTACT['f_email'][lang]}<input type="email" name="email" required maxlength="160" autocomplete="email"></label>
      <label class="full">{CONTACT['f_msg'][lang]}<textarea name="message" rows="6" required maxlength="5000"></textarea></label>
      <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <p class="hint">{hint}</p>
      <button class="btn" type="submit">{CONTACT['f_send'][lang]}</button>
    </form>
  </div>
</section>
<section class="section soft">
  <div class="wrap">
    <h2 class="title">{CONTACT['members_h'][lang]}</h2>
    <div class="minigrid">{mem}</div>
  </div>
</section>"""
    return page(lang, "contact.html", "contact", UI["contact"][lang], body)


# ------------------------------------------------------------------ Rechtliches
DRAFT = {
    "de": "ENTWURF – Angaben in [eckigen Klammern] ergänzen und rechtlich prüfen lassen, bevor die Seite live geht.",
    "en": "DRAFT – complete the items in [square brackets] and have this reviewed before going live.",
}
LEGAL_TEXT = {
    ("de", 0): ("Impressum", f"""
<h2>Angaben zum Unternehmen</h2><p>{'<br>'.join(HQ)}</p>
<p>Vertreten durch: [Name(n) der vertretungsberechtigten Person(en)]<br>Handelsregister: [Kanton / Registernummer]<br>UID: [CHE-xxx.xxx.xxx]</p>
<h2>Kontakt</h2><p>E-Mail: <a href="mailto:info@nagroup.biz">info@nagroup.biz</a><br>Telefon: [Telefonnummer]</p>
<h2>Haftung für Links</h2><p>Für Inhalte externer Websites, auf die wir verlinken, sind ausschließlich deren Betreiber verantwortlich.</p>"""),
    ("de", 1): ("Datenschutzerklärung", """
<h2>Verantwortlich</h2><p>Neidhart &amp; Arbenz AG, Tüfenwiesstrasse 14 A, 9524 Zuzwil SG, Schweiz – <a href="mailto:info@nagroup.biz">info@nagroup.biz</a></p>
<h2>Hosting und Server-Logfiles</h2><p>Diese Website wird bei Media Serv SRL (Rumänien, EU) gehostet. Beim Aufruf werden technisch notwendige Daten (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browser-Kennung) in Server-Logfiles gespeichert, um den sicheren Betrieb zu gewährleisten. [Speicherdauer beim Hoster prüfen.]</p>
<h2>Kontaktformular und E-Mail</h2><p>Wenn Sie uns über das Formular oder per E-Mail kontaktieren, verarbeiten wir Ihre Angaben (Name, Firma, E-Mail-Adresse, Nachricht) ausschließlich zur Bearbeitung Ihrer Anfrage. Die Nachricht wird per E-Mail an uns übermittelt; unser E-Mail-Dienst ist Microsoft 365. Eine Weitergabe an Dritte findet nicht statt.</p>
<h2>Keine Cookies, kein Tracking</h2><p>Diese Website setzt keine Cookies und verwendet keine Analyse- oder Tracking-Dienste. Schriften werden lokal vom eigenen Server geladen.</p>
<h2>Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung Ihrer Daten sowie auf Datenübertragbarkeit und Widerspruch (DSGVO bzw. Schweizer DSG). Wenden Sie sich dazu an die oben genannte Adresse. Zudem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren.</p>"""),
    ("en", 0): ("Legal notice", f"""
<h2>Company details</h2><p>{'<br>'.join(HQ)}</p>
<p>Represented by: [name(s) of authorised representative(s)]<br>Commercial register: [canton / register number]<br>VAT/UID: [CHE-xxx.xxx.xxx]</p>
<h2>Contact</h2><p>Email: <a href="mailto:info@nagroup.biz">info@nagroup.biz</a><br>Phone: [phone number]</p>
<h2>External links</h2><p>The operators of linked external websites are solely responsible for their content.</p>"""),
    ("en", 1): ("Privacy policy", """
<h2>Controller</h2><p>Neidhart &amp; Arbenz AG, Tüfenwiesstrasse 14 A, 9524 Zuzwil SG, Switzerland – <a href="mailto:info@nagroup.biz">info@nagroup.biz</a></p>
<h2>Hosting and server log files</h2><p>This website is hosted by Media Serv SRL (Romania, EU). When you visit it, technically necessary data (IP address, date and time, page requested, browser identifier) is stored in server log files to ensure secure operation. [Check retention period with the host.]</p>
<h2>Contact form and email</h2><p>If you contact us via the form or by email, we process your details (name, company, email address, message) solely to handle your enquiry. The message is sent to us by email; our email service is Microsoft 365. Your data is not passed on to third parties.</p>
<h2>No cookies, no tracking</h2><p>This website does not set cookies and does not use analytics or tracking services. Fonts are served from our own server.</p>
<h2>Your rights</h2><p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection (GDPR / Swiss FADP). Please contact us at the address above. You may also lodge a complaint with a data protection authority.</p>"""),
}


def page_legal(lang, kind):
    title, body = LEGAL_TEXT[(lang, kind)]
    path = LEGAL[lang][kind]
    html = page_header(lang, title, [(title, "")], "hero-3.webp") + \
        f'<section class="section"><div class="wrap narrow prose legal"><p class="draft">{DRAFT[lang]}</p>{body}</div></section>'
    return page(lang, path, "", title, html)


# ------------------------------------------------------------------ Start
def main():
    # alte Einzelseiten-Struktur aufräumen (nur lokal; auf dem Server bleiben alte Dateien liegen)
    for lang in LANGS:
        for sub in ("products", "sourcing"):
            d = os.path.join(OUT, lang, sub)
            if os.path.isdir(d):
                shutil.rmtree(d)
    n = 0
    for lang in LANGS:
        write(f"{lang}/index.html", page_home(lang))
        write(f"{lang}/company.html", page_company(lang))
        write(f"{lang}/advantages.html", page_advantages(lang))
        write(f"{lang}/products.html", page_products(lang))
        write(f"{lang}/sourcing.html", page_sourcing(lang))
        write(f"{lang}/contact.html", page_contact(lang))
        n += 6
        for p in PRODUCTS:
            write(f"{lang}/products/{p['id']}.html", page_product(lang, p))
            n += 1
        for m in MEMBERS:
            write(f"{lang}/sourcing/{m['id']}.html", page_member(lang, m))
            n += 1
    for lang in LEGAL:
        for kind in (0, 1):
            write(f"{lang}/{LEGAL[lang][kind]}", page_legal(lang, kind))
            n += 1
    print(f"{n} Seiten erzeugt.")


if __name__ == "__main__":
    main()
