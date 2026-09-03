# Living AI Wiki — 4개 AI 도구 공유 레포 설정 가이드

Claude(챗) · Claude Code · Codex(CLI/ChatGPT 클라우드) · ChatGPT(챗)를 하나의 레포에서
같은 규칙으로 작업시키기 위한 설정 가이드. `living-ai-wiki-report.docx`의 10.2 착수
체크리스트를 확장한다.

작성 시점: 2026-09-03. Codex/ChatGPT 관련 세부 사항(설정 파일 형식, 옵션명)은 OpenAI가
자주 바꾸므로, 실제 착수 시점에 `developers.openai.com/codex`에서 최신 문서를 한 번
더 확인할 것.

---

## 1. 원칙

네 도구는 능력이 다르므로 역할도 다르게 줘야 한다. 이 차이를 무시하고 "4개 도구에
똑같은 걸 시킨다"고 접근하면 설정이 꼬인다.

| 도구 | 코드 실행 / 파일 시스템 접근 | 이 프로젝트에서의 역할 |
| --- | --- | --- |
| **Claude Code** | 있음 (로컬 셸, 파일 읽기/쓰기, 훅) | 구현 주력. sources/ 불변 강제(PreToolUse 훅)를 실제로 걸 수 있는 유일한 도구 중 하나 |
| **Codex CLI** | 있음 (로컬 셸, 파일 읽기/쓰기, 샌드박스) | 구현 보조 또는 교차검증. Claude Code가 만든 코드를 다른 모델로 리뷰·재현할 때 유용 |
| **Codex (ChatGPT 클라우드)** | 있음 (GitHub 레포에 연결된 원격 컨테이너) | 백그라운드 작업 위임. PR 리뷰, 격리된 환경에서 실험 브랜치 작업 |
| **ChatGPT Projects (일반 챗)** | 없음 (파일 업로드만 가능, 레포 연결 불가) | 설계 논의, 문서 검토, 코드 스니펫 초안. 직접 실행/커밋 불가 |
| **Claude.ai Projects (일반 챗)** | 없음 (파일 업로드만 가능) | 위와 동일한 역할. 지금 이 프로젝트 문서가 올라가 있는 곳 |

핵심 원칙 세 가지:

1. **규칙은 한 곳에만 쓴다.** `AGENTS.md` 하나가 원본이고, 나머지 도구별 파일은
   그것을 참조하거나 가져올 뿐 규칙을 다시 쓰지 않는다. 규칙이 두 곳에 있으면
   반드시 벌어진다(diverge).
2. **"불변 규칙"이라고 적어놓는 것과 실제로 막는 것은 다르다.** 코드 실행형 도구
   4종 중 로컬에서 도는 두 개(Claude Code, Codex CLI)는 훅이나 파일 권한으로
   실제 집행이 가능하지만, 클라우드형(Codex 클라우드)과 챗형 두 개는 지시문을
   "따르기를 기대"하는 수준이다. §10에서 실제 집행 방법을 별도로 다룬다.
3. **챗형 두 도구(ChatGPT, Claude.ai)는 이 프로젝트의 실행자가 아니라 협업자다.**
   레포에 직접 접근하지 못하므로, 최신 상태를 사람이 수동으로 올려줘야 한다.
   이 동기화 부담을 인정하고 설계에 반영한다(§11).

---

## 2. 디렉토리 구조

```
mong-studio-wiki/                  # 레포 루트
├── AGENTS.md                      # 공통 규칙 원본 (단일 소스)
├── CLAUDE.md                      # AGENTS.md를 import + Claude 전용 추가사항
├── .codex/
│   └── config.toml                # Codex CLI 프로젝트 설정
├── .claude/
│   └── settings.json              # Claude Code 훅 설정 (sources/ 쓰기 차단)
├── sources/                       # 원본 ADR/설계 문서 — 불변
├── wiki/                          # LLM이 생성·유지하는 위키 페이지
├── answers/                       # 쿼리 결과물 (검색 대상 아님)
├── harness/                       # 평가 하네스
├── evals/                         # 질문셋, 결과 JSON
├── config/
│   └── models.yaml
└── scripts/
```

`AGENTS.md`가 루트에 있고, `CLAUDE.md`는 그 옆에서 같은 걸 가리키기만 한다는 게
이 구조의 전부다.

