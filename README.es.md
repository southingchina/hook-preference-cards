# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

Página local de preferencias mediante tarjetas para practicar aperturas, títulos e ideas. Permite indicar gusto o rechazo, omitir, marcar una apertura inválida, deshacer, recuperar el progreso, consultar estadísticas de características y exportar JSON o CSV. Utiliza un servidor con la biblioteca estándar de Python y HTML/CSS/JavaScript sin dependencias de frontend.

## Requisitos

Python 3.10+; HTML/CSS/JavaScript

## Configuración y puntos de entrada

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## Instalación y uso

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## Alcance y limitaciones

Tras iniciar el servidor, abre http://127.0.0.1:8769. Las elecciones se guardan en runtime/; --port cambia el puerto y --state selecciona otro archivo de estado. El servidor solo escucha en bucle local y no incluye autenticación pública multiusuario. data/hooks.json contiene 20 ejemplos sintéticos originales, sin material de creadores ni métricas reales. Los ID deben ser únicos; solo review.status=approved entra en la cola. Usa un estado nuevo al cambiar el conjunto de tarjetas. Las estadísticas describen tus elecciones, no el rendimiento esperado ante una audiencia.

## Registro de validación

2026-10-24 · Python / HTTP: 14 ✓

## Licencia y atribución

[MIT](LICENSE)

Son versiones de la documentación. Las interfaces, salidas CLI y ejecutables mantienen el comportamiento de la implementación actual.

[Referencia completa en chino](README.zh-CN.md) · [Política de mantenimiento de idiomas](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — Comunica problemas reproducibles con datos sintéticos. Elimina credenciales e información privada de los registros.
