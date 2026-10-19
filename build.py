#!/usr/bin/env python3
"""Erzeugt die HTML-Seiten in public/ aus src/content.py.

Aufruf:  python3 build.py
Danach Änderungen committen und pushen – der Server holt sie per cPanel-Git ab.
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from content import LANGS, LANG_LABEL, CEOS, HQ, MEMBERS, T  # noqa: E402

BASE = "https://nagroup.biz"
OUT = os.path.join(os.path.dirname(__file__), "public")
def ver(rel):
    """Kurzer Inhalts-Hash als Cache-Buster, z. B. style.css?v=1a2b3c4d."""
    with open(os.path.join(OUT, rel.lstrip("/")), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


LEGAL = {  # Sprache -> (Impressum-Datei, Datenschutz-Datei)
    "de": ("impressum.html", "datenschutz.html"),
    "en": ("legal-notice.html", "privacy.html"),
}


def legal_link(lang, kind):
    """Link auf Impressum (0) bzw. Datenschutz (1) – ES/ZH verweisen auf Englisch."""
    target = T[lang]["legal_lang"]
    return f"/{target}/{LEGAL[target][kind]}"


def head(lang, title, desc, path):
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{BASE}/{l}/">' for l in LANGS
    )
    return f"""<!doctype html>
<html lang="{'zh-Hans' if lang == 'zh' else lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
{alts}
<link rel="alternate" hreflang="x-default" href="{BASE}/en/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/space-grotesk-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={ver('/assets/css/style.css')}">
</head>
<body>"""


def header(lang, onepage=True):
    t = T[lang]
    pre = "" if onepage else f"/{lang}/"
    nav = "".join(f'<a href="{pre}#{k}">{v}</a>' for k, v in t["nav"].items())
    langs = "".join(
        f'<a href="/{l}/" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == lang else "") + f">{LANG_LABEL[l]}</a>"
        for l in LANGS
    )
    return f"""<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/{lang}/"><img src="/assets/img/na-logo.webp" width="52" height="45" alt="NA Group – Natural Advantage"></a>
    <nav class="nav" aria-label="{t['nav']['netzwerk']}">{nav}</nav>
    <div class="lang">{langs}</div>
  </div>
</header>"""


def footer(lang):
    t = T[lang]
    return f"""<footer class="site-footer">
  <div class="wrap">
    <span>{' · '.join(HQ[:3])}</span>
    <nav aria-label="{t['imprint']}"><a href="{legal_link(lang, 0)}">{t['imprint']}</a><a href="{legal_link(lang, 1)}">{t['privacy_short']}</a></nav>
  </div>
</footer>
<script src="/assets/js/main.js?v={ver('/assets/js/main.js')}" defer></script>
</body>
</html>
"""


def members(lang, region):
    t = T[lang]
    out = []
    for m in MEMBERS[region]:
        since = f"<p>{t['since'].format(y=m['since'])}</p>" if m["since"] else ""
        addr = "<br>".join(m["address"])
        out.append(f"""<details class="member" id="{m['id']}">
  <summary><span class="mlogo"><img src="/assets/img/{m['logo']}" alt="" loading="lazy" decoding="async"></span><span class="mname">{m['name']}</span><span class="loc">{t['loc'][m['id']]}</span></summary>
  <div class="body">
    <p>{t['about'][m['id']]}</p>{since}
    <address>{addr}<br><a href="mailto:{m['email']}">{m['email']}</a></address>
  </div>
</details>""")
    return "\n".join(out)


def page_home(lang):
    t = T[lang]
    steps = "".join(
        f'<li><span class="n">0{i}</span><strong>{s}</strong><p>{d}</p></li>'
        for i, (s, d) in enumerate(t["steps"], 1)
    )
    chips = "".join(f"<li>{r}</li>" for r in t["range"])
    allm = MEMBERS["asia"][:1] + MEMBERS["europe"][:2] + MEMBERS["europe"][2:] + MEMBERS["asia"][1:]
    strip = "".join(
        f'<li><a href="#{m["id"]}" title="{m["name"]}"><img src="/assets/img/{m["logo"]}" alt="{m["name"]}" loading="lazy" decoding="async"></a></li>'
        for m in allm
    )
    cat_imgs = ["cat-bettwaren.webp", "cat-matratzenzubehoer.webp", "cat-promo.webp"]
    cats = "".join(
        f'<figure class="cat"><img src="/assets/img/{img}" alt="" loading="lazy" decoding="async"><figcaption>{name}</figcaption></figure>'
        for img, name in zip(cat_imgs, t["cats"])
    )
    facts = "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in t["facts"])
    paras = "".join(f"<p>{p}</p>" for p in t["company_p"])
    people = "".join(
        f'<div class="person"><img class="avatar" src="/assets/img/{c["photo"]}" width="80" height="80" alt="{c["name"]}" loading="lazy"><strong>{c["name"]}</strong><span>{t["ceo"]}</span>'
        f'<a href="tel:{c["phone"].replace(" ", "")}">{c["phone"]}</a><br>'
        f'<a href="mailto:{c["email"]}">{c["email"]}</a></div>'
        for c in CEOS
    )
    hint = t["f_hint"].format(privacy=f'<a href="{legal_link(lang, 1)}">{t["privacy"]}</a>')
    arrow = ('<svg width="140" height="40" viewBox="0 0 140 40" aria-hidden="true">'
             '<path d="M4 20H136" stroke="#5ec2b7" stroke-width="2" stroke-dasharray="6 6"/>'
             '<path d="M124 10L136 20 124 30M16 10L4 20 16 30" fill="none" stroke="#5ec2b7" stroke-width="2"/></svg>')
    return head(lang, t["title"], t["description"], f"/{lang}/") + header(lang) + f"""
