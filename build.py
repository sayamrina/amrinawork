"""Builds index.html (English), de/index.html and id/index.html from content.py."""
import re
import json
import hashlib
from pathlib import Path
from urllib.parse import quote
from viz import viz, tab_icon, CHECK
from content_extra import X, KB_WORDS
import legal
from content import T, EMAIL, WA, BOOKING, PORTFOLIO, LINKEDIN, GITHUB, WORK, WORK_META, WORK_LINKS, TOOLS, SERVICE_KEYS

BASE = "https://sayamrina.github.io/amrinawork/"
ROOT = Path(__file__).parent
PATHS = {"en": "", "de": "de/", "id": "id/"}
SHORT = {"en": "EN", "de": "DE", "id": "ID"}
NOTAB = ' tabindex="-1"'


def icon(name, size=22):
    svg = (ROOT / "icons" / f"{name}.svg").read_text()
    svg = re.sub(r"<title>.*?</title>", "", svg)
    return svg.replace('role="img"', f'aria-hidden="true" fill="currentColor" width="{size}" height="{size}"')


VER = hashlib.md5((ROOT / "style.css").read_bytes() + (ROOT / "main.js").read_bytes()).hexdigest()[:8]


def page(lang):
    t = dict(T[lang], **X[lang])
    v = t["viz"]
    up = "" if lang == "en" else "../"
    mail = f"mailto:{EMAIL}?subject={quote(t['mail_subject'])}"
    wa = f"https://wa.me/{WA}?text={quote(t['wa_hello'])}"
    book = BOOKING or f"https://wa.me/{WA}?text={quote(t['wa_book'])}"

    def lang_href(l):
        return up + PATHS[l] if PATHS[l] else (up or "./")

    alternates = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{PATHS[l]}">' for l in T)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'
    navitems = list(t["nav"])
    navitems.insert(2, ("offers", t["nav_offers"]))
    nav = "\n      ".join(f'<a href="#{i}">{label}</a>' for i, label in navitems)
    switch = "".join(
        f'<a href="{lang_href(l)}" data-lang="{l}" hreflang="{l}" lang="{l}"'
        + (' aria-current="true"' if l == lang else "") + f' title="{T[l]["lang_name"]}">{SHORT[l]}</a>'
        for l in T)
    dlg_buttons = "\n".join(
        f'<a class="dlg-lang" href="{lang_href(l)}" data-lang="{l}" lang="{l}" hreflang="{l}">'
        f'<span class="dlg-code">{SHORT[l]}</span><span>{T[l]["lang_name"]}</span></a>' for l in T)
    dlg_others = "".join(f'<p lang="{l}">{T[l]["dlg_title"]}</p>' for l in T if l != lang)

    tabs = "\n".join(
        f'<button type="button" role="tab" id="tab-{k}" data-panel="panel-{k}" aria-selected="{"true" if i == 0 else "false"}"'
        f'{"" if i == 0 else NOTAB}>{tab_icon(k)}<span>{name}</span><i class="prog" aria-hidden="true"></i></button>'
        for i, (k, (name, _)) in enumerate(zip(SERVICE_KEYS, t["services"])))
    panels = "\n".join(
        f"""<div class="panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{" tabindex=\"0\"" if i == 0 else " hidden"}>
  <p class="panel-line"><b>{name}.</b> {line}</p>
  {viz(k, v, up)}
  <p class="panel-cap">{v['example'] if k == 'dash' else v['illustration']}</p>
</div>""" for i, (k, (name, line)) in enumerate(zip(SERVICE_KEYS, t["services"])))

    def links(key):
        return " ".join(
            f'<a href="{url}" target="_blank" rel="noopener">{t["link_live"] if kind == "live" else t["link_page"]}</a>'
            for kind, url in WORK_LINKS[key])

    def stack(k):
        return "".join(f'<span title="{n}">{icon(ic, 18)}<span class="sr">{n}</span></span>' for n, ic in WORK_META[k][1])

    def case(i, k):
        kind, title, result = t["work"][k]
        big, label = t["work_metrics"][k]
        live = WORK_LINKS[k][0][1]
        page = next((u for kd, u in WORK_LINKS[k] if kd == "page"), None)
        details = f'<a class="details" href="{page}" target="_blank" rel="noopener">{t["link_page"]}</a>' if page else ""
        return f"""<article class="case{' big' if i < 2 else ''}" data-cats="{' '.join(WORK_META[k][0])}">
  <a class="shot" href="{live}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
    <span class="shot-bar"><i></i><i></i><i></i></span>
    <img src="{up}img/{k}.webp" alt="" loading="lazy">
    <span class="shot-cta">{t['work_try']}</span>
  </a>
  <div class="case-body">
    <p class="kind">{kind}</p>
    <h3>{title}</h3>
    <p class="metric"><b>{big}</b><span>{label}</span></p>
    <div class="case-foot"><span class="stack">{stack(k)}</span><span class="case-links"><a class="try" href="{live}" target="_blank" rel="noopener">{t['work_try']}</a>{details}</span></div>
  </div>
</article>"""

    work = "\n".join(case(i, k) for i, k in enumerate(WORK))
    names = dict(zip(SERVICE_KEYS, (n for n, _ in t["services"])))
    used = [k for k in SERVICE_KEYS if any(k in WORK_META[w][0] for w in WORK)]
    filters = f'<button type="button" aria-pressed="true" data-cat="all">{t["work_all"]}</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-cat="{k}">{names[k]}</button>' for k in used)


    # --- adoption section
    adopt_steps = "".join(f"<li><b>{h}</b><span>{p}</span></li>" for h, p in t["adopt_steps"])
    wo, wi = t["adopt_curve"]
    adopt_svg = f"""<svg class="curve" viewBox="0 0 400 240" width="400" height="240" role="img" aria-label="{wi} / {wo}">
  <defs><linearGradient id="cg-{lang}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".22"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>
  <path class="grid" d="M20 210H390M20 150H390M20 90H390M20 30H390"/>
  <path class="with-fill" d="M20 205 C 90 200, 120 150, 170 120 S 280 50, 390 38 V210 H20Z" fill="url(#cg-{lang})"/>
  <path class="without" d="M20 205 C 90 200, 120 150, 170 128 S 260 150, 390 168"/>
  <path class="with" d="M20 205 C 90 200, 120 150, 170 120 S 280 50, 390 38"/>
  <g class="marks"><circle cx="70" cy="200" r="7"/><circle cx="170" cy="120" r="7"/><circle cx="300" cy="58" r="7"/></g>
  <text x="388" y="190" text-anchor="end" class="lbl-without">{wo}</text><text x="388" y="22" text-anchor="end" class="lbl-with">{wi}</text>
</svg>"""

    # --- savings calculator
    cur = t["currency"]

    # --- offers
    def offer_href(key, wa_text):
        return book if key == "pilot" else f"https://wa.me/{WA}?text={quote(wa_text)}"
    offers = "".join(
        f"""<article class="offer offer-{key}"><p class="tag">{tag}</p><h3>{title}</h3><p>{desc}</p><a class="btn{' btn-line' if key != 'pilot' else ''}" href="{offer_href(key, wa_text)}" target="_blank" rel="noopener">{cta}</a></article>"""
        for key, tag, title, desc, cta, wa_text in t["offers"])

    # --- knowledge base for the on-page assistant
    kb = [dict(id="greet", q="", a=t["asst_hello"], src="", href="")]
    for k, (name, line) in zip(SERVICE_KEYS, t["services"]):
        kb.append(dict(id=f"svc-{k}", q=name, a=f"{name}: {line}", src=t["services_h"], href="#services"))
    for key, tag, title, desc, cta, wa_text in t["offers"]:
        kb.append(dict(id=f"offer-{key}", q=title, a=f"{title} ({tag}): {desc}", src=t["offers_h"], href="#offers"))
    for i, (q, a) in enumerate(t["faq"]):
        kb.append(dict(id=f"faq-{i}", q=q, a=a, src=f"{t['faq_h']}: {q}", href="#faq"))
    kb.append(dict(id="process", q=t["process_h"], a=" ".join(f"{i}. {h}: {p}." for i, (h, p) in enumerate(t["process"], 1)), src=t["process_h"], href="#process"))
    kb.append(dict(id="adopt", q=t["adopt_h"], a=t["adopt_p"] + " " + " ".join(f"{h}: {p}." for h, p in t["adopt_steps"]), src=t["adopt_h"], href="#adopt"))
    kb.append(dict(id="about", q=t["about_h"], a=t["about"], src=t["about_h"], href="#about"))
    kb.append(dict(id="lang", q=t["facts"][2][0], a=f"{t['facts'][2][0]}: {t['facts'][2][1]}.", src=t["about_h"], href="#about"))
    kb.append(dict(id="location", q="", a=t["hero_me"], src=t["about_h"], href="#about"))
    kb.append(dict(id="contact", q=t["contact_h"], a=f"{t['opt_call'][0]}, {t['opt_wa'][0]}, {t['opt_mail'][0]}. {t['contact_p']}", src=t["contact_h"], href="#contact"))
    kb.append(dict(id="calc", q=t["calc_h"], a=f"{t['calc_h']} {t['calc_p']} {t['calc_note']}", src=t["calc_h"], href="#savings"))
    for e in kb:
        e["k"] = KB_WORDS.get(e["id"], "")
    ldjson = json.dumps({
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Amrina, AI engineer",
        "url": BASE + PATHS[lang], "image": BASE + "img/amrina.webp", "description": t["description"],
        "email": EMAIL, "telephone": "+4915129529331", "inLanguage": lang,
        "address": {"@type": "PostalAddress", "addressLocality": "Saarbrücken", "addressCountry": "DE"},
        "areaServed": ["DE", "ID", "Worldwide"],
        "founder": {"@type": "Person", "name": "Amrina", "jobTitle": "AI engineer and educational technology specialist",
                    "alumniOf": "Saarland University", "sameAs": [PORTFOLIO, LINKEDIN, GITHUB]},
        "knowsLanguage": ["en", "de", "id"],
    }, ensure_ascii=False).replace("</", "<\\/")
    kb_json = json.dumps(kb, ensure_ascii=False).replace("</", "<\\/")
    asst_cfg = json.dumps(dict(none=t["asst_none"], src=t["asst_src"], wa=t["asst_wa"], book=t["asst_book"],
                               waHref=f"https://wa.me/{WA}?text=", waText=t["asst_wa_text"], bookHref=book), ensure_ascii=False).replace("</", "<\\/")
    mark_small = open(ROOT / 'logo' / 'mark.svg').read().strip().replace('<svg ', '<svg width="30" height="30" ', 1)
    chips = "".join(f'<button type="button" class="chip">{c}</button>' for c in t["asst_chips"])

    offer_tiles = "".join(
        f'<a class="tile" href="#services" data-tab="{k}">{tab_icon(k)}<span>{name}</span></a>'
        for k, (name, _) in zip(SERVICE_KEYS, t["services"]))
    # sentinel for the scroll-aware assistant launcher (fallback when scroll-state queries are unsupported)
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
<script type="application/ld+json">{ldjson}</script>
<link rel="stylesheet" href="{up}fonts.css?v={VER}">
<link rel="stylesheet" href="{up}style.css?v={VER}">
</head>
<body data-lang="{lang}">
<div class="scroll-sentinel" aria-hidden="true"></div>
<a class="skip" href="#main">{t['skip']}</a>

