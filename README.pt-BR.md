# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

Página local de preferências por cartões para praticar aberturas, títulos e ideias. Permite gostar, não gostar, pular, marcar uma abertura inválida, desfazer, retomar o progresso, consultar estatísticas e exportar JSON ou CSV. Usa um servidor com a biblioteca padrão do Python e HTML/CSS/JavaScript sem dependências de frontend.

## Requisitos

Python 3.10+; HTML/CSS/JavaScript

## Configuração e pontos de entrada

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## Instalação e uso

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## Escopo e limitações

Após iniciar o servidor, abra http://127.0.0.1:8769. As escolhas ficam em runtime/; --port altera a porta e --state seleciona outro arquivo de estado. O servidor escuta apenas em loopback e não oferece autenticação pública multiusuário. data/hooks.json contém 20 exemplos sintéticos originais, sem materiais de criadores ou métricas reais. Os IDs devem ser únicos; somente review.status=approved entra na fila. Use outro estado ao trocar o conjunto de cartões. As estatísticas descrevem suas escolhas, não preveem o desempenho com o público.

## Registro de validação

2026-10-24 · Python / HTTP: 14 ✓

## Licença e créditos

[MIT](LICENSE)

São versões da documentação. Interfaces, saídas CLI e executáveis mantêm o comportamento da implementação atual.

[Referência completa em chinês](README.zh-CN.md) · [Política de manutenção dos idiomas](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — Relate problemas reproduzíveis com dados sintéticos. Remova credenciais e informações privadas dos logs.
