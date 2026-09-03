# AGENTS.md — Living AI Wiki

이 레포에서 작업하는 모든 AI 에이전트가 지켜야 할 규칙입니다. 프로젝트 배경과 실행 계획은 `docs/living-ai-wiki-report.docx`를 참고합니다.

## 절대 규칙

1. `sources/`는 읽기 전용이다. 어떤 이유로도 스냅샷 이후 하위 파일을 생성·수정·삭제하지 않는다.
2. 코퍼스 스냅샷을 변경하지 않는다. 고정된 git tag 이후 `sources/` 변경 커밋을 만들지 않는다.
3. `evals/results/`의 기존 결과를 덮어쓰거나 삭제하지 않는다. 매 실행은 새 파일로 저장한다.
4. k, threshold, 모델명, 반복 횟수 같은 실험 파라미터를 코드에 하드코딩하지 않는다. `config/*.yaml`에서 정의하고 코드는 이를 읽는다.
5. `answers/`를 위키 컴파일·검색·인덱싱의 입력으로 사용하지 않는다.
6. `wiki/`의 각 claim에는 원본 source ID와 span을 가리키는 provenance가 있어야 한다. 근거 없는 claim을 허용하지 않는다.

## 작업 규칙

- 새 실험은 config 파일 하나에서 시작해 새 결과 JSON 하나 이상을 만든다.
- 결과에는 config 경로, git commit, corpus tag, 모델 ID, seed 또는 반복 번호를 기록한다.
- 커밋 메시지에 실행한 config 이름을 남긴다.
- 구현이나 지시가 기획서의 D1~D7 결정과 충돌하면 변경 전에 사용자에게 확인한다.
- 기능 변경 후 `uv run pytest`와 `uv run ruff check .`를 실행한다.

## 금지 사항

- `.omc` 또는 superpowers 파서 추가 금지
- 실시간 파일 watcher 구현 금지
- A3 결과가 나오기 전 Microsoft GraphRAG 정식 파이프라인 구현 금지
- 실측 전 README·리포트·포트폴리오에 성과 수치 기재 금지

## Code Review Rules

- `sources/` 변경이 포함된 PR을 승인하지 않는다.
- 기존 `evals/results/` 파일 수정·삭제를 승인하지 않는다.
- 실험 파라미터가 코드에 직접 들어가면 config로 이동하도록 요청한다.
- `answers/`가 검색 입력에 포함되거나 provenance 없는 wiki claim이 생성될 수 있으면 차단한다.
- 재현 명령, config, 결과 스키마 중 하나라도 빠진 실험 결과는 완료로 간주하지 않는다.