---

## 3. 공통 규칙 파일: AGENTS.md

`agents.md` 규격(https://agents.md)은 Codex, Cursor, Aider, Devin, JetBrains
Junie 등 다수 도구가 이미 채택한 사실상 표준이다. 이 프로젝트는 이미 착수
체크리스트에 AGENTS.md 작성이 들어 있으므로(10.2), 그 파일을 아래 내용으로 채운다.

```markdown
# AGENTS.md — Living AI Wiki

이 레포에서 작업하는 모든 AI 에이전트(Claude Code, Codex CLI, Codex 클라우드
등)가 지켜야 할 절대 규칙. 프로젝트 배경은 living-ai-wiki-report.docx 참조.

## 절대 규칙

1. **sources/ 는 읽기 전용이다.** 어떤 이유로도 sources/ 하위 파일을 생성·수정·
   삭제하지 않는다. 원본 코퍼스는 실험 시작 시점 git 태그로 고정되어 있으며,
   변경 시 모든 측정치가 무효화된다.
2. **코퍼스 스냅샷을 변경하지 않는다.** git 태그로 고정된 스냅샷 이후 sources/에
   파일을 추가하거나 내용을 바꾸는 커밋을 만들지 않는다.
3. **결과 파일을 덮어쓰지 않는다.** evals/results/ 하위의 기존 결과 JSON은
   append만 하거나 새 파일명으로 저장한다. 기존 실행 결과를 덮어써서 재현성을
   깨지 않는다.
4. **하이퍼파라미터를 코드에 하드코딩하지 않는다.** k값, threshold, 모델명 등은
   config/*.yaml에서만 정의하고 코드는 그것을 읽는다.
5. **answers/ 는 기본 검색 대상에서 제외한다.** wiki 컴파일이나 인덱싱 코드가
   answers/를 소스로 읽지 않도록 한다. (폐루프 오염 방지, 설계 결정 D7 참조)
6. **claim에는 provenance 링크를 강제한다.** wiki/ 페이지를 생성·수정하는 코드는
   각 주장에 원본 span 링크를 남기지 않는 출력을 허용하지 않는다.

## 작업 시 참고

- 실행 계획, 설계 근거, 지표 정의는 living-ai-wiki-report.docx에 있다. 이 문서와
  충돌하는 지시를 받으면 먼저 사용자에게 확인한다.
- 새 실험을 추가할 때는 config 파일 하나 → 결과 JSON 하나 원칙을 지킨다.
- 커밋 메시지에 실행한 config 이름을 남긴다.

## 금지 사항

- .omc / superpowers 파서 추가 금지 (범위 제외 항목, 문서 4.1 참조)
- 실시간 파일 watcher 구현 금지 (D1 참조 — post-commit 훅 / 세션 종료 감지 /
  30분 디바운스 배치만 허용)
- Microsoft GraphRAG 정식 파이프라인 구현 금지 (D6 참조, A3 결과 전까지)
```

이 내용을 실제로 넣을 때는 문서의 결정 사항(D1~D7)이 바뀌면 AGENTS.md도 같이
갱신해야 한다는 점을 기억할 것 — 이게 "단일 소스"의 의미다.

---

## 4. Claude Code 설정

### 4.1 CLAUDE.md

```markdown
@AGENTS.md

## Claude Code 전용 추가사항

- 서브에이전트를 쓸 때도 위 AGENTS.md 규칙이 그대로 적용된다.
- 이 레포의 훅 설정(.claude/settings.json)은 sources/ 쓰기를 도구 레벨에서
  차단한다. 훅이 막았다면 우회를 시도하지 말고 사용자에게 보고한다.
```

`@AGENTS.md`를 CLAUDE.md 첫 줄에 두면 Claude Code가 세션 시작 시 그 내용을
불러온 뒤, 그 아래 적힌 Claude 전용 내용을 이어 붙인다. 규칙 본문을 복사해 넣지
않는다 — 그러면 AGENTS.md를 고쳐도 CLAUDE.md는 그대로라 두 파일이 벌어진다.

### 4.2 sources/ 쓰기 차단 훅

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE '\"file_path\":\\s*\"[^\"]*sources/' && { echo 'sources/ 는 읽기 전용입니다' >&2; exit 2; } || exit 0"
          }
        ]
      }
    ]
  }
}
```

이 훅은 예시 골격이다. 실제 매칭 로직(파일 경로 추출 방식)은 착수 시점의 Claude
Code 훅 스펙 문서를 확인해 정확히 맞출 것 — 훅 입력 포맷은 버전에 따라 바뀔 수
있다. 훅이 정상 동작하는지는 체크리스트 항목("sources/ 쓰기 차단 훅 설정 및
실제 차단 동작 확인")대로 반드시 실제로 시도해서 막히는지 확인한다.

---

## 5. Codex CLI 설정

### 5.1 설치

```bash
npm install -g @openai/codex
# 또는
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### 5.2 AGENTS.md는 그대로 읽힌다

