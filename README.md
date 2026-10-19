# nagroup.biz – Website der NA Group

Statische Website (HTML/CSS) in vier Sprachen (DE, EN, ES, 中文) plus PHP-Kontaktformular.
Kein WordPress, keine Datenbank, keine Cookies, kein Tracking.

## Aufbau

```
src/content.py      Alle Texte und Daten (hier ändern)
build.py            Erzeugt die HTML-Seiten in public/
public/             Fertige Website – genau das landet auf dem Server
  de/ en/ es/ zh/   Sprachversionen (index.html + Impressum/Datenschutz für de/en)
  assets/           CSS, JS, Schriften (lokal, DSGVO-freundlich), Favicon
  kontakt.php       Kontaktformular (Empfänger oben in der Datei)
  .htaccess         HTTPS, Sprachweiche, Sicherheits-Header
.cpanel.yml         Deployment-Anweisung für cPanel „Git Version Control“
```

## Text ändern

1. `src/content.py` bearbeiten
2. `python3 build.py`
3. Commit + Push auf GitHub
4. cPanel → Git Version Control → Repository → „Manage“ → Pull or Deploy → **Update from Remote**, dann **Deploy HEAD Commit**

## Server-Voraussetzungen (cPanel)

- PHP **8.x** für die Domain (MultiPHP Manager) – mit PHP 5.6 läuft `kontakt.php` nicht.
- Postfach `noreply@nagroup.biz` existiert (Absender des Formulars).
- E-Mail Routing für nagroup.biz = **Remote Mail Exchanger** (Mails liegen bei Microsoft 365),
  sonst landen Formular-Mails im lokalen cPanel-Postfach statt bei Outlook.

## Livegang

1. In `.cpanel.yml` `DEPLOYPATH` auf `/home/nagroup/public_html/` setzen.
2. Vorher altes WordPress aus `public_html` sichern und entfernen.
3. Platzhalter in Impressum/Datenschutz `[...]` ausfüllen.

## Bilder (wichtig)

Die Bilder in `public/assets/img/` (Logos, Fotos, Titelbilder) stammen von der alten Website und liegen
**nur auf dem Server**, nicht in GitHub:

- `/home/nagroup/repositories/nagroup-website/public/assets/img/` (wird bei jedem Deploy mitkopiert)
- `/home/nagroup/neu.nagroup.biz/assets/img/`

Empfehlung: den Ordner einmal im cPanel-Dateimanager als ZIP herunterladen und per GitHub
„Add file → Upload files“ nach `public/assets/img/` hochladen – dann ist alles versioniert.