<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="#main"><svg class="mark" aria-hidden="true" width="38" height="38" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect x="1" y="1" width="46" height="46" rx="13" fill="#2546d8"/><path d="M8.5 36.5L16.5 11.5 24 31 31.5 11.5 39.5 36.5" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12.6 28h7.4" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/></svg><span>Amrina<small>{t['role']}</small></span></a>
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
      <p class="hi"><img src="{up}img/amrina.webp" alt="" width="40" height="40">{t['hero_hi']}</p>
      <h1>{t['hero_h1']}</h1>
      <p class="help-with" id="help-with">{t['help_with']}</p>
      <nav class="offer-tiles" aria-labelledby="help-with">{offer_tiles}</nav>
      <p class="lede">{t['hero_lede']}</p>
      <div class="hero-links" role="group" aria-label="{t['hero_links']}">
        <a class="pill-link" href="{PORTFOLIO}" target="_blank" rel="noopener"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7.5" height="7.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2" fill="currentColor"/></svg>{t['footer_portfolio']}</a>
        <a class="pill-link" href="{LINKEDIN}" target="_blank" rel="noopener"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="4" fill="currentColor"/><path d="M7 10v7M7 7v.01M11 17v-7m0 3.2c0-1.9 1.2-3.2 2.9-3.2 1.6 0 2.6 1.1 2.6 3.1V17" fill="none" stroke="var(--paper)" stroke-width="2.2" stroke-linecap="round"/></svg>LinkedIn</a>
      </div>
      <p class="lets">{t['lets_talk']}</p>
      <p class="actions"><a class="btn" href="{book}" target="_blank" rel="noopener">{t['cta_primary']}</a> <a class="btn btn-line" href="{wa}" target="_blank" rel="noopener">{t['cta_wa']}</a></p>
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
      <div class="tabs-col">
        <div class="tabs" role="tablist" aria-label="{t['services_h']}">
{tabs}
        </div>
        <button type="button" class="autoplay-btn" data-pause="{t['pause']}" data-play="{t['play']}">{t['pause']}</button>
      </div>
      <div class="stage">
{panels}
      </div>
    </div>
  </div>
