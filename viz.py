"""Animated mock-ups for the "What I build" tabs. Each one sits in a small app window."""
import re

CHECK = '<svg class="ck" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# Tab icons, 24x24 strokes
TAB_ICONS = {
    "chat": '<path d="M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-5 4v-4H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M8 10h8M8 13h5"/>',
    "auto": '<rect x="3" y="5" width="8" height="6" rx="1.5"/><rect x="13" y="13" width="8" height="6" rx="1.5"/><path d="M7 11v4a2 2 0 0 0 2 2h4M17 13V9a2 2 0 0 0-2-2h-4"/>',
    "web": '<rect x="2.5" y="4" width="19" height="14" rx="2"/><path d="M2.5 8h19M8 21h8"/>',
    "pm": '<rect x="3" y="4" width="5" height="16" rx="1.5"/><rect x="9.5" y="4" width="5" height="10" rx="1.5"/><rect x="16" y="4" width="5" height="13" rx="1.5"/>',
    "dash": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "learn": '<path d="M2 9l10-5 10 5-10 5-10-5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
}


def tab_icon(key):
    return (f'<svg class="tab-ic" width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" fill="none" '
            f'stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{TAB_ICONS[key]}</svg>')


def window(title, body, live):
    return f"""<div class="win">
  <div class="win-bar"><i></i><i></i><i></i><span class="win-title">{title}</span><span class="live">{live}</span></div>
  <div class="win-body">{body}</div>
</div>"""


def viz(key, v, up):
    if key == "chat":
        body = f"""<div class="vz-chat">
  <div class="b b-guest s1">{v['chat_q']}</div>
  <div class="dots s2" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="b b-ai s3">{v['chat_a']}</div>
  <div class="handover s4"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="7" r="3.2" fill="currentColor"/><path d="M3.5 17c.8-3.2 3.4-5 6.5-5s5.7 1.8 6.5 5" fill="currentColor"/></svg>{v['chat_handover']}</div>
  <div class="toast s5">{CHECK}{v['toast']}</div>
</div>"""
        return window(v["app_chat"], body, v["live"])

    if key == "auto":
        mail = re.sub(r"\{(\d)\}(.*?)\{/\1\}", r'<mark class="hl h\1">\2</mark>', v["auto_mail"])
        rows = "".join(
            f'<li class="f{i}"><span><i class="dot h{i}"></i>{k}</span><b>{val}</b>{CHECK}</li>'
            for i, (k, val) in enumerate(v["auto_fields"], 1))
        body = f"""<div class="vz-auto">
  <div class="mail"><p class="mail-from">{v['auto_from']}</p><p>{mail}</p><span class="scan" aria-hidden="true"></span></div>
  <svg class="flow" width="54" height="24" viewBox="0 0 60 24" aria-hidden="true"><path d="M2 12h50m-8-8 8 8-8 8" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div class="fields"><ul>{rows}</ul><p class="done">{CHECK}{v['auto_done']}</p></div>
</div>"""
        return window(v["app_auto"], body, v["live"])

    if key == "web":
        checks = "".join(f'<li class="c{i}">{CHECK}{c}</li>' for i, c in enumerate(v["web_checks"], 1))
        body = f"""<div class="vz-web">
  <div class="browser"><div class="bar"><i></i><i></i><i></i><span></span></div><div class="viewport"><img src="{up}img/web.webp" alt="" width="900" height="563" loading="lazy"></div></div>
  <div class="phone"><img src="{up}img/web.webp" alt="" width="900" height="563" loading="lazy"></div>
  <ul class="checks">{checks}</ul>
</div>"""
        return window(v["app_web"], body, v["live"])

    if key == "pm":
        c1, c2, c3 = v["pm_cards"]
        cols = v["pm_cols"]
        body = f"""<div class="vz-pm">
  <div class="col"><h4>{cols[0]}</h4>
    <div class="card new"><em class="p p1">P1</em><span>{c1[0]}</span><small class="assign">{v['pm_assign']}</small></div>
    <div class="card"><em class="p p2">P2</em><span>{c2[0]}</span></div>
  </div>
  <div class="col"><h4>{cols[1]}</h4><div class="card"><em class="p p3">P3</em><span>{v['pm_extra']}</span><div class="mini-track"><i></i></div></div></div>
  <div class="col"><h4>{cols[2]}</h4><div class="card done">{CHECK}<span>{c3[0]}</span></div></div>
  <p class="pm-note">{v['pm_new']}</p>
</div>"""
        return window(v["app_pm"], body, v["live"])

    if key == "dash":
        vals = [38, 44, 41, 52, 58, 55, 66, 72, 69, 80, 86, 94]
        bars = "".join(f'<rect class="r" style="--i:{i}" x="{i*25+4}" y="{100-h}" width="17" height="{h}" rx="3"/>' for i, h in enumerate(vals))
        pts = " ".join(f"{i*25+12.5},{100-h-8}" for i, h in enumerate(vals))
        kpis = "".join(
            f'<div><b class="count" data-to="{n}">{n}</b><span>{l}</span></div>' for l, n in v["dash_kpis"])
        body = f"""<div class="vz-dash">
  <div class="kpis">{kpis}</div>
  <p class="dash-t">{v['dash_title']}</p>
  <svg class="bars" width="300" height="140" viewBox="0 0 300 100" preserveAspectRatio="none" aria-hidden="true">{bars}<polyline class="trend" points="{pts}" fill="none" vector-effect="non-scaling-stroke"/></svg>
</div>"""
        return window(v["app_dash"], body, v["live"])

    if key == "learn":
        mods = "".join(
            f'<li style="--w:{p}%"><span>{n}</span><div class="track"><i></i></div>'
            + (CHECK if p == 100 else f'<em>{p}%</em>' if p else f'<em class="unlock">{v["learn_unlock"]}</em>')
            + "</li>"
            for n, p in v["learn_mods"])
        body = f"""<div class="vz-learn">
  <ul class="mods">{mods}</ul>
  <div class="award"><svg width="64" height="64" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="20" r="15" fill="currentColor"/><path d="M15 32l-4 12 7-3 4 6 2-14m9-1 4 12-7-3-4 6-2-14" fill="currentColor" opacity=".55"/><path d="M24 11l2.8 5.7 6.2.9-4.5 4.4 1 6.2L24 25.3l-5.5 2.9 1-6.2-4.5-4.4 6.2-.9z" fill="#fff"/></svg><div><b>{v['learn_badge']}</b><span>{v['learn_cert']} PDF</span></div></div>
</div>"""
        return window(v["app_learn"], body, v["live"])
