# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

A local card-based preference page for writing openings, titles and creative exercises. Like, dislike, skip, mark an invalid opening, undo a choice, resume saved progress, inspect feature statistics, and export JSON or CSV. The Python standard-library server and plain HTML/CSS/JavaScript need no frontend dependency installation.

## Requirements

Python 3.10+; HTML/CSS/JavaScript

## Configuration and entry points

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## Installation and usage

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## Scope and limitations

Open http://127.0.0.1:8769 after starting the server. Choices are stored under runtime/; --port changes the port and --state selects a separate state file. The server binds to loopback and has no public multi-user authentication. data/hooks.json contains 20 original synthetic examples, not creators' source material or real engagement data. Keep IDs unique; only review.status=approved enters the queue. Use a new state file for a new card pool. Statistics describe your choices, not predicted audience performance.

## Validation record

2026-10-24 · Python / HTTP: 14 ✓

## License and attribution

[MIT](LICENSE)

These are documentation editions. Application interfaces, CLI output and executable releases retain the behavior of the current implementation.

[Complete Chinese reference](README.zh-CN.md) · [Language maintenance policy](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — Report a reproducible issue with synthetic data. Remove credentials and private information from logs.