<main id="main">
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="eyebrow">{t['eyebrow']}</p>
      <h1>{t['h1']}</h1>
      <p class="lead">{t['lead']}</p>
      <div class="btns"><a class="btn btn-primary" href="#kontakt">{t['cta1']}</a><a class="btn" href="#netzwerk">{t['cta2']}</a></div>
    </div>
    <div class="hero-media" role="img" aria-label="{t['hero_alt']}">
      <img src="/assets/img/hero-2.webp" alt="" width="1599" height="869" fetchpriority="high">
      <img src="/assets/img/hero-1.webp" alt="" width="1600" height="1068" loading="lazy">
      <img src="/assets/img/hero-3.webp" alt="" width="1471" height="860" loading="lazy">
    </div>
  </div>
</section>

<section class="logostrip" aria-label="{t['nav']['netzwerk']}">
  <div class="wrap"><ul>{strip}</ul></div>
</section>

<section class="network" id="netzwerk" aria-label="{t['nav']['netzwerk']}">
  <div class="wrap">
    <div class="net">
      <div class="net-col">
        <span class="region">{t['eu_region']}</span>
        <h2>{t['eu_h']}</h2>
        {members(lang, 'europe')}
      </div>
      <div class="net-mid">{arrow}<strong>{t['mid']}<small>{t['mid_sub']}</small></strong></div>
      <div class="net-col">
        <span class="region">{t['as_region']}</span>
        <h2>{t['as_h']}</h2>
        {members(lang, 'asia')}
      </div>
    </div>
  </div>
</section>

<div class="light">
<section class="section" id="ablauf">
  <div class="wrap">
    <h2>{t['steps_h']}</h2>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="section" id="sortiment" style="padding-top:0">
  <div class="wrap">
    <h2>{t['range_h']}</h2>
    <div class="cats">{cats}</div>
    <ul class="chips">{chips}</ul>
  </div>
</section>

<section class="section" id="unternehmen" style="padding-top:0">
  <div class="wrap split">
    <div class="prose"><h2>{t['company_h']}</h2>{paras}</div>
    <ul class="facts">{facts}</ul>
  </div>
</section>
</div>

<section class="section contact" id="kontakt">
  <div class="wrap split">
    <div>
      <h2>{t['contact_h']}</h2>
      <p class="lead">{t['contact_lead']}</p>
      <div class="people">{people}</div>
    </div>
    <form class="form" action="/kontakt.php" method="post">
      <p class="notice ok" id="form-ok" role="status" hidden>{t['f_ok']}</p>
      <p class="notice err" id="form-err" role="alert" hidden>{t['f_err']}</p>
      <input type="hidden" name="lang" value="{lang}">
      <input type="hidden" name="ts" value="">
      <label>{t['f_name']}<input type="text" name="name" required maxlength="120" autocomplete="name"></label>
      <label>{t['f_company']}<input type="text" name="company" maxlength="160" autocomplete="organization"></label>
      <label class="full">{t['f_email']}<input type="email" name="email" required maxlength="160" autocomplete="email"></label>
      <label class="full">{t['f_msg']}<textarea name="message" rows="5" required maxlength="5000"></textarea></label>
      <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <p class="hint">{hint}</p>
      <button class="btn btn-primary" type="submit">{t['f_send']}</button>
    </form>
  </div>
</section>
</main>
""" + footer(lang)


DRAFT = {
    "de": "ENTWURF – Angaben in [eckigen Klammern] ergänzen und rechtlich prüfen lassen, bevor die Seite live geht.",
    "en": "DRAFT – complete the items in [square brackets] and have this reviewed before going live.",
}

LEGAL_TEXT = {
    ("de", 0): ("Impressum", f"""