Codex CLI는 AGENTS.md를 네이티브로 지원한다. 별도 CODEX.md를 만들 필요가 없다.
동작 방식:

- 전역: `~/.codex/AGENTS.md` (모든 프로젝트 공통 지시, 이 프로젝트 특화 내용은
  여기 넣지 않는다)
- 프로젝트: 레포 루트부터 현재 작업 디렉토리까지 경로상의 각 디렉토리에서
  AGENTS.md를 찾아 합친다. 루트 쪽이 먼저, cwd에 가까운 파일이 나중에 붙는 순서라
  더 구체적인 지시가 실질적으로 우선한다.
- 하위 디렉토리별로 다른 규칙을 주고 싶으면 (예: harness/AGENTS.md에 하네스
  전용 규칙 추가) 해당 디렉토리에 파일을 따로 두면 된다. 이 프로젝트는 지금
  단계에서는 루트 AGENTS.md 하나로 충분하다.

즉 §3에서 만든 AGENTS.md 하나가 Claude Code(§4)와 Codex CLI 양쪽에서 동시에
원본 규칙 역할을 한다 — 이게 이 가이드의 핵심 이점이다.

### 5.3 config.toml

`.codex/config.toml` (레포 루트, 프로젝트 전용 오버라이드):

```toml
model = "gpt-5.5"                    # 착수 시점 최신 모델명으로 확인 후 교체
approval_policy = "on-request"       # 샌드박스 밖 동작만 승인 요청
sandbox_mode = "workspace-write"     # 워크스페이스 내 읽기/쓰기 + 로컬 명령 실행 허용
```

옵션 값(모델명, approval_policy·sandbox_mode 후보값)은 OpenAI가 바꿀 수 있으니
착수 전에 `codex --help`와 공식 config 문서로 재확인한다.

`sandbox_mode = "workspace-write"`는 sources/를 막아주지 않는다 — "워크스페이스
전체 쓰기 가능"이라는 뜻이라서, sources/ 보호는 config가 아니라 §10의 파일 권한
방식으로 해야 한다.

### 5.4 MCP 서버가 필요하면

이 프로젝트에서 당장 MCP가 필요하진 않지만(하네스는 자체 구현), 나중에 외부
도구를 붙일 경우:

```bash
codex mcp add <서버이름> -- <실행커맨드>
```

또는 config.toml에 `[mcp_servers.<이름>]` 블록으로 직접 정의한다.

---

## 6. Codex (ChatGPT 클라우드) 설정

로컬 셸이 아니라 GitHub 레포에 연결된 원격 컨테이너에서 도는 버전. 백그라운드로
장시간 작업을 맡기거나, PR 리뷰를 자동화할 때 쓴다.

### 6.1 연결

1. chatgpt.com/codex 접속 → GitHub 계정 연결 (레포에 대해 push 또는 admin 권한
   필요).
2. 이 레포를 대상으로 "environment"를 만든다 — 어떤 셋업 스크립트를 돌릴지,
   어떤 툴을 쓸 수 있게 할지 정의.
3. AGENTS.md는 여기서도 그대로 읽힌다 (루트 파일 = 레포 전체 규칙, 하위 디렉토리
   파일 = 해당 디렉토리 변경 시에만 적용). 별도 설정 불필요.

### 6.2 작업 방식

세 가지 진입점이 있다:

- **웹 UI**에서 직접 작업(task) 생성
- **IDE에서** 클라우드 작업을 걸어놓고 나중에 diff를 로컬로 당겨오기
- **GitHub PR/이슈 코멘트**에서 `@codex review`, `@codex fix the ...` 같은 명령으로
  호출

