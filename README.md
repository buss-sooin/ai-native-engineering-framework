# AI-Native Engineering Framework

사람과 AI가 함께 소프트웨어를 설계·구현·검증할 때 **누가 무엇을 결정하고 실행하며, 그 결과를 어떤 근거로 검증할지 분명하게 하기 위한** 공통 원칙과 워크플로를 정리한 Framework입니다.

특정 모델이나 도구의 사용법보다 작업의 목적과 필요한 역량을 먼저 파악하고, 사람과 AI의 책임, 실행 권한, 검증 기준을 구분하는 것을 중요하게 다룹니다.

## 개발 흐름

```text
문제와 검증 목표 정의
→ 설계 대안·영향 범위·검증 기준 구체화
→ 중요한 결정과 실행 범위 확정
→ 역할에 맞는 사람·AI 환경에서 구현·실행
→ 실제 결과와 검증 기준 비교
→ 구현 상태와 검증 결과 문서화
```

모든 작업에 이 절차를 똑같이 적용하지는 않습니다. 작은 수정은 필요한 단계만 거치고, 중요한 설계 변경이나 영향 범위가 큰 작업은 실행 전에 목적과 범위, 검증 기준을 분명히 남깁니다.

한 번 정한 범위 안의 반복 작업은 이어서 수행할 수 있지만, 목적이나 위험 범위가 달라지면 다시 판단합니다. 또한 AI가 작업을 완료했다고 보고했다는 이유만으로 구현이나 검증이 끝났다고 판단하지 않고, 실제 결과를 확인해 최종 상태를 결정합니다.

## 사람·AI 협업 원칙

- **책임을 먼저 나눕니다.** 무엇을 결정할지, 누가 실행할지, 어떤 근거로 결과를 검증할지 먼저 구분합니다. 중요한 의사결정과 최종 책임은 사람이 가집니다.
- **작업에 맞는 도구와 환경을 선택합니다.** 설계와 분석, 실제 파일 검토, 코드와 설정 변경, 명령 실행처럼 작업마다 필요한 역량이 다르기 때문에 그 책임에 맞는 사람·AI 환경을 선택합니다.
- **AI가 수행할 범위를 분명히 합니다.** 접근할 수 있는 정보와 변경 범위, 위험 수준을 확인하고, 처음 정한 목적이나 범위를 벗어나면 그대로 진행하지 않고 다시 판단합니다.
- **실행과 검증을 구분합니다.** 작업을 수행한 AI의 완료 보고만으로 성공을 판단하지 않고, 미리 정한 기준과 실제 로그·상태·데이터를 비교해 결과를 확인합니다.
- **중요한 결과를 대화에만 남기지 않습니다.** 확정된 설계, 구현 상태와 검증 결과는 저장소의 문서와 기록에 남겨 다른 사람이나 새로운 AI 세션에서도 같은 기준으로 이어갈 수 있게 합니다.

세부적인 적용 조건과 권한 기준은 [AI Engineering Guidelines](governance/AI-ENGINEERING-GUIDELINES.md)에서 관리합니다.

### 적용 예시

`barcode-ingest-pipeline`에서는 작업의 성격에 따라 AI 환경을 나눠 사용했습니다.

- **ChatGPT 일반 Chat** — 요구사항 분석, 설계, 장애 시나리오 구성과 실행 결과 해석
- **ChatGPT Work mode** — 실제 저장소의 코드·설정·문서 검토와 산출물 비교
- **Codex CLI** — 코드·설정 변경, 명령 실행, 테스트와 Git 작업

중요한 설계 선택이나 결과의 의미처럼 사람이 직접 판단해야 하는 부분은 개발자가 맡았습니다.

이 구성은 `barcode-ingest-pipeline`에서 실제로 사용한 하나의 적용 사례입니다. Framework는 특정 AI 모델이나 제품 조합을 요구하지 않고, **작업에 필요한 책임과 역량에 맞게 역할을 나누는 것**을 원칙으로 합니다.

## 적용 프로젝트

이 Framework를 실제 프로젝트에 적용한 사례입니다.

| 프로젝트 | 적용 목적 | 주요 적용 영역 | 확인 가능한 결과 |
| --- | --- | --- | --- |
| [barcode-ingest-pipeline](https://github.com/buss-sooin/barcode-ingest-pipeline) | 비동기 수집 파이프라인의 성능·데이터 정합성과 운영 장애 대응 검증 | 장애 재현 조건과 판정 기준 설계, 사람·AI 책임 분리, 실행 결과 검토와 문서화 | 성능·정합성 검증 결과, 장애 재현 기록, 기술 문서 |

각 프로젝트의 상세 구현과 검증 결과는 해당 저장소에서 확인할 수 있습니다. 새로운 적용 사례가 생기면 같은 형식으로 추가합니다.

## 문서 안내

Framework의 세부 원칙과 워크플로는 아래 문서에서 확인할 수 있습니다.

| 문서 | 주요 내용 |
| --- | --- |
| [AI Engineering Guidelines](governance/AI-ENGINEERING-GUIDELINES.md) | 사람·AI 협업, 의사결정, 실행 권한과 검증에 대한 공통 원칙 |
| [Technical Documentation Guidelines](governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md) | 한국어 기술 문서의 용어와 표현 기준 |
| [Git Convention](conventions/git/GIT-CONVENTION.md) | 변경 이력과 작업 책임을 분명하게 남기기 위한 Git 사용 기준 |
| [Failure Reproduction Workflow](workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md) | 장애 재현 조건 정의, 실행, 근거 수집과 결과 판정 방법 |
| [Project Collaboration Bootstrap Workflow](workflows/project-collaboration-bootstrap/PROJECT-COLLABORATION-BOOTSTRAP-WORKFLOW.md) | 새 프로젝트에서 사람·AI의 역할과 작업 환경을 정하는 방법 |
| [Post-Incident Analysis Workflow](workflows/post-incident-analysis/POST-INCIDENT-ANALYSIS-WORKFLOW.md) | 장애 이후 근거를 바탕으로 원인과 복구 결과를 분석하는 방법 |

README는 Framework의 전체 방향과 실제 적용 사례를 빠르게 이해하기 위한 시작점이며, 구체적인 규칙과 절차는 각 문서에서 다룹니다.
