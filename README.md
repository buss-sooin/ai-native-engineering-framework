# AI-Native Engineering Framework

사람과 AI가 함께 소프트웨어를 설계·구현·검증할 때 **결정, 실행, 검증의 책임을 분명히 하고 결과를 근거로 설명하기 위한** 공통 원칙과 워크플로를 관리합니다. 특정 모델이나 도구의 사용법보다 작업의 목적, 필요한 역량, 실행 권한과 검증 기준을 먼저 정합니다.

이 저장소의 거버넌스 문서는 `Effective` 상태입니다. 이는 권한 있는 사람의 수용을 거쳐 Framework 수준에 적용된다는 뜻입니다. 각 프로젝트의 기술 선택, 구현 절차와 실행 결과는 해당 프로젝트에서 관리합니다.

## 개발 흐름

```text
문제와 검증 목표 정의
→ 설계 대안·영향 범위·판정 기준 검토
→ 중요한 결정과 실행 경계 승인
→ 적합한 사람·AI 실행 환경에서 구현·실행
→ 실제 결과를 근거와 기준에 대조
→ 구현 상태·검증 결과를 문서에 반영
```

모든 작업에 모든 단계를 같은 무게로 적용하지 않습니다. 중요한 설계나 영향이 큰 변경에는 승인된 의도와 검증 기준을 남기고, 제한된 범위의 후속 실행은 그 경계 안에서 이어갑니다. 조사 결과나 AI의 완료 보고만으로 구현·검증이 끝났다고 판단하지 않습니다.

## 사람·AI 협업 원칙

- **책임을 먼저 나눕니다.** 무엇을 결정하고, 누가 실행하며, 누가 어떤 근거로 검증할지 구분합니다. 최종 책임과 권한은 사람에게 있습니다.
- **작업에 맞는 실행 환경을 선택합니다.** 대화에 제공된 근거만으로 가능한 설계·분석, 실제 파일 검토, 코드·설정 변경과 명령 실행, 사람이 직접 관측해야 하는 작업은 필요한 역량과 책임이 다릅니다. 사용할 수 있다는 사실만으로 선택되거나 승인되지는 않습니다.
- **실행 범위를 제한합니다.** 접근 권한, 데이터 노출, 변경의 영향 범위와 되돌릴 수 있는지를 확인합니다. 중요한 의도·범위·위험이 달라지면 다시 판단합니다.
- **결과를 독립적으로 확인합니다.** 실행 전 판정 기준을 정하고, 로그·상태·데이터 등 실제 근거와 대조합니다. 확인된 범위를 넘는 주장은 하지 않습니다.
- **지속될 결정을 정본에 남깁니다.** 대화 기록은 탐색에 활용하지만, 확정된 설계·구현 상태·검증 결과는 책임에 맞는 저장소 산출물에 반영합니다.

이 원칙의 정확한 적용 조건과 권한 경계는 AI Engineering Guidelines를 따릅니다.

`barcode-ingest-pipeline`에서는 설계·분석에 ChatGPT 일반 Chat, 실제 저장소와 문서 검토에 ChatGPT Work mode, 코드·설정 변경과 테스트·Git 작업에 Codex CLI를 사용했습니다. 사람이 직접 관측하거나 판단해야 하는 책임은 별도로 남겼습니다. 이는 해당 프로젝트의 적용 사례이며, 모든 프로젝트에 같은 제품 구성을 요구하는 규칙은 아닙니다.

## 연결 프로젝트

프로젝트를 추가할 때는 **적용 목적 → 주요 적용 영역 → 확인 가능한 산출물** 순서로 한 행에 요약합니다. 프로젝트별 주장과 수치는 해당 저장소의 실제 문서와 근거를 따릅니다.

| 프로젝트 | 적용 목적 | 주요 적용 영역 | 산출물 |
| --- | --- | --- | --- |
| [barcode-ingest-pipeline](https://github.com/buss-sooin/barcode-ingest-pipeline) | 비동기 수집 파이프라인의 성능·정합성과 제한된 운영 장애의 영향·복구 검증 | 장애 재현 조건과 판정 기준 설계, 실행 책임 분리, 결과 검토와 문서화 | 프로젝트 README의 성능·정합성 검증, 검증 브랜치의 장애 재현 기록·기술 문서 |

연결 프로젝트가 늘어나면 같은 네 열을 유지하고, 상세 구현이나 실험 이력은 각 프로젝트의 문서로 연결합니다.

## 문서 안내

| 문서 | 다루는 책임 |
| --- | --- |
| [AI Engineering Guidelines](governance/AI-ENGINEERING-GUIDELINES.md) | Framework 수준의 사람·AI 협업, 권한, 의사결정과 검증 원칙 |
| [Technical Documentation Guidelines](governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md) | 한국어 기술문서의 용어·표현 기준 |
| [Git Convention](conventions/git/GIT-CONVENTION.md) | 변경 책임을 드러내는 커밋과 공개 이력 관리 |
| [Failure Reproduction Workflow](workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md) | 장애 재현의 설계·실행·근거·판정 |
| [Project Collaboration Bootstrap Workflow](workflows/project-collaboration-bootstrap/PROJECT-COLLABORATION-BOOTSTRAP-WORKFLOW.md) | 프로젝트의 AI 역량·협업 경계 설정 |
| [Post-Incident Analysis Workflow](workflows/post-incident-analysis/POST-INCIDENT-ANALYSIS-WORKFLOW.md) | 장애 이후 원인 분석과 학습 |

세부 규칙과 상태는 각 문서가 관리합니다. README는 처음 방문한 사람이 목적과 적용 사례를 찾는 진입점입니다.