<h2>Angaben zum Unternehmen</h2>
<p>{'<br>'.join(HQ)}</p>
<p>Vertreten durch: [Name(n) der vertretungsberechtigten Person(en)]<br>
Handelsregister: [Kanton / Registernummer]<br>
UID: [CHE-xxx.xxx.xxx]</p>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:info@nagroup.biz">info@nagroup.biz</a><br>Telefon: [Telefonnummer]</p>
<h2>Haftung für Links</h2>
<p>Für Inhalte externer Websites, auf die wir verlinken, sind ausschließlich deren Betreiber verantwortlich.</p>
"""),
    ("de", 1): ("Datenschutzerklärung", """
<h2>Verantwortlich</h2>
<p>Neidhart &amp; Arbenz AG, Tüfenwiesstrasse 14 A, 9524 Zuzwil SG, Schweiz – <a href="mailto:info@nagroup.biz">info@nagroup.biz</a></p>
<h2>Hosting und Server-Logfiles</h2>
<p>Diese Website wird bei Media Serv SRL (Rumänien, EU) gehostet. Beim Aufruf werden technisch notwendige Daten (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browser-Kennung) in Server-Logfiles gespeichert, um den sicheren Betrieb zu gewährleisten. [Speicherdauer beim Hoster prüfen.]</p>
<h2>Kontaktformular und E-Mail</h2>
<p>Wenn Sie uns über das Formular oder per E-Mail kontaktieren, verarbeiten wir Ihre Angaben (Name, Firma, E-Mail-Adresse, Nachricht) ausschließlich zur Bearbeitung Ihrer Anfrage. Die Nachricht wird per E-Mail an uns übermittelt; unser E-Mail-Dienst ist Microsoft 365. Eine Weitergabe an Dritte findet nicht statt.</p>
<h2>Keine Cookies, kein Tracking</h2>
<p>Diese Website setzt keine Cookies und verwendet keine Analyse- oder Tracking-Dienste. Schriften werden lokal vom eigenen Server geladen.</p>
<h2>Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung Ihrer Daten sowie auf Datenübertragbarkeit und Widerspruch (DSGVO bzw. Schweizer DSG). Wenden Sie sich dazu an die oben genannte Adresse. Zudem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren.</p>
"""),
    ("en", 0): ("Legal notice", f"""
<h2>Company details</h2>
<p>{'<br>'.join(HQ)}</p>
<p>Represented by: [name(s) of authorised representative(s)]<br>
Commercial register: [canton / register number]<br>
VAT/UID: [CHE-xxx.xxx.xxx]</p>
<h2>Contact</h2>
<p>Email: <a href="mailto:info@nagroup.biz">info@nagroup.biz</a><br>Phone: [phone number]</p>
<h2>External links</h2>
<p>The operators of linked external websites are solely responsible for their content.</p>
"""),
    ("en", 1): ("Privacy policy", """
<h2>Controller</h2>
<p>Neidhart &amp; Arbenz AG, Tüfenwiesstrasse 14 A, 9524 Zuzwil SG, Switzerland – <a href="mailto:info@nagroup.biz">info@nagroup.biz</a></p>
<h2>Hosting and server log files</h2>
<p>This website is hosted by Media Serv SRL (Romania, EU). When you visit it, technically necessary data (IP address, date and time, page requested, browser identifier) is stored in server log files to ensure secure operation. [Check retention period with the host.]</p>
<h2>Contact form and email</h2>
<p>If you contact us via the form or by email, we process your details (name, company, email address, message) solely to handle your enquiry. The message is sent to us by email; our email service is Microsoft 365. Your data is not passed on to third parties.</p>
<h2>No cookies, no tracking</h2>
<p>This website does not set cookies and does not use analytics or tracking services. Fonts are served from our own server.</p>
<h2>Your rights</h2>
<p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection (GDPR / Swiss FADP). Please contact us at the address above. You may also lodge a complaint with a data protection authority.</p>
"""),
}


def page_legal(lang, kind):
    title, body = LEGAL_TEXT[(lang, kind)]
    path = f"/{lang}/{LEGAL[lang][kind]}"
    return (head(lang, f"{title} – NA Group", title, path) + header(lang, onepage=False)
            + f'<main id="main" class="wrap legal"><h1>{title}</h1><p class="draft">{DRAFT[lang]}</p>{body}</main>'
            + footer(lang))


def write(rel, html):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ", rel)


def main():
    print("Erzeuge Seiten:")
    for lang in LANGS:
        write(f"{lang}/index.html", page_home(lang))
    for lang in LEGAL:
        for kind in (0, 1):
            write(f"{lang}/{LEGAL[lang][kind]}", page_legal(lang, kind))


if __name__ == "__main__":
    main()
