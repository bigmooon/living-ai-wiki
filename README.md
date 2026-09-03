# Living AI Wiki

시간에 따라 이전 결정이 뒤집히는 ADR 코퍼스에서 질문 유형별 검색 전략을 비교하고, 측정 결과를 바탕으로 검색 경로를 선택하는 3-way 라우터를 설계하는 프로젝트입니다.

> 현재 상태: **착수용 저장소 골격**. 아직 코퍼스 스냅샷과 실험 결과가 없으며, 성과 수치를 주장하지 않습니다.

## 왜 이 프로젝트인가

일반적인 검색 평가는 정답 문서를 찾았는지에 집중합니다. 하지만 ADR에는 폐기된 결정과 현재 유효한 결정이 함께 남습니다. 두 문서를 모두 정확히 검색해도 최신 결정을 구분하지 못하면 답은 틀릴 수 있습니다.

이 프로젝트는 다음 세 질문 유형에서 검색 경로별 성능을 분리해 측정합니다.

| 질문 유형 | 정의 | 비교할 주요 경로 |
| --- | --- | --- |
| 핀포인트 | 한 원본에 있는 구체적인 값이나 사실 | BM25 + dense + RRF hybrid |
| 종합 | 여러 문서의 배경과 근거를 합쳐야 하는 질문 | 컴파일된 wiki 페이지 |
| 멀티홉 | 결정 간 관계와 영향 전파를 따라가야 하는 질문 | wiki-link 그래프 순회 |

핵심 산출물은 애플리케이션 자체가 아니라 재현 가능한 `config -> result JSON -> report` 흐름과 질문 유형 × 검색 경로 승패표입니다.

## 목표

- G1: 핀포인트·종합·멀티홉 질문별 검색 경로의 Recall@k 차이 측정
- G2: 3-way 라우팅 정확도와 최선 단일 경로 대비 전체 정확도 비교
- G3: claim 단위 provenance 강제 전후의 근거 없는 주장 비율 감사
- G4: 제3자가 README와 config만으로 결과를 재현할 수 있는 실행 경로 제공

## 저장소 구조

```text
.
├── sources/                 # 고정된 원본 ADR 코퍼스 (스냅샷 이후 읽기 전용)
├── wiki/                    # LLM이 생성·유지하는 위키 페이지
├── answers/                 # 질의 결과물 (검색·인덱싱 대상 제외)
├── harness/                 # 평가 실행과 결과 스키마
├── evals/
│   ├── fixtures/            # 예시·시범 질문셋
│   └── results/             # 덮어쓰지 않는 실험 결과 JSON
├── config/
│   ├── models.yaml          # embedding / generation / judge 선택
│   └── experiments/         # 실험별 단일 설정 파일
├── scripts/                 # 스냅샷·보호·검증 도구
└── docs/                    # 기획서와 도구 설정 가이드
```

## 빠른 시작

Python 3.12와 [uv](https://docs.astral.sh/uv/)를 기준으로 합니다.

```bash
uv sync --all-groups
uv run living-wiki validate-config config/experiments/b0.yaml
uv run pytest
uv run ruff check .
```

### 1. 모델 설정 확정

`config/models.yaml`의 `TBD` 값을 실제 모델 ID와 선택 근거로 교체합니다. Judge는 generation 모델과 다른 계열로 고정합니다.

### 2. 코퍼스 최초 스냅샷

`sources/`가 비어 있는 현재 상태에서는 아래 작업을 실행하지 않습니다. ADR을 모두 넣고 검토한 뒤 한 번만 스냅샷을 고정합니다.

```bash
uv run python scripts/build_corpus_manifest.py
git add sources/ config/corpus-manifest.json
git commit -m "data: freeze corpus snapshot v1"
git tag corpus-v1
./scripts/install_git_hooks.sh
./scripts/protect_sources.sh
```

스냅샷 이후에는 `sources/`를 수정하지 않습니다. 변경이 필요하면 기존 실험과 섞지 말고 새 코퍼스 버전과 실험 계열을 설계합니다.

### 3. 실험 계약

- 한 실험은 `config/experiments/*.yaml` 하나로 정의합니다.
- 한 실행은 `evals/results/`의 새 JSON 파일 하나를 만듭니다.
- 기존 결과 파일을 수정하거나 덮어쓰지 않습니다.
- 모든 결과에는 config 경로, git commit, corpus tag, 모델 ID, 반복 번호를 기록합니다.
- 전체 평균보다 질문 유형별 지표를 우선 보고합니다.

## 평가 설계

| 코드 | 경로 | 역할 |
| --- | --- | --- |
| B0 | 원본 전체 컨텍스트 | 기준선 |
| B1 | dense only | 단일 검색 대조군 |
| B2 | BM25 only | 단일 검색 대조군 |
| B3 | BM25 + dense + RRF | 핀포인트 후보 |
| W1 | wiki 페이지 직독 | 종합 후보 |
| G1 | wiki-link 그래프 순회 | 멀티홉 후보 |

주요 지표는 Recall@k, Precision@k, nDCG@k, 라우팅 accuracy·confusion matrix, claim faithfulness 3분류, latency p50/p95, 토큰과 인덱싱 비용입니다.

## 8주 로드맵

| 마일스톤 | 완료 기준 | 목표 시점 |
| --- | --- | --- |
| M1 측정 기반 확보 | 코퍼스 고정, 질문 시범 라벨링, B0 3회 측정 | 1주차 말 |
| M2 핵심 결과 확보 | 질문 유형 × 검색 경로 승패표와 실패 사례 분석 | 3주차 말 |
| M3 설계 검증 완료 | 라우터·그래프·재검색 A2~A4 채택/기각 판단 | 6주차 말 |
| M4 문서화 완료 | faithfulness 감사, 재현 가이드, 최소 결과 뷰 | 8주차 말 |

3주차에 유형별 승자가 갈리지 않으면 3-way 라우터를 고집하지 않습니다. 단일 최적 경로를 확정하고 faithfulness 감사에 집중하는 것도 사전 정의된 유효한 결과입니다.

## 협업 및 보호 규칙

- 모든 에이전트 규칙의 원본은 [`AGENTS.md`](AGENTS.md) 하나입니다.
- Claude Code는 [`CLAUDE.md`](CLAUDE.md)에서 이를 import합니다.
- 로컬 커밋 훅은 `sources/` 변경과 기존 결과 JSON 수정·삭제를 차단합니다.
- PR CI는 스냅샷 이후 `sources/` 변경을 거부합니다.
- `answers/`는 위키 컴파일과 검색 인덱싱 대상에서 제외합니다.

세부 설계 근거는 `docs/living-ai-wiki-report.docx`, 에이전트 도구 설정은 `docs/AGENT_TOOLS_SETUP.md`를 참고하세요.

## 현재 제한사항

- 실제 ADR 코퍼스가 아직 포함되지 않았습니다.
- embedding / generation / judge 모델은 아직 확정되지 않았습니다.
- 현재 골격의 의존성은 `uv.lock`으로 고정되어 있으며, 모델 SDK를 확정할 때 함께 갱신합니다.
- 측정 전이므로 README와 포트폴리오에 결과 수치를 기재하지 않습니다.