</section>

<section id="adopt" class="block block-tint">
  <div class="wrap adopt">
    <div>
      <h2>{t['adopt_h']}</h2>
      <p class="adopt-p">{t['adopt_p']}</p>
      <ol class="adopt-steps">{adopt_steps}</ol>
    </div>
    <figure class="curve-card">{adopt_svg}<figcaption>{t['viz']['illustration']}</figcaption></figure>
  </div>
</section>

<section id="work" class="block block-dark">
  <div class="wrap">
    <div class="head-row"><h2>{t['work_h']}</h2><a href="{PORTFOLIO}" target="_blank" rel="noopener">{t['work_more']}</a></div>
    <div class="filters" role="group" aria-label="{t['work_h']}">{filters}</div>
    <div class="cases">
{work}
    </div>
  </div>
</section>

<section id="savings" class="block">
  <div class="wrap calc">
    <div class="calc-in">
      <h2>{t['calc_h']}</h2>
      <p class="calc-p">{t['calc_p']}</p>
      <div class="field"><label for="c-q">{t['calc_q']}</label><output id="o-q" for="c-q">20</output><input id="c-q" type="range" min="5" max="200" step="5" value="20"></div>
      <div class="field"><label for="c-m">{t['calc_min']}</label><output id="o-m" for="c-m">4</output><input id="c-m" type="range" min="1" max="30" step="1" value="4"></div>
      <div class="field"><label for="c-s">{t['calc_share']}</label><output id="o-s" for="c-s">50%</output><input id="c-s" type="range" min="10" max="90" step="5" value="50"></div>
      <div class="field"><label for="c-c">{t['calc_cost']}</label><output id="o-c" for="c-c">{cur} {t['cost_default']}</output><input id="c-c" type="range" min="{t['cost_min']}" max="{t['cost_max']}" step="{t['cost_step']}" value="{t['cost_default']}" data-cur="{cur}"></div>
    </div>
    <div class="calc-out" aria-live="polite">
      <p class="big"><b id="r-h">0</b><span>{t['calc_hours']}</span></p>
      <p class="big money"><b id="r-v">0</b><span>{t['calc_money']}</span></p>
      <div class="hourbar" aria-hidden="true"><i id="r-bar"></i></div>
      <p class="calc-note">{t['calc_note']}</p>
      <a class="btn btn-invert" href="{book}" target="_blank" rel="noopener">{t['calc_cta']}</a>
    </div>
  </div>
