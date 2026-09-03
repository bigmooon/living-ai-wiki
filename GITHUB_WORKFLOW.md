# GITHUB_WORKFLOW.md — GitHub 운영 규칙

이 문서는 Living AI Wiki 레포의 GitHub 운영 방식(라벨·이슈·마일스톤·브랜치·PR·커밋·
릴리스)을 정의한다. 근거 문서는 다음 둘이다.

- [`AGENTS.md`](AGENTS.md) — 에이전트 절대 규칙 원본. 이 문서는 그것을 복제하지 않고
  참조만 한다.
- `docs/living-ai-wiki-report.docx` — 특히 7장(실행 계획), 8장(범위 관리),
  부록 A(포트폴리오 포지셔닝).
- [`docs/AGENT_TOOLS_SETUP.md`](docs/AGENT_TOOLS_SETUP.md) — 4-tool 워크플로우, sources/
  불변성의 실제 집행 메커니즘(§9). 이 문서에서는 그 메커니즘을 재설명하지 않는다.

**전제**: 개인 8주 프로젝트이며 채용 포트폴리오로도 쓰인다. Claude Code / Codex CLI /
Codex 클라우드 3개 에이전트가 커밋·PR을 만들 수 있다. 라벨·마일스톤·PR 히스토리
자체가 실력을 보여주는 산출물이라는 전제를 깐다 — 따라서 "그럴듯해 보이는 절차"가
아니라 "실제로 굴러가고, 남이 봐도 왜 이렇게 했는지 알 수 있는 절차"를 우선한다.
동시에 과설계를 피한다: 여러 명의 필수 승인자, 복잡한 CODEOWNERS 매트릭스 같은
다인 조직 프로세스는 넣지 않는다.

---

## A. 라벨 체계 (확정 — 기존 스캐폴드 기준, `gh label list`로 실측 반영)

**중요**: 레포에는 이미 `.github/ISSUE_TEMPLATE/*.yml`이 전제하는 라벨셋이
콜론-스페이스 표기(`type: xxx`, `area: xxx`)로 존재한다. 이 문서는 그것과 다른
새 네이밍(예: `type/decision`처럼 슬래시 표기)을 제안하지 않는다 — 두 표기가
공존하면 그 자체가 첫 번째로 정리해야 할 비일관성이 된다. 아래는 기존 라벨 위에
필요한 만큼만 얹는다.

기존 라벨 (콜론-스페이스 표기 유지, `bug`/`enhancement` 등 GitHub 기본 라벨은 생략):

| 라벨 | 용도 (기존 정의) |
| --- | --- |
| `type: experiment` | 측정 가설과 config→result 실행 작업 (B0~B3/W1/G1, A1~A5 포함) |
| `type: implementation` | 파이프라인·하네스 구현 작업 |
| `type: evaluation` | 지표·라벨링·감사 작업 |
| `area: corpus` | ADR 코퍼스와 스냅샷 관련 |
| `area: retrieval` | BM25·dense·RRF 검색 경로 |
| `area: wiki` | 위키 컴파일·그래프·provenance |
| `area: governance` | 재현성·보호 규칙·CI |
| `priority: critical` | 마일스톤 전제 또는 일정 차단 |
| `status: blocked` | 외부 결정이나 선행 작업 대기 |

버그는 별도 `type: bug`를 만들지 않고 GitHub 기본 `bug` 라벨을 그대로 쓴다
(`bug_report.yml` 템플릿과 일치). `area`/`priority`/`status` 축은 이미 갖춰져
있으므로 이 문서에서 새로 제안하지 않는다.

프로젝트 고유 구조(D1~D7, A1~A5, B0~B3/W1/G1)를 위해 라벨을 더 세분화하지
않는다 — report.docx 표를 라벨로 축소 복제하면 표가 바뀔 때마다 라벨셋도
갱신해야 하는 이중 관리가 생긴다. 구체 코드는 라벨이 아니라 이슈 제목에
표기한다(아래 규칙).

이 문서에서 실제로 추가한 라벨 (기존 축이 다루지 않던 부분):

| 라벨 | 용도 |
| --- | --- |
| `type: decision` | D1~D7 설계 결정의 변경·재검토·신규 기록 (기존 3종에는 이 축이 없음) |
| `agent: claude-code` | Claude Code가 작업 주체인 이슈/PR |
| `agent: codex-cli` | Codex CLI가 작업 주체 |
| `agent: codex-cloud` | Codex 클라우드가 작업 주체 |
| `cuttable` | 8.2 절단 순서 대상 (아래 참고) |