결과는 PR로 돌아오거나(새 브랜치 + PR 생성), 리뷰 코멘트로 돌아온다(우선순위
높은 이슈만 기본 노출). 사람이 diff를 확인하고 머지 여부를 결정하는 구조라,
이 프로젝트처럼 "재현성이 생명"인 작업에는 오히려 잘 맞는다 — 자동 머지 없이
항상 리뷰 단계를 거친다.

### 6.3 이 프로젝트에서의 용도 제안

- Claude Code로 만든 하네스/파이프라인 코드를 Codex 클라우드에게 "다른 모델
  관점에서" 리뷰시켜 교차검증(예: A1~A5 ablation 구현이 config만 바꿔서 재현
  가능한 구조인지 점검).
- 7주차 Audit 파이프라인처럼 독립적으로 걸어놓고 결과만 나중에 확인해도 되는
  작업을 백그라운드로 위임.
- sources/ 보호는 §10 방식(파일 권한 + 브랜치 보호)에 반드시 의존한다 — 클라우드
  컨테이너는 로컬 훅이 없으므로 AGENTS.md의 "읽기 전용" 문구만으로는 집행력이
  없다.

---

## 7. ChatGPT Projects 설정 (일반 챗)

레포에 직접 연결되지 않는다는 전제를 깔고 쓴다. 이 도구의 역할은 "구현"이 아니라
"설계 논의·문서 검토"다.

### 7.1 설정 절차

1. ChatGPT에서 새 Project 생성, 이름은 레포와 동일하게 (예: `living-ai-wiki`).
2. Project의 custom instructions에 다음을 넣는다:

   ```
   이 프로젝트는 living-ai-wiki 레포 작업을 위한 논의 공간이다. 첨부된
   AGENTS.md와 living-ai-wiki-report.docx가 규칙과 설계 근거의 원본이다.
   코드 구현이나 실행은 이 대화에서 하지 않는다 — Claude Code / Codex CLI가
   담당한다. 여기서는 설계 검토, 코드 스니펫 초안, 이슈 분석만 한다.
   AGENTS.md의 절대 규칙(특히 sources/ 불변, 하드코딩 금지)에 위배되는
   제안을 하지 않는다.
   ```

3. Project 파일로 `AGENTS.md`와 `living-ai-wiki-report.docx`를 업로드한다
   (Google Drive 연동이 있다면 그쪽으로 동기화해도 된다 — Slack/Drive만 지원,
   GitHub 레포 직접 연결은 안 됨).

### 7.2 한계와 대응

- **파일 업로드는 스냅샷이다.** AGENTS.md를 레포에서 고치면 ChatGPT Project의
  업로드본은 자동으로 갱신되지 않는다. §11의 동기화 절차를 따른다.
- **코드 실행/커밋 불가.** 여기서 나온 코드 스니펫은 사람이 복사해서 Claude
  Code나 Codex CLI에게 "이 스니펫을 검토하고 반영해줘" 형태로 넘겨야 한다.
- 조직에 ChatGPT Work(에이전트 모드)가 있다면 더 넓은 자동화가 가능할 수 있지만,
  이 프로젝트처럼 재현성이 핵심인 실험 코드베이스에는 권장하지 않는다 — 실행
  경로가 불투명해지면 8주차 재현성 목표(G4)와 충돌한다.

---

## 8. Claude.ai Projects 설정 (일반 챗)

이미 이 프로젝트가 "Living LLM Wiki"라는 Claude Project로 만들어져 있고
`living-ai-wiki-report.docx`가 올라가 있다. 여기에 AGENTS.md를 프로젝트 문서로
추가하면 §7과 동일한 역할(설계 논의·리뷰)을 이 쪽에서도 할 수 있다. 절차:

1. AGENTS.md 작성 완료 후, 이 Claude Project에 문서로 저장(예:
   `claude/AGENTS.md` 경로).
2. 커스텀 인스트럭션에 "코드 실행/커밋은 Claude Code·Codex CLI 담당, 여기선
   설계 검토만"이라는 문구를 넣어 ChatGPT Project와 동일한 역할 분리를 명시.

ChatGPT Project와 마찬가지로 레포에 실시간 연결되지 않으므로 동일한 동기화
문제를 갖는다.