</section>

<section id="offers" class="block block-tint">
  <div class="wrap">
    <h2>{t['offers_h']}</h2>
    <div class="offers">{offers}</div>
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
        <a class="opt opt-main" href="{book}" target="_blank" rel="noopener"><svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="6" width="13" height="12" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 10.5l6-3.5v10l-6-3.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><b>{t['opt_call'][0]}</b><span>{t['opt_call'][1]}</span></a>
        <a class="opt" href="{wa}" target="_blank" rel="noopener"><svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.1.1.7-.1 1.3Z" fill="currentColor"/></svg><b>{t['opt_wa'][0]}</b><span>{t['opt_wa'][1]}</span></a>
        <a class="opt" href="{mail}"><svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3.5 7l8.5 6 8.5-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><b>{t['opt_mail'][0]}</b><span>{t['opt_mail'][1]}</span></a>
      </div>
      <p class="contact-direct"><a href="{mail}">{EMAIL}</a></p>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap foot-in">
    <p>© 2026 {t['footer']}</p>
    <p><a href="{up}impressum.html">{t['legal_imp']}</a> <a href="{up}datenschutz.html">{t['legal_priv']}</a> <a href="{PORTFOLIO}" target="_blank" rel="noopener">{t['footer_portfolio']}</a> <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></p>
  </div>
