"""Builds index.html (English), de/index.html and id/index.html from content.py."""
import re
from pathlib import Path
from urllib.parse import quote
from content import T, EMAIL, WA, BOOKING, PORTFOLIO, LINKEDIN, GITHUB, WORK, WORK_LINKS, TOOLS, SERVICE_KEYS

BASE = "https://sayamrina.github.io/amrinawork/"
ROOT = Path(__file__).parent
PATHS = {"en": "", "de": "de/", "id": "id/"}
SHORT = {"en": "EN", "de": "DE", "id": "ID"}
NOTAB = ' tabindex="-1"'
CHECK = '<svg class="ck" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def icon(name):
    svg = (ROOT / "icons" / f"{name}.svg").read_text()
    svg = re.sub(r"<title>.*?</title>", "", svg)
    return svg.replace('role="img"', 'aria-hidden="true" fill="currentColor"')


def viz(key, v, up):
    if key == "chat":
        return f"""<div class="vz vz-chat">
  <div class="b b-guest">{v['chat_q']}</div>
  <div class="b b-ai">{v['chat_a']}</div>
  <div class="handover"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="7" r="3.2" fill="currentColor"/><path d="M3.5 17c.8-3.2 3.4-5 6.5-5s5.7 1.8 6.5 5" fill="currentColor"/></svg>{v['chat_handover']}</div>
</div>"""
    if key == "auto":
        rows = "".join(f"<li><span>{k}</span><b>{val}</b>{CHECK}</li>" for k, val in v["auto_fields"])
        return f"""<div class="vz vz-auto">
  <div class="mail"><p class="mail-from">{v['auto_from']}</p><p>{v['auto_mail']}</p></div>
  <svg class="flow" viewBox="0 0 60 24" aria-hidden="true"><path d="M2 12h50m-8-8 8 8-8 8" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div class="fields"><ul>{rows}</ul><p class="done">{CHECK}{v['auto_done']}</p></div>
</div>"""
    if key == "web":
        return f"""<div class="vz vz-web">
  <div class="browser"><div class="bar"><i></i><i></i><i></i><span></span></div><img src="{up}img/web.webp" alt="" width="900" height="563" loading="lazy"></div>
  <div class="phone"><img src="{up}img/web.webp" alt="" width="900" height="563" loading="lazy"></div>
</div>"""
    if key == "pm":
        c1, c2, c3 = v["pm_cards"]
        def card(c, cls=""):
            tag = f'<em class="p {c[1].lower()}">{c[1]}</em>' if c[1] else CHECK
            return f'<div class="card {cls}">{tag}<span>{c[0]}</span></div>'
        cols = v["pm_cols"]
        return f"""<div class="vz vz-pm">
  <div class="col"><h4>{cols[0]}</h4>{card(c2)}<div class="card ghost"></div></div>
  <div class="col"><h4>{cols[1]}</h4>{card(c1, 'hot')}</div>
  <div class="col"><h4>{cols[2]}</h4>{card(c3, 'done')}<div class="card ghost"></div></div>
</div>"""
    if key == "dash":
        vals = [38, 44, 41, 52, 58, 55, 66, 72, 69, 80, 86, 94]
        bars = "".join(f'<rect x="{i*25+4}" y="{100-h}" width="17" height="{h}" rx="3"/>' for i, h in enumerate(vals))
        kpis = "".join(f"<div><b>{n}</b><span>{l}</span></div>" for l, n in v["dash_kpis"])
        return f"""<div class="vz vz-dash">
  <div class="kpis">{kpis}</div>
  <p class="dash-t">{v['dash_title']}</p>
  <svg class="bars" viewBox="0 0 300 100" preserveAspectRatio="none" aria-hidden="true">{bars}</svg>
</div>"""
    if key == "learn":
        mods = "".join(
            f'<li><span>{n}</span><div class="track"><i style="width:{p}%"></i></div>{CHECK if p == 100 else f"<em>{p}%</em>"}</li>'
            for n, p in v["learn_mods"])
        return f"""<div class="vz vz-learn">
  <ul class="mods">{mods}</ul>
  <div class="award"><svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="20" r="15" fill="currentColor"/><path d="M15 32l-4 12 7-3 4 6 2-14m9-1 4 12-7-3-4 6-2-14" fill="currentColor" opacity=".55"/><path d="M24 11l2.8 5.7 6.2.9-4.5 4.4 1 6.2L24 25.3l-5.5 2.9 1-6.2-4.5-4.4 6.2-.9z" fill="#fff"/></svg><div><b>{v['learn_badge']}</b><span>{v['learn_cert']} PDF</span></div></div>
</div>"""


