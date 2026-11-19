"""Builds index.html (English), de/index.html and id/index.html from content.py."""
from pathlib import Path
from urllib.parse import quote
from content import T, EMAIL, WA, PORTFOLIO, LINKEDIN, GITHUB, WORK_LINKS

BASE = "https://sayamrina.github.io/amrinawork/"
ROOT = Path(__file__).parent
PATHS = {"en": "", "de": "de/", "id": "id/"}
HTML_LANG = {"en": "en", "de": "de", "id": "id"}
SHORT = {"en": "EN", "de": "DE", "id": "ID"}


def page(lang):
    t = T[lang]
    up = "" if lang == "en" else "../"
    mail = f"mailto:{EMAIL}?subject={quote(t['mail_subject'])}"
    wa = f"https://wa.me/{WA}"

    def lang_href(l):
        return up + PATHS[l] if PATHS[l] else (up or "./")

    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{BASE}{PATHS[l]}">' for l in T
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'

    nav = "\n".join(f'<a href="#{i}">{label}</a>' for i, label in t["nav"])
    switch = "".join(
        f'<a href="{lang_href(l)}" data-lang="{l}" hreflang="{l}" lang="{l}"'
        + (' aria-current="true"' if l == lang else "")
        + f' title="{T[l]["lang_name"]}">{SHORT[l]}</a>'
        for l in T
    )
    dlg_buttons = "\n".join(
        f'<a class="dlg-lang" href="{lang_href(l)}" data-lang="{l}" lang="{l}" hreflang="{l}">'
        f'<span class="dlg-code">{SHORT[l]}</span><span>{T[l]["lang_name"]}</span></a>'
        for l in T
    )
    dlg_others = "".join(f'<p lang="{l}">{T[l]["dlg_title"]}</p>' for l in T if l != lang)

    services = "\n".join(
        f"""<li class="svc">
  <h3>{name}</h3>
  <div><p>{body}</p><p class="svc-ex"><span>{t['examples']}:</span> {ex}</p></div>
</li>""" for name, body, ex in t["services"])

    def links(key):
        out = []
        for kind, url in WORK_LINKS[key]:
            label = t["link_live"] if kind == "live" else t["link_page"]
            out.append(f'<a href="{url}" target="_blank" rel="noopener">{label}</a>')
        return " ".join(out)

    work = "\n".join(
        f"""<article class="case">
  <p class="case-kind">{kind}</p>
  <h3>{title}</h3>
  <dl>
    <dt>{t['lbl_problem']}</dt><dd>{prob}</dd>
    <dt>{t['lbl_solution']}</dt><dd>{sol}</dd>
    <dt>{t['lbl_result']}</dt><dd class="case-result">{res}</dd>
  </dl>
  <p class="case-links">{links(key)}</p>
</article>""" for key, kind, title, prob, sol, res in t["work"])

    process = "\n".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in t["process"])
    about = "\n".join(f"<p>{p}</p>" for p in t["about"])
    tools = "\n".join(f"<div><dt>{g}</dt><dd>{items}</dd></div>" for g, items in t["tools"])
    faq = "\n".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])

    return f"""<!doctype html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['description']}">
<link rel="canonical" href="{BASE}{PATHS[lang]}">
{alternates}
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['description']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{PATHS[lang]}">
<meta name="theme-color" content="#f4f6f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0f1519" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,650;12..96,750&family=Hanken+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
</head>
<body data-lang="{lang}">
<a class="skip" href="#main">{t['skip']}</a>

<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="#main"><span class="mark" aria-hidden="true"></span><span>Amrina<small>{t['role']}</small></span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">{t['menu']}</button>
    <nav id="nav" class="nav" aria-label="Main">
      {nav}
    </nav>
    <div class="switch" role="group" aria-label="{t['lang_switch']}">{switch}</div>
    <a class="btn btn-small" href="#contact">{t['nav_cta']}</a>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <h1>{t['hero_h1']}</h1>
      <p class="lede">{t['hero_lede']}</p>
      <p class="actions"><a class="btn" href="#contact">{t['cta_primary']}</a> <a class="btn btn-line" href="{wa}" target="_blank" rel="noopener">{t['cta_wa']}</a></p>
    </div>
    <figure class="chat" aria-label="{t['chat_label']}">
      <figcaption>{t['chat_label']}</figcaption>
      <div class="msg msg-guest">{t['chat_guest']}</div>
      <div class="typing" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="msg msg-ai">{t['chat_answer']}</div>
      <div class="source" id="src1"><span class="source-n">1</span><div><span class="source-t">{t['chat_source_title']}</span>{t['chat_source']}</div></div>
      <p class="chat-note">{t['chat_note']}</p>
    </figure>
  </div>
</section>

<section id="services" class="block">
  <div class="wrap">
    <div class="head"><h2>{t['services_h']}</h2><p>{t['services_intro']}</p></div>
    <ul class="svcs">
{services}
    </ul>
  </div>
</section>

<section id="work" class="block block-tint">
  <div class="wrap">
    <div class="head"><h2>{t['work_h']}</h2><p>{t['work_intro']}</p></div>
    <div class="cases">
{work}
    </div>
    <p class="more">{t['work_more']} <a href="{PORTFOLIO}" target="_blank" rel="noopener">{t['work_more_link']}</a></p>
  </div>
</section>

<section id="process" class="block">
  <div class="wrap">
    <div class="head"><h2>{t['process_h']}</h2></div>
    <ol class="steps">
{process}
    </ol>
  </div>
</section>

<section id="tools" class="block block-tint">
  <div class="wrap">
    <div class="head"><h2>{t['tools_h']}</h2><p>{t['tools_intro']}</p></div>
    <dl class="tools">
{tools}
    </dl>
  </div>
</section>

<section id="about" class="block">
  <div class="wrap about">
    <h2>{t['about_h']}</h2>
    <div>
{about}
      <p class="about-links"><span>{t['about_links']}:</span> <a href="{PORTFOLIO}" target="_blank" rel="noopener">sayamrina.github.io</a> <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></p>
    </div>
  </div>
</section>

<section id="faq" class="block block-tint">
  <div class="wrap faq">
    <h2>{t['faq_h']}</h2>
    <div class="faq-list">
{faq}
    </div>
  </div>
</section>

<section id="contact" class="contact">
  <div class="wrap">
    <h2>{t['contact_h']}</h2>
    <p>{t['contact_p']}</p>
    <p class="actions"><a class="btn btn-invert" href="{mail}">{t['contact_mail']}</a> <a class="btn btn-line-invert" href="{wa}" target="_blank" rel="noopener">{t['contact_wa']}</a></p>
    <p class="contact-direct"><a href="{mail}">{EMAIL}</a></p>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap foot-in">
    <p>© 2026 {t['footer']}</p>
    <p><a href="{PORTFOLIO}" target="_blank" rel="noopener">{t['footer_portfolio']}</a> <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></p>
  </div>
</footer>

<dialog id="lang-dialog" class="dlg" aria-labelledby="dlg-title">
  <h2 id="dlg-title">{t['dlg_title']}</h2>
  <div class="dlg-others">{dlg_others}</div>
  <div class="dlg-langs">
{dlg_buttons}
  </div>
  <p class="dlg-note">{t['dlg_note']}</p>
</dialog>

<script src="{up}main.js"></script>
</body>
</html>
"""


for lang in T:
    out = ROOT / PATHS[lang] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page(lang), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))