---

## 9. sources/ 불변성 — 실제 집행 메커니즘

AGENTS.md에 "sources/는 읽기 전용"이라고 적는 것은 로컬 도구(Claude Code 훅,
Codex CLI 승인 정책)에는 어느 정도 먹히지만, 클라우드/챗형 도구에는 지시일 뿐
강제력이 없다. 도구에 의존하지 않는 실제 집행 방법을 겹겹이 둔다:

1. **파일 시스템 권한.** 스냅샷 고정 직후:
   ```bash
   chmod -R a-w sources/
   ```
   OS 레벨 권한이라 어떤 도구를 쓰든 쓰기 자체가 실패한다.

2. **git 커밋 훅.** pre-commit 훅에서 `sources/` 하위 변경분이 staged 되어
   있으면 커밋을 거부.

3. **GitHub 브랜치 보호 규칙 (Codex 클라우드가 PR을 만드는 경로에 대비).**
   sources/ 경로에 대한 CODEOWNERS 지정 + 필수 리뷰어 설정으로, 자동 생성된
   PR이 그냥 머지되지 않게 막는다.

4. **CI 체크.** PR마다 `git diff main --name-only`로 sources/ 변경 여부를
   검사하는 단계를 넣어 실패시키기.

이 네 가지 중 최소 1, 2번은 착수 체크리스트(10.2)에 이미 있는 항목이니 그대로
구현하고, 3~4번은 Codex 클라우드를 실제로 쓰기 시작하는 시점에 추가한다.

---

## 10. AGENTS.md 갱신 시 전파 절차

설계 결정(D1~D7)이 바뀌거나 새 절대 규칙이 생기면:

1. `AGENTS.md`(원본)만 수정하고 커밋.
2. `CLAUDE.md`, `.codex/config.toml`은 보통 손댈 필요 없음 (import 방식이므로
   자동 반영).
3. ChatGPT Project / Claude.ai Project에는 갱신된 AGENTS.md 파일을 다시
   업로드 — 이 프로젝트를 진행하며 위 4곳 규칙이 벌어지지 않았는지 주 1회 정도
   점검하는 습관을 들인다 (8주 일정 특성상 착수 체크리스트에 넣어도 됨).

---

## 11. 착수 체크리스트 (확장판)

기존 living-ai-wiki-report.docx 10.2에 아래 항목을 추가한다.

- [ ] AGENTS.md 작성 (본 가이드 §3 내용 기반)
- [ ] CLAUDE.md 작성 — `@AGENTS.md` import 방식 확인
- [ ] `.codex/config.toml` 작성 및 `codex`로 AGENTS.md가 실제로 로드되는지 확인
      (세션 시작 로그 또는 `/status` 류 명령으로 확인)
- [ ] `chmod -R a-w sources/` 실행 및 세 도구(Claude Code, Codex CLI, Codex
      클라우드) 각각에서 sources/ 쓰기 시도 → 실제로 실패하는지 확인
- [ ] pre-commit 훅으로 sources/ 변경 커밋 차단 확인
- [ ] ChatGPT Project 생성, AGENTS.md + report.docx 업로드, custom instructions
      설정
- [ ] Claude.ai Project(현재 이 프로젝트)에 AGENTS.md 추가
- [ ] (Codex 클라우드를 실제로 쓸 계획이면) GitHub 레포 연결 + environment
      설정 + CODEOWNERS로 sources/ 보호

---

## 12. 요약: 무엇이 진짜로 "공유"되는가

- **공유되는 것**: 규칙 텍스트(AGENTS.md 원본), 그 규칙이 유도하는 행동
  (sources/ 안 건드림, 하드코딩 안 함 등).
- **공유되지 않는 것**: 실행 컨텍스트. 네 도구는 같은 규칙을 보고 있어도 각자
  다른 세션에서 따로 돈다. "4개가 하나의 에이전트처럼 협업"하는 게 아니라,
  "4개가 같은 규칙서를 보고 각자 맡은 역할을 한다"는 것이 이 설정의 실제
  의미다. 실행 이력(누가 뭘 했는지)은 git 커밋 로그와 evals/results/의 config→
  결과 JSON 매핑이 대신한다 — 이게 8주차 재현성 목표(G4)와도 맞아떨어진다.
