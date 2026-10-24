# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

Page locale de préférences par cartes pour travailler les accroches, titres et idées. Elle permet d'aimer, de ne pas aimer, de passer, de signaler une accroche invalide, d'annuler, de reprendre sa progression, de consulter les statistiques et d'exporter en JSON ou CSV. Le serveur utilise la bibliothèque standard de Python et du HTML/CSS/JavaScript sans dépendances frontend.

## Prérequis

Python 3.10+; HTML/CSS/JavaScript

## Configuration et points d’entrée

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## Installation et utilisation

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## Périmètre et limites

Après démarrage, ouvrez http://127.0.0.1:8769. Les choix sont enregistrés dans runtime/ ; --port change le port et --state choisit un autre fichier d'état. Le serveur n'écoute qu'en bouclage et n'inclut pas d'authentification publique multiutilisateur. data/hooks.json contient 20 exemples synthétiques originaux, sans contenus de créateurs ni mesures d'engagement réelles. Gardez les ID uniques ; seules les cartes review.status=approved entrent dans la file. Utilisez un nouvel état pour un nouveau lot. Les statistiques décrivent vos choix, pas les performances auprès du public.

## Historique de validation

2026-10-24 · Python / HTTP: 14 ✓

## Licence et attribution

[MIT](LICENSE)

Il s’agit de versions de la documentation. Interfaces, sorties CLI et exécutables conservent le comportement de l’implémentation actuelle.

[Référence complète en chinois](README.zh-CN.md) · [Politique de maintenance des langues](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — Signalez les problèmes reproductibles avec des données synthétiques. Retirez identifiants secrets et informations privées des journaux.
