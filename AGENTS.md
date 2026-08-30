# Repository Execution Guide

이 파일은 Canonical Governance 출처가 아니라 저장소 탐색과 제한된 실행을 위한 라우터다.

## Canonical Discovery

- 저장소 목적과 Effective Canonical Artifact 목록은 [`README.md`](README.md)에서 확인한다.
- 저장소를 실질적으로 변경하기 전에 [`governance/AI-ENGINEERING-GUIDELINES.md`](governance/AI-ENGINEERING-GUIDELINES.md)를 확인한다.
- 한국어 기술문서를 작성하거나 실질적으로 수정할 때는 [`governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md`](governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md)를 확인한다.
- Failure Reproduction Workflow를 변경할 때는 Definition, 실행 Template과 Conformance Record를 함께 확인한다.
  - [`workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md`](workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md)
  - [`workflows/failure-reproduction/templates/REPRODUCTION-RECORD.md`](workflows/failure-reproduction/templates/REPRODUCTION-RECORD.md)
  - [`workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW-CONFORMANCE.md`](workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW-CONFORMANCE.md)

## Bounded Repository Execution

- 기존 tracked·untracked working-tree 변경을 먼저 확인하고 보존한다.
- 승인된 목표, 경로와 실행 경계 안에서만 변경하고 검증한다.
- 이 파일과 Canonical Artifact가 충돌하면 이 파일로 Governance를 덮어쓰지 말고 충돌과 영향을 보고한다.
