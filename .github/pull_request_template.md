<!-- 제목 프리픽스: [claude-code] / [codex-cli] / [codex-cloud] 중 하나를 붙인다 -->

## 변경 내용

-

## 관련 이슈 / 실험

- Closes #
- Config:

## 재현 방법

```bash
# 실행 명령을 작성하세요.
```

## 변경 전/후 수치
<!-- 측정된 경우만 기재. 측정 전이면 "TBD, 착수 전/측정 전"이라고 명시하고
     숫자를 지어내지 않는다 (AGENTS.md 금지사항: 실측 전 성과 수치 기재 금지) -->


## 검증

- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] 필요한 경우 동일 config 반복 실행과 결과 파일 생성 확인
- [ ] `sources/` 변경 없음
- [ ] 기존 `evals/results/` 파일을 수정하거나 삭제하지 않음 (새 파일만 추가)
- [ ] 실험 파라미터(k, threshold, 모델명, 반복 횟수 등)가 코드에 하드코딩되지 않고 `config/*.yaml`에 있음
- [ ] `answers/`가 검색·인덱싱 입력에 포함되지 않음
- [ ] wiki claim 변경 시 provenance(원본 source ID + span)가 유지됨
- [ ] 커밋 메시지 footer에 `Config:` (실험 커밋인 경우) 포함

## 교차검증 (해당하는 경우)
<!-- Codex 클라우드에 @codex review로 교차검증을 요청했다면 코멘트 요약과
     반영 여부를 기록. GITHUB_WORKFLOW.md §E 참고 -->
