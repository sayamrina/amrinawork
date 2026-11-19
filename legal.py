"""Impressum and Datenschutzerklärung (German, as required in Germany), with a short EN/ID note."""

NAME = "Amrina"
STREET = "Metzer Str. 46"
CITY = "66117 Saarbrücken"
COUNTRY = "Deutschland"
PHONE = "+49 151 29529331"
UPDATED = "November 2026"

NOTE = """<p class="legal-note" lang="en">English: this page is in German, as German law requires. In short: this website sets no cookies, uses no tracking or analytics and loads nothing from third parties.</p>
<p class="legal-note" lang="id">Indonesia: halaman ini berbahasa Jerman sesuai hukum Jerman. Singkatnya: website ini tidak memakai cookie, tidak melacak pengunjung, dan tidak memuat apa pun dari pihak ketiga.</p>"""


def impressum(email):
    return f"""<h1>Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>{NAME}<br>{STREET}<br>{CITY}<br>{COUNTRY}</p>
<h2>Kontakt</h2>
<p>Telefon: <a href="tel:{PHONE.replace(' ', '')}">{PHONE}</a><br>E-Mail: <a href="mailto:{email}">{email}</a></p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>{NAME}, Anschrift wie oben</p>
<h2>Verbraucherstreitbeilegung</h2>
<p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Haftung für Inhalte und Links</h2>
<p>Die Inhalte dieser Website wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität kann ich jedoch keine Gewähr übernehmen. Diese Website enthält Links zu externen Websites, auf deren Inhalte ich keinen Einfluss habe; für diese Inhalte ist der jeweilige Anbieter verantwortlich. Werden mir Rechtsverletzungen bekannt, entferne ich die betreffenden Links umgehend.</p>
<h2>Hinweis zu den Projekten</h2>
<p>Die auf dieser Website gezeigten Projekte sind eigene Projekte, Demos oder Projekte aus meiner Masterarbeit und keine Kundenaufträge, sofern nicht ausdrücklich anders angegeben.</p>"""


def datenschutz(email):
    return f"""<h1>Datenschutzerklärung</h1>
<p class="legal-meta">Stand: {UPDATED}</p>

<h2>1. Verantwortlicher</h2>
<p>{NAME}<br>{STREET}<br>{CITY}<br>{COUNTRY}<br>E-Mail: <a href="mailto:{email}">{email}</a><br>Telefon: {PHONE}</p>

<h2>2. Überblick</h2>
<p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Tracking-Dienste und lädt beim Aufruf keine Inhalte von Drittanbietern. Schriftarten, Bilder und Skripte werden vom selben Server ausgeliefert wie die Seite selbst. Daten an andere Anbieter fließen erst, wenn Sie selbst einen Link zu einem solchen Anbieter anklicken (siehe Abschnitte 6 bis 9).</p>

<h2>3. Hosting über GitHub Pages</h2>
<p>Diese Website wird über GitHub Pages bereitgestellt, einen Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Website verarbeitet GitHub technisch notwendige Daten, insbesondere Ihre IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite sowie Angaben zu Browser und Betriebssystem (Server-Logfiles). Dies dient der Auslieferung und der Sicherheit der Website.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; mein berechtigtes Interesse liegt in einer zuverlässigen und sicheren Bereitstellung der Website. Dabei können Daten in die USA übermittelt werden. Die Übermittlung stützt sich auf das EU-US Data Privacy Framework beziehungsweise auf Standardvertragsklauseln der EU-Kommission. Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>

<h2>4. Speicherung im Browser</h2>
<p>Wenn Sie beim ersten Besuch eine Sprache wählen, wird diese Wahl im lokalen Speicher Ihres Browsers (localStorage, Schlüssel „amrinawork-lang“) abgelegt, damit die Abfrage nicht erneut erscheint. Diese Information verlässt Ihr Gerät nicht. Die Speicherung ist für den von Ihnen gewünschten Dienst unbedingt erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG). Sie können sie jederzeit über die Einstellungen Ihres Browsers löschen.</p>

<h2>5. Assistent auf dieser Seite</h2>
<p>Der Assistent („Meinen Assistenten fragen“) läuft vollständig in Ihrem Browser. Er sucht Antworten nur im Text dieser Seite. Ihre Eingaben werden weder gespeichert noch an einen Server oder einen KI-Dienst übertragen. Erst wenn Sie auf „Per WhatsApp fragen“ klicken, wird Ihre Frage als vorausgefüllter Text an WhatsApp übergeben (siehe Abschnitt 7).</p>

<h2>6. Kontakt per E-Mail</h2>
<p>Wenn Sie mir eine E-Mail schreiben, verarbeite ich Ihre Angaben (zum Beispiel Name, E-Mail-Adresse und Inhalt der Nachricht), um Ihre Anfrage zu beantworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, soweit Ihre Anfrage auf einen Vertrag zielt, im Übrigen Art. 6 Abs. 1 lit. f DSGVO. Für E-Mails nutze ich Gmail der Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. Ich lösche Ihre Daten, sobald sie nicht mehr erforderlich sind, soweit keine gesetzlichen Aufbewahrungspflichten bestehen.</p>

<h2>7. Kontakt über WhatsApp</h2>
<p>Die WhatsApp-Schaltflächen öffnen einen Chat in WhatsApp, einem Dienst der WhatsApp Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Irland. Für die Verarbeitung dort gelten die Datenschutzbestimmungen von WhatsApp. Die Nutzung ist freiwillig; Sie können mich jederzeit auch per E-Mail erreichen. Rechtsgrundlage für meine Verarbeitung Ihrer Nachricht ist Art. 6 Abs. 1 lit. b beziehungsweise lit. f DSGVO.</p>

<h2>8. Terminbuchung über Google Kalender</h2>
<p>Die Schaltfläche zur Buchung eines Videogesprächs öffnet eine Buchungsseite von Google Kalender (Google Ireland Limited, Anschrift wie oben). Die dort von Ihnen eingegebenen Daten (Name, E-Mail-Adresse, Nachricht) werden verarbeitet, um den Termin zu vereinbaren und einen Google-Meet-Link zu erstellen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO. Es gelten zusätzlich die Datenschutzbestimmungen von Google.</p>

<h2>9. Externe Links</h2>
<p>Diese Website verlinkt auf externe Seiten, etwa mein Portfolio, LinkedIn und Demos meiner Projekte bei verschiedenen Anbietern. Erst wenn Sie einen solchen Link anklicken, werden Daten an den jeweiligen Anbieter übertragen; dort gelten dessen Datenschutzbestimmungen.</p>

<h2>10. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO (Art. 21). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Wenden Sie sich dazu einfach an die oben genannte E-Mail-Adresse.</p>
<p>Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Zuständig ist das Unabhängige Datenschutzzentrum Saarland, Fritz-Dobisch-Straße 12, 66111 Saarbrücken.</p>"""


def page(title, body, back, up=""):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}, Amrina</title>
<meta name="robots" content="noindex, follow">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}fonts.css">
<link rel="stylesheet" href="{up}style.css">
</head>
<body class="legal-page">
<header class="top"><div class="wrap top-in"><a class="brand" href="{back}">{{MARK}}<span>Amrina<small>AI engineer</small></span></a><a class="legal-back" href="{back}">Zur Startseite</a></div></header>
<main class="wrap legal">
{NOTE}
{body}
</main>
<footer class="foot"><div class="wrap foot-in"><p>© 2026 Amrina, AI engineer, Saarbrücken</p><p><a href="impressum.html">Impressum</a> <a href="datenschutz.html">Datenschutz</a></p></div></footer>
</body>
</html>
"""
