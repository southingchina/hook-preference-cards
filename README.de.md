# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

Lokale Kartenoberfläche für Vorlieben bei Texteinstiegen, Titeln und kreativen Übungen. Unterstützt Gefällt/Gefällt nicht, Überspringen, ungültige Einstiege, Rückgängig, gespeicherten Fortschritt, Merkmalsstatistiken sowie JSON-/CSV-Export. Der Server nutzt Pythons Standardbibliothek und normales HTML/CSS/JavaScript ohne Frontend-Abhängigkeiten.

## Voraussetzungen

Python 3.10+; HTML/CSS/JavaScript

## Konfiguration und Einstiegspunkte

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## Installation und Verwendung

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## Umfang und Einschränkungen

Nach dem Start http://127.0.0.1:8769 öffnen. Entscheidungen liegen unter runtime/; --port ändert den Port und --state die Zustandsdatei. Der Server bindet nur an Loopback und bietet keine öffentliche Mehrbenutzer-Anmeldung. data/hooks.json enthält 20 selbst erstellte synthetische Beispiele, keine fremden Originalinhalte oder echten Interaktionszahlen. IDs müssen eindeutig sein; nur review.status=approved kommt in die Auswahl. Bei neuem Kartensatz eine neue Zustandsdatei nutzen. Statistiken beschreiben persönliche Entscheidungen, keine vorhergesagte Publikumswirkung.

## Prüfstand

2026-10-24 · Python / HTTP: 14 ✓

## Lizenz und Herkunft

[MIT](LICENSE)

Dies sind Sprachfassungen der Dokumentation. Oberflächen, CLI-Ausgaben und ausführbare Pakete folgen weiterhin der aktuellen Implementierung.

[Vollständige chinesische Referenz](README.zh-CN.md) · [Pflege der Sprachfassungen](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — Reproduzierbare Probleme mit synthetischen Daten melden. Zugangsdaten und private Informationen aus Protokollen entfernen.