def page(lang):
    t = T[lang]
    v = t["viz"]
    up = "" if lang == "en" else "../"
    mail = f"mailto:{EMAIL}?subject={quote(t['mail_subject'])}"
    wa = f"https://wa.me/{WA}?text={quote(t['wa_hello'])}"
    book = BOOKING or f"https://wa.me/{WA}?text={quote(t['wa_book'])}"

    def lang_href(l):
        return up + PATHS[l] if PATHS[l] else (up or "./")

    alternates = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{PATHS[l]}">' for l in T)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'
    nav = "\n      ".join(f'<a href="#{i}">{label}</a>' for i, label in t["nav"])
    switch = "".join(
        f'<a href="{lang_href(l)}" data-lang="{l}" hreflang="{l}" lang="{l}"'
        + (' aria-current="true"' if l == lang else "") + f' title="{T[l]["lang_name"]}">{SHORT[l]}</a>'
        for l in T)
    dlg_buttons = "\n".join(
        f'<a class="dlg-lang" href="{lang_href(l)}" data-lang="{l}" lang="{l}" hreflang="{l}">'
        f'<span class="dlg-code">{SHORT[l]}</span><span>{T[l]["lang_name"]}</span></a>' for l in T)
    dlg_others = "".join(f'<p lang="{l}">{T[l]["dlg_title"]}</p>' for l in T if l != lang)

    tabs = "\n".join(
        f'<button role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}"'
        f'{"" if i == 0 else NOTAB}>{name}</button>'
        for i, (k, (name, _)) in enumerate(zip(SERVICE_KEYS, t["services"])))
    panels = "\n".join(
        f"""<div class="panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>
  <p class="panel-line"><b>{name}.</b> {line}</p>
  {viz(k, v, up)}
  <p class="panel-cap">{v['example'] if k == 'dash' else v['illustration']}</p>
</div>""" for i, (k, (name, line)) in enumerate(zip(SERVICE_KEYS, t["services"])))

    def links(key):
        return " ".join(
            f'<a href="{url}" target="_blank" rel="noopener">{t["link_live"] if kind == "live" else t["link_page"]}</a>'
            for kind, url in WORK_LINKS[key])

    work = "\n".join(
        f"""<article class="case{' big' if i < 2 else ''}">
  <a class="shot" href="{WORK_LINKS[k][0][1]}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><img src="{up}img/{k}.webp" alt="" loading="lazy"></a>
  <p class="kind">{t['work'][k][0]}</p>
  <h3>{t['work'][k][1]}</h3>
  <p class="result">{t['work'][k][2]}</p>
  <p class="case-links">{links(k)}</p>
</article>""" for i, k in enumerate(WORK))

    process = "\n".join(f"<li><b>{h}</b><span>{p}</span></li>" for h, p in t["process"])
    tools = "\n".join(
        f"""<div class="tg"><h3>{g}</h3><ul>{''.join(
            f'<li>{icon(ic) if ic else f"<span class=letter aria-hidden=true>{name[0]}</span>"}{name}</li>' for name, ic in items)}</ul></div>"""
        for g, items in zip(t["tools_groups"], TOOLS))
    facts = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["facts"])
    faq = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])

    return f"""<!doctype html>
<html lang="{lang}">
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
<meta property="og:image" content="{BASE}img/amrina.webp">
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
    <a class="brand" href="#main"><svg class="mark" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect x="1" y="1" width="46" height="46" rx="13" fill="#2546d8"/><path d="M8.5 36.5L16.5 11.5 24 31 31.5 11.5 39.5 36.5" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12.6 28h7.4" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/></svg><span>Amrina<small>{t['role']}</small></span></a>
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
      <div class="hero-links" role="group" aria-label="{t['hero_links']}">
        <a class="pill-link" href="{PORTFOLIO}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7.5" height="7.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2" fill="currentColor"/></svg>{t['footer_portfolio']}</a>
        <a class="pill-link" href="{LINKEDIN}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="4" fill="currentColor"/><path d="M7 10v7M7 7v.01M11 17v-7m0 3.2c0-1.9 1.2-3.2 2.9-3.2 1.6 0 2.6 1.1 2.6 3.1V17" fill="none" stroke="var(--paper)" stroke-width="2.2" stroke-linecap="round"/></svg>LinkedIn</a>
      </div>
      <p class="lets">{t['lets_talk']}</p>
      <p class="actions"><a class="btn" href="{book}" target="_blank" rel="noopener">{t['cta_primary']}</a> <a class="btn btn-line" href="{wa}" target="_blank" rel="noopener">{t['cta_wa']}</a></p>
      <p class="me"><img src="{up}img/amrina.webp" alt="Amrina" width="44" height="44">{t['hero_me']}</p>
    </div>
    <figure class="chat" aria-label="{t['chat_label']}">
      <figcaption>{t['chat_label']}</figcaption>
      <div class="msg msg-guest">{t['chat_guest']}</div>
      <div class="typing" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="msg msg-ai">{t['chat_answer']}</div>
      <div class="source" id="src1"><span class="source-n">1</span><div><span class="source-t">{t['chat_source_title']}</span>{t['chat_source']}</div></div>
    </figure>
  </div>
</section>

<section id="services" class="block">
  <div class="wrap">
    <h2>{t['services_h']}</h2>
    <div class="bench">
      <div class="tabs" role="tablist" aria-label="{t['services_h']}">
{tabs}
      </div>
      <div class="stage">
{panels}
      </div>
    </div>
  </div>
</section>

<section id="work" class="block block-tint">
  <div class="wrap">
    <div class="head-row"><h2>{t['work_h']}</h2><a href="{PORTFOLIO}" target="_blank" rel="noopener">{t['work_more']}</a></div>
    <div class="cases">
{work}
    </div>
  </div>
</section>

<section id="process" class="block">
  <div class="wrap">
    <h2>{t['process_h']}</h2>
    <ol class="steps">
{process}
    </ol>
  </div>
</section>

<section id="tools" class="block block-tint">
  <div class="wrap">
    <h2>{t['tools_h']}</h2>
    <div class="tools">
{tools}
    </div>
  </div>
</section>

<section id="about" class="block">
  <div class="wrap about">
    <img class="portrait" src="{up}img/amrina.webp" alt="Amrina" width="360" height="360" loading="lazy">
    <div>
      <h2>{t['about_h']}</h2>
      <p>{t['about']}</p>
      <dl class="facts">{facts}</dl>
      <p class="about-links"><a href="{PORTFOLIO}" target="_blank" rel="noopener">{t['footer_portfolio']}</a> <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></p>
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
  <div class="wrap contact-in">
    <div>
      <h2>{t['contact_h']}</h2>
      <p>{t['contact_p']}</p>
      <div class="options">
        <a class="opt opt-main" href="{book}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="6" width="13" height="12" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 10.5l6-3.5v10l-6-3.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><b>{t['opt_call'][0]}</b><span>{t['opt_call'][1]}</span></a>
        <a class="opt" href="{wa}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.1.1.7-.1 1.3Z" fill="currentColor"/></svg><b>{t['opt_wa'][0]}</b><span>{t['opt_wa'][1]}</span></a>
        <a class="opt" href="{mail}"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3.5 7l8.5 6 8.5-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><b>{t['opt_mail'][0]}</b><span>{t['opt_mail'][1]}</span></a>
      </div>
      <p class="contact-direct"><a href="{mail}">{EMAIL}</a></p>
    </div>
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