</footer>

<button class="asst-btn" type="button" popovertarget="asst"><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-5 4v-4H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M8 10h8M8 13h5"/></svg><span>{t['asst_btn']}</span></button>
<dialog id="asst" class="asst" popover aria-labelledby="asst-title">
  <header class="asst-head"><span class="asst-av" aria-hidden="true">{mark_small}</span><div><h2 id="asst-title">{t['asst_title']}</h2><p>{t['asst_note']}</p></div><button type="button" class="asst-x" popovertarget="asst" popovertargetaction="hide" aria-label="{t['asst_close']}">×</button></header>
  <div class="asst-log" aria-live="polite"><div class="m m-ai">{t['asst_hello']}</div></div>
  <div class="asst-chips">{chips}</div>
  <form class="asst-form"><label class="sr" for="asst-in">{t['asst_ph']}</label><input id="asst-in" type="text" autocomplete="off" placeholder="{t['asst_ph']}" maxlength="200"><button type="submit">{t['asst_send']}</button></form>
</dialog>
<script type="application/json" id="kb">{kb_json}</script>
<script type="application/json" id="asst-cfg">{asst_cfg}</script>

<dialog id="lang-dialog" class="dlg" closedby="none" aria-labelledby="dlg-title">
  <h2 id="dlg-title">{t['dlg_title']}</h2>
  <div class="dlg-others">{dlg_others}</div>
  <div class="dlg-langs">
{dlg_buttons}
  </div>
  <p class="dlg-note">{t['dlg_note']}</p>
</dialog>

<script src="{up}main.js?v={VER}"></script>
</body>
</html>
"""


for lang in T:
    out = ROOT / PATHS[lang] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page(lang), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))

mark = (ROOT / "logo" / "mark.svg").read_text().strip().replace("<svg ", '<svg class="mark" aria-hidden="true" width="38" height="38" ', 1)
for fname, title, body in [("impressum.html", "Impressum", legal.impressum(EMAIL)), ("datenschutz.html", "Datenschutzerklärung", legal.datenschutz(EMAIL))]:
    (ROOT / fname).write_text(legal.page(title, body, "./").replace("{MARK}", mark), encoding="utf-8")
    print("wrote", fname)