우선순위·영역(`priority: *`, `area: *`) 라벨은 위에 이미 정리한 대로 기존
스캐폴드에 존재하며, 이 문서는 그 축을 더 세분화하지 않는다. `priority: critical`
하나만 있고 p1/p2처럼 여러 단계로 나누지 않는 것도 기존 설계 그대로 유지한다 —
8주 개인 프로젝트에서 우선순위를 여러 단계로 세분화하는 것은 과설계다.

**이슈 제목 코드 표기 규칙**: `[D3]`, `[A1]`처럼 대괄호로 report.docx 코드를 표기한다.
`type: experiment`/`type: implementation` 템플릿 모두 제목 프리픽스가 `[Experiment]`
`[Implementation]`으로 고정되어 있으므로, report 코드는 그 뒤에 이어 쓴다
(예: `[Experiment] [A1] hybrid vs dense vs BM25`).

단, **`G1`은 report.docx 안에서 코드가 충돌한다** — 3장 목표표의 G1("검색 전략별
강점 규명")과 6.1 비교대상표의 G1("그래프 순회 baseline")은 같은 코드, 다른 의미다.
이슈 제목에서 반드시 구분자를 붙인다: `[목표 G1]` / `[경로 G1]`. (코드 자체를 report에서
고칠지는 이 문서의 범위 밖이며, 필요하면 별도로 판단한다.)

**`cuttable` 라벨**: 8.2절 절단 순서(1순위 Lint → 2순위 대시보드 → 3순위 faithfulness는
끝까지 사수)를 반영해, 절단 후보 1·2순위 작업(Lint 파이프라인, 대시보드)에
`cuttable`을 붙인다. faithfulness 관련 이슈에는 붙이지 않는다 — 절대 자르지 않는
항목이라는 의도를 라벨로도 드러낸다.

### 착수 체크리스트
- [x] `type: decision`, `agent: claude-code`, `agent: codex-cli`, `agent: codex-cloud`, `cuttable` 5개 라벨 생성 완료 (`gh label create`)
- [ ] 기존 GitHub 기본 라벨(`enhancement`, `question`, `duplicate` 등) 중 안 쓸 것 삭제 또는 유지 여부 결정
- [ ] `[목표 G1]` / `[경로 G1]` 구분 규칙을 이슈 템플릿 설명(`description`)에도 반영 (B절 참고)

---

## B. 이슈 컨벤션

### 템플릿 3종 (기존 2종 + 신규 1종)

기존에 이미 `.github/ISSUE_TEMPLATE/`에 `experiment.yml`(실험/ablation)과
`implementation.yml`(구현 작업), `bug_report.yml`(버그·평가 오염)이 있다. 이 문서가
새로 정의하는 것은 **`decision.yml`** 하나뿐이다 — D1~D7 같은 설계 결정 변경을
기록할 자리가 기존 3종에 없었기 때문이다.

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 실험 이슈(`experiment.yml`) 보강 | 기존 필드(가설/config 경로/지표·판정 기준/완료 조건)는 유지. 완료 조건 체크리스트에 **"가설 기각 여부(채택/기각/판단 보류)가 이슈 코멘트로 기록됨"** 항목 추가 | 6.5 "부정적 결과도 결론으로 보고한다"(R10)를 이미 있는 완료 조건 체크리스트에 자연스럽게 얹는다. 새 필드 타입을 늘리지 않고 기존 구조를 확장하는 쪽이 스캐폴드와 일관적이다 |
| 결정 이슈(`decision.yml`, 신규) | 관련 D-코드, 변경 전/후, report.docx 해당 절, AGENTS.md 갱신 필요 여부, 사용자 확인 여부 | D1~D7이 바뀌면 AGENTS.md도 같이 갱신해야 하므로(AGENT_TOOLS_SETUP.md §10), 이슈에서 그 갱신 여부를 체크리스트로 남긴다. AGENTS.md 작업 규칙("D1~D7 결정과 충돌하면 변경 전에 사용자에게 확인")도 필드로 강제 |
| 코드 표기 | 제목에 `[A1]`, `[D3]`, `[경로 G1]` 등 report.docx 코드 필수. `experiment.yml`/`implementation.yml`은 제목 프리픽스가 `[Experiment]`/`[Implementation]`으로 고정되어 있으므로 코드는 그 뒤에 붙인다 | 문서와 이슈 간 추적성. 코드 없는 실험/결정 이슈는 승인하지 않는다(Code Review Rules와 연결) |
| 일반 버그(`bug_report.yml`) | 코드 표기 선택 | 실험·결정과 무관한 순수 버그까지 코드를 강제하면 형식주의가 된다. 기존 필드(관찰된 현상/재현 방법/기대 동작/평가 오염 가능성)로 충분 |

`experiment.yml`의 `acceptance` 필드(완료 조건 체크리스트)에 추가할 항목:
```
- [ ] 가설 기각 여부(채택/기각/판단 보류)가 이슈 코멘트로 기록됨
```

### 착수 체크리스트
- [ ] `.github/ISSUE_TEMPLATE/experiment.yml`의 `acceptance` 필드에 "가설 기각 여부" 체크 항목 추가
- [ ] `.github/ISSUE_TEMPLATE/decision.yml` 신규 작성 (D-코드, 변경 전/후, AGENTS.md 갱신 여부, 사용자 확인 여부 필드)
- [ ] 각 템플릿 `description` 또는 본문에 `[목표 G1]`/`[경로 G1]` 구분 규칙 명시

---

## C. 마일스톤 / 프로젝트 보드

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 마일스톤 단위 | 7.1절 4개 마일스톤(1주차 말/3주차 말/6주차 말/8주차 말)에 **1:1 매핑**. 8개로 주차별 세분화하지 않음 | 7.1절 마일스톤은 이미 "의미"가 붙은 판단 지점이다(측정 기반 확보 / 핵심 결과 확보 / 설계 검증 완료 / 문서화 완료). 주차별로 쪼개면 8개의 형식적 체크포인트가 생기지만 판단 지점은 늘지 않는다. 개인 프로젝트에서 마일스톤은 진행 추적용이 아니라 "여기서 멈춰서 판단한다"는 신호여야 한다 |
| 마일스톤 설명 | 각 마일스톤 설명에 7.1절 "의미" 열 문장을 그대로 인용. 3주차 말 마일스톤 설명에는 8.1절 분기점 판단 기준 전문을 인용 | "3주차에 유형별 승자가 갈리지 않으면 3-way 라우터의 전제 자체가 성립하지 않는다"는 판단 기준을 마일스톤 설명에서 바로 볼 수 있어야, 그 시점에 실제로 그 질문을 던지게 된다 |
| GitHub Projects 보드 | 사용한다. 컬럼: `Backlog` → `This Week` → `In Progress` → `Blocked/Needs Decision` → `Done` | 개인 프로젝트라 스프린트/스윔레인 같은 다인 조직 구조는 불필요. 주 단위 실행 계획(7장 표)과 맞춰 "이번 주" 컬럼 하나만 별도로 둔다 |
| 보드-이슈 연결 | 모든 실험/결정 이슈는 보드에 올리고, 라벨(`type: *`, `agent: *`)로 필터 뷰 구성 | 별도 필드 대신 기존 라벨(A절)을 재사용해 관리 축을 하나로 유지 |

### 착수 체크리스트
- [ ] Milestone 4개 생성, 설명에 7.1절 "의미" + (3주차만) 8.1절 분기점 기준 인용
- [ ] GitHub Projects 보드 생성, 5개 컬럼 구성
- [ ] 1주차 이슈부터 마일스톤·보드에 연결

---

## D. 브랜치 전략

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 병렬 작업 분리 | Claude Code(Track A: 파이프라인)와 Codex(Track B: 평가 하네스)가 git worktree로 디렉토리 분리 작업 — 기존 워크플로우 유지 | AGENT_TOOLS_SETUP.md의 역할 분담(Claude Code=구현 주력, Codex CLI=구현 보조/교차검증)을 브랜치 네이밍에도 반영 |
| 브랜치 네이밍 | `track-a/<설명>` (Claude Code, 파이프라인), `track-b/<설명>` (Codex, 하네스), `experiment/<코드>-<설명>` (예: `experiment/A1-hybrid`, `experiment/D5-router`) | 코드(A/D/B 등)가 브랜치명에 있으면 `git branch -a`만 봐도 report.docx와의 대응이 보인다 |
| main 보호 | 직접 push 금지, PR 필수. 상태 체크(CI: sources/ 불변 검사, pytest, ruff) 통과 필수. 필수 리뷰어는 두지 않음(1인 프로젝트) | 다인 조직의 필수 승인자 수를 흉내내지 않는다 — 셀프 머지가 기본이라는 E절 결정과 일관 |
| 머지 정책 | 실험/기능 브랜치는 스쿼시 머지. `main`↔장기 트랙 브랜치(있다면) 동기화는 일반 머지 | 실험 브랜치는 커밋이 시행착오 위주라 스쿼시로 히스토리를 정리하는 편이 낫다. 커밋 메시지 conventions(F절)는 스쿼시 커밋 메시지에 적용 |
| sources/ 이중 방어 | 이미 `.github/CODEOWNERS`에 `/sources/`, `/config/`, `/evals/results/`가 `@bigmooon`으로 지정되어 있고, `.github/workflows/repository-guard.yml`이 PR마다 `scripts/verify_repository_guards.py`로 `sources/` 변경을 검사한다. 이 문서는 새 메커니즘을 추가하지 않고, main 브랜치 보호 규칙에서 이 CI 체크(`repository-guard`)를 **필수 상태 체크**로 지정하는 것만 추가한다 | AGENT_TOOLS_SETUP.md §9가 말하는 "지시문 vs 실제 집행"의 차이는 여기서 이미 좁혀져 있다(파일 권한 스크립트 `protect_sources.sh` + pre-commit 훅 + CI 워크플로 3중). 브랜치 보호는 그 중 CI 체크가 "실패해도 머지는 가능"한 상태를 막는 마지막 연결 고리다 |

### 착수 체크리스트
- [x] 레포를 public으로 전환 (브랜치 보호는 GitHub Free 플랜에서 private 레포에 미지원 — sources/ 등 민감 파일 없음을 확인 후 전환)
- [x] main 브랜치 보호 규칙 설정 완료: PR 필수, 관리자 포함 강제(enforce_admins), force-push·삭제 금지, `test`(CI) 워크플로를 필수 상태 체크로 지정
- [ ] `Repository guard`(`protect-frozen-data` job)는 아직 실행 이력이 없어(현재 pull_request 트리거로만 동작) 필수 체크에서 보류. 이 job이 실제 PR에서 한 번 실행되어 체크 이름이 GitHub에 등록된 뒤, `gh api repos/bigmooon/living-ai-wiki/branches/main/protection/required_status_checks/contexts -X POST -f contexts[]=protect-frozen-data`로 추가
- [ ] worktree 기반 Track A/B 브랜치 네이밍 규칙을 팀(에이전트) 안내에 반영 (기존 CODEOWNERS/훅/CI는 변경 불필요)

---

## E. PR 컨벤션

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| PR 템플릿 | 기존 `.github/pull_request_template.md`(변경 내용/관련 이슈/재현 방법/검증 체크리스트)에 다음을 보강: 변경 전/후 수치(측정된 경우만 — 없으면 "TBD, 착수 전/측정 전" 명시), `sources/` 미변경·config 하드코딩 없음 체크 항목, 교차검증 섹션. 새 템플릿을 만들지 않고 기존 파일을 확장 | Code Review Rules(AGENTS.md)의 차단 조건을 PR 템플릿 체크리스트로 선반영해, 리뷰 시점이 아니라 PR 작성 시점에 걸러지게 한다. 이 확장은 본 착수 작업 중 이미 반영 완료(아래 참고) |
| 리뷰 절차 | 기본은 셀프 머지. Codex 클라우드를 "다른 모델 관점 교차검증"으로 쓸 때는 `@codex review`로 호출하고, 코멘트가 달리면 반영 여부를 PR 본문에 기록한 뒤에 머지 | 개인 프로젝트이므로 필수 리뷰어를 두지 않되, 실제로 받은 교차검증 코멘트는 무시하지 않고 흔적을 남긴다 — 이것 자체가 "책임감 있는 AI 도구 활용" 신호(F절과 연결) |
| 에이전트 식별 | PR 제목 프리픽스 `[claude-code]` / `[codex-cli]` / `[codex-cloud]` + 동일 이름의 `agent: *` 라벨(A절) 자동 부여 | 라벨과 제목 두 곳에 표기해 필터링(보드)과 가독성(PR 목록) 둘 다 확보 |

### 착수 체크리스트
- [x] `.github/pull_request_template.md` 보강 완료 (변경 전/후 수치, sources/·하드코딩 체크, 교차검증 섹션 추가)
- [ ] PR 제목 프리픽스 규칙을 각 에이전트의 설정 파일(CLAUDE.md 등)에 참조로 추가할지 판단 — 필요하면 별도 확인 후 반영

---

## F. 커밋 컨벤션

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 형식 | Conventional Commits (`feat:`, `fix:`, `data:`, `chore:`, `docs:`) + footer에 `Config: config/experiments/<파일명>.yaml` | AGENTS.md 기존 규칙("커밋 메시지에 실행한 config 이름을 남긴다")을 footer 필드로 구조화 — grep 가능하게 만든다 |
| 실험 커밋 footer | `Config:`, `Corpus-Tag:`, `Model:`, `Run:` (반복 번호/seed) | evals/results/ JSON에 요구되는 메타데이터(config 경로, git commit, corpus tag, 모델 ID, seed/반복 번호)와 대칭 — 커밋만 봐도 어떤 결과 JSON과 짝인지 역추적 가능 |
| 에이전트 표기 | `Co-Authored-By: <Agent Name> <noreply@...>` 트레일러. 예: `Co-Authored-By: Claude Code <noreply@anthropic.com>`, `Co-Authored-By: Codex CLI <noreply@openai.com>` | 표준 git 트레일러라 GitHub 기여자 그래프에도 반영됨. "AI 도구를 책임감 있게 활용했다"는 신호로 포트폴리오에서 그대로 인용 가능(A.6 방법론 서사와 연결 — 도구를 숨기지 않는다) |

**예시:**
```
feat(retrieval): implement hybrid BM25+dense with RRF

Config: config/experiments/a1-hybrid.yaml
Corpus-Tag: corpus-v1
Model: <embedding-model-id>
Run: 3/3

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

### 착수 체크리스트
- [ ] 커밋 메시지 footer 형식을 CLAUDE.md/AGENTS.md 작업 규칙에 참조 추가할지 판단
- [ ] 실험 커밋에 `Config:`/`Corpus-Tag:`/`Model:`/`Run:` footer 실제로 붙는지 1주차 첫 실험 커밋으로 확인

---

## G. 릴리스 노트 컨벤션

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 태그 명명 | 7.1 마일스톤과 정렬: `v0.1-baseline`(1주차 말, B0), `v0.2-hybrid`(3주차 말, 승패표), `v0.3-router`(6주차 말, A2~A4 판단), `v1.0-final`(8주차 말) | 마일스톤=판단 지점, 태그=그 지점의 스냅샷. 태그 이름만으로 어느 마일스톤 산출물인지 알 수 있게 한다. 8.1 분기점에서 라우터를 기각하는 경우 `v0.3-router`를 `v0.3-single-path`처럼 실제 결론에 맞게 조정 (사전에 이름을 고정하지 않고 6주차 판단 후 확정) |
| 공개 시점 규칙 | 부록 A.3 표를 릴리스 노트에도 그대로 적용: 착수 전(`v0.1` 이전)에는 성과 수치 기재 금지, 3주차 이후(`v0.2-hybrid`)부터 승패표 중심 수치 1개 문장, 6주차 이후(`v0.3-router`)부터 2~3개 문장, 8주차(`v1.0-final`)에 전체 구성 | AGENTS.md 금지사항("실측 전 README·리포트·포트폴리오에 성과 수치 기재 금지")과 A.3의 시점별 분량 원칙을 릴리스 노트라는 실제 산출물에 연결. 릴리스 노트도 "포트폴리오"의 일부로 취급 |
| 템플릿 구조 | ① 무엇을 측정했나 (config·질문셋 범위) ② 결과 (수치, 유형별 분리) ③ 기각한 것 (해당 마일스톤에서 판단 보류/기각된 A-코드, 이유) ④ 다음 결정 (다음 마일스톤에서 확인할 질문) | 6.5절 "부정적 결과도 결론으로 보고한다"를 릴리스 노트 구조 자체에 박아 넣는다. "기각한 것" 섹션이 비어 있으면 오히려 의심해야 할 신호(모든 게 성공했다는 결과는 드물다) |

### 착수 체크리스트
- [ ] `v0.1-baseline` 태그를 1주차 B0 측정 완료 시점에 생성, 릴리스 노트 4단 구조로 작성
- [ ] 각 릴리스 노트 작성 전 A.3 표에서 해당 시점의 허용 분량 재확인

---

## H. 채용 담당자를 위한 진입점

| 항목 | 결정 | 근거 |
| --- | --- | --- |
| 안내 필요 여부 | 필요함. README 상단에 짧은 안내 섹션 추가(고정 이슈는 만들지 않음) | 고정 이슈는 조직의 공지 채널을 흉내내는 형식이라 1인 레포에는 과하다. README는 이미 진입점 역할을 하고 있으므로 거기에 링크만 추가하는 편이 담백하다 |
| 링크 구조 | README에 "무엇을, 어디서 볼지" 3줄: ① 핵심 결과 → 최신 마일스톤 릴리스 노트(`v0.2-hybrid` 이후) ② 승패표 → 해당 실험 이슈 또는 릴리스 노트의 결과 섹션 ③ 설계 근거 → `docs/living-ai-wiki-report.docx` | 승패표가 핵심 산출물(부록 A.4 문서 구성 1순위)이므로 그것으로 바로 가는 링크를 최상단에 둔다 |
| 톤 | 사실만 나열. "이 프로젝트는 ~을 보여줍니다" 류의 자기 홍보 문구 없이, "무엇을 측정했고 어디서 확인 가능한가"만 서술 | A.5 "사용하지 않을 표현"(실사용 도구, 풀스택+AI 통합 등 검증 불가능한 주장)과 같은 원칙을 README 안내 섹션에도 적용 |

**README 안내 섹션 예시 문구 (참고용, 실측 후 실제 링크로 교체):**
```
## 결과 확인 경로
- 최신 측정 결과: [릴리스 노트](../../releases) (v0.2-hybrid 이후부터 수치 포함)
- 질문 유형 × 검색 경로 승패표: 해당 릴리스 노트 "결과" 섹션
- 설계 근거: docs/living-ai-wiki-report.docx (7장 실행 계획, 8장 범위 관리)
```

### 착수 체크리스트
- [ ] README에 "결과 확인 경로" 섹션 추가 (3주차 `v0.2-hybrid` 릴리스 이후 실제 링크로 채움)
- [ ] 착수 전(현재)에는 이 섹션을 만들되 "측정 전" 상태임을 명시 — README 현재 "현재 제한사항" 절과 모순 없게 유지

---

## 요약: TBD 항목과 확정 시점

| TBD 항목 | 확정 시점 |
| --- | --- |
| `v0.3-router` 태그명이 라우터 채택/기각에 따라 최종 어떻게 바뀔지 | 6주차 말 (8.1 분기점 실제 판단 후) |
| PR 제목 프리픽스를 각 에이전트 설정 파일에 자동 반영할지 | 각 에이전트로 실제 PR을 처음 만들 때 |
| README "결과 확인 경로"의 실제 링크 | 3주차 말 `v0.2-hybrid` 릴리스 시점 |
| `decision.yml` 이슈 템플릿과 `experiment.yml` 완료 조건 보강의 실제 반영 | 다음 세션에서 파일 작업으로 진행 |
| `Repository guard`(`protect-frozen-data`) 필수 상태 체크 추가 | 해당 job이 실제 PR에서 한 번 실행되어 체크 이름이 GitHub에 등록된 이후 |

## 이번 착수 작업에서 실제로 반영한 것 / 안 한 것

- **반영 (로컬 파일)**: `.github/pull_request_template.md` 보강 (기존 파일 확장, 신규 생성 아님).
- **반영 (GitHub 원격, `gh` CLI 설치 및 인증 후 진행)**:
  - `gh` CLI를 winget user-scope로 설치 (관리자 권한 불필요), 사용자가 브라우저 OAuth로 인증 완료.
  - 라벨 5종 생성: `type: decision`, `agent: claude-code`, `agent: codex-cli`, `agent: codex-cloud`, `cuttable`.
  - 레포를 private → public으로 전환 (브랜치 보호 규칙이 GitHub Free 플랜에서 private 레포에 미지원되어, `sources/`를 포함한 전체 커밋 이력에 민감 파일이 없음을 확인한 뒤 사용자 확인 하에 전환).
  - main 브랜치 보호 규칙 적용: PR 필수, 관리자 포함 강제, force-push·브랜치 삭제 금지, `test`(CI) 워크플로를 필수 상태 체크로 지정.
- **미반영 (후속 작업 필요)**: `decision.yml` 이슈 템플릿 신규 작성, `experiment.yml`
  완료 조건에 "가설 기각 여부" 항목 추가, GitHub Projects 보드, Milestone 4개 생성,
  `Repository guard` 워크플로를 필수 상태 체크에 추가(실행 이력 생긴 후). 위 각 절의
  착수 체크리스트에 남겨 두었다.
