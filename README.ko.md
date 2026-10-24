# Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

글의 도입부, 제목과 창작 연습을 위한 로컬 카드 선호도 페이지입니다. 좋아요, 싫어요, 건너뛰기, 유효하지 않은 도입부 표시, 실행 취소, 저장한 진행 복구, 특징 통계 및 JSON/CSV 내보내기를 지원합니다. Python 표준 라이브러리 서버와 기본 HTML/CSS/JavaScript를 사용하며 프런트엔드 의존성 설치가 필요 없습니다.

## 필요 환경

Python 3.10+; HTML/CSS/JavaScript

## 설정 및 진입점

`data/hooks.json`, `runtime/`, `--port`, `--state`, `http://127.0.0.1:8769`

## 설치 및 사용

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```


```shell
python -m unittest discover -s tests -v
```


## 공개 범위와 제한

서버 실행 후 http://127.0.0.1:8769를 여세요. 선택은 runtime/에 저장되며 --port와 --state로 포트 및 상태 파일을 바꿀 수 있습니다. 루프백에만 바인딩하며 공개 다중 사용자 인증은 없습니다. data/hooks.json에는 실제 창작자 자료나 반응 수가 아닌 자체 제작 합성 예시 20개만 들어 있습니다. ID는 고유해야 하며 review.status=approved인 카드만 선택 대기열에 들어갑니다. 카드 묶음을 바꾸면 새 상태 파일을 사용하세요. 통계는 개인 선택을 나타내며 대중의 반응을 예측하지 않습니다.

## 검증 기록

2026-10-24 · Python / HTTP: 14 ✓

## 라이선스 및 출처

[MIT](LICENSE)

프로젝트 문서의 언어별 버전입니다. 앱 화면, CLI 출력과 실행 파일은 현재 구현을 따릅니다.

[중국어 상세 참고 문서](README.zh-CN.md) · [언어 문서 유지 관리 정책](docs/LOCALIZATION.md)

[Issues](https://github.com/southingchina/hook-preference-cards/issues) — 재현 가능한 문제는 합성 데이터로 보고하고 로그의 자격 증명과 개인 정보를 제거하세요.
