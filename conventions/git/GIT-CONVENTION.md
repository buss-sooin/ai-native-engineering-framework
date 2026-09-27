# Git Convention

Status: Effective

## 목적과 책임 경계

이 문서는 AI-Native Engineering Framework 아래에서 사람과 AI agent가 commit을 설계하고 공개 branch에 변경을 통합할 때 적용하는 공통 Git 형상 관리 규칙을 정의한다.

Commit history가 제3자에게 변경의 책임, 인과관계와 검증 경계를 설명할 수 있도록 하는 것이 목적이다. 특정 repository의 과거 commit 제목이나 내부 작업 절차를 복제하지 않는다.

이 문서는 branch 전략, merge 방식, release 절차 또는 review workflow를 새로 정의하지 않는다. 적용 대상 repository에 이 문서보다 엄격한 규칙이 있으면 그 규칙을 우선한다. 상위 Authority 또는 repository 규칙과 충돌하면 임의로 통합하지 않고 충돌을 보고한다.

이 문서는 [`AI-ENGINEERING-GUIDELINES.md`](../../governance/AI-ENGINEERING-GUIDELINES.md)의 권한, 실행 경계와 검증 원칙을 따르며, 한국어 commit 설명은 [`TECHNICAL-DOCUMENTATION-GUIDELINES.md`](../../governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md)의 용어 원칙을 따른다.

## 규칙 분류와 적용 조건

- 범위(Scope): Framework
- 의무(Obligation): Conditional
- 활성화 조건(Activation Condition): commit을 설계·생성하거나 공개 branch에 변경을 선별 통합하는 경우

활성화 조건이 충족되면 commit 책임, 제목, 본문, 공개 이력 경계와 AI agent 요구사항을 적용한다.

## Commit 책임

하나의 commit은 하나의 Git 흐름 단계 또는 독립된 변경 책임을 표현해야 한다. 변경 파일 집합은 제목과 본문에서 설명하는 단일 책임에 응집되어야 한다.

- 공개 범위 변경, 제품 동작, 독립적인 테스트 기반, 빌드·배포 변경을 불필요하게 섞지 않는다.
- 제품 동작과 그 동작을 직접 검증하는 테스트처럼 같은 책임을 완성하는 변경은 하나의 commit에 포함할 수 있다.
- 단순 파일 수가 아니라 변경 이유, 독립적인 검증 가능성, 되돌림 경계와 공개 범위를 기준으로 commit을 분리한다.
- 큰 내부 작업 번호, AI 계획 단계 또는 Chat 단위를 commit 책임으로 사용하지 않는다.
- unrelated change는 사용자 승인 없이 같은 commit에 포함하지 않는다.

## 제목 형식

Commit 제목은 다음 형식을 사용한다.

`<type>(<scope>): <제3자가 이해할 수 있는 구체적인 변경 효과>`

### Type

기본 type은 다음과 같다.

- `feat`: 사용자가 관찰할 수 있는 기능 또는 처리 능력을 추가한다.
- `fix`: 잘못된 동작이나 명시된 위험을 교정한다.
- `build`: build, packaging, image 또는 전달 경계를 변경한다.
- `test`: 제품 동작과 독립적으로 테스트 기반이나 검증 장치를 변경한다.
- `docs`: 문서의 의미나 사용 정보를 변경한다.
- `chore`: 제품 동작에 직접 영향을 주지 않는 유지관리 또는 repository 관리를 수행한다.
- `refactor`: 외부 동작을 의도적으로 바꾸지 않고 내부 구조를 개선한다.

Repository가 추가 type이나 더 엄격한 분류를 정의하면 해당 규칙을 따른다. 편의를 위해 의미가 맞지 않는 type을 선택하지 않는다.

### Scope

`scope`는 변경 책임을 식별할 수 있는 component, subsystem 또는 관리 영역을 사용한다. 파일명이나 내부 작업 번호가 아니라 변경의 책임 경계를 나타내야 한다.

### 변경 효과

제목의 마지막 부분은 명령, 작업 번호 또는 작업 완료 사실이 아니라 실제 시스템 변화나 결과를 설명한다.

- 제목만 읽어도 변경된 component와 동작 또는 관리 효과를 식별할 수 있어야 한다.
- 이전 Chat, 내부 계획서 또는 비공개 문서를 읽어야만 의미를 이해할 수 있는 제목을 사용하지 않는다.
- `수정`, `작업 완료`, `계획 반영`처럼 변화가 드러나지 않는 표현을 단독으로 사용하지 않는다.

## Commit 본문

제3자가 변경의 인과관계와 경계를 이해하는 데 필요하면 본문에 다음 내용을 간결하게 기록한다.

- 문제 또는 기존 위험
- 실제 변경 경계와 동작
- 수행한 검증 방법과 결과
- 의도적으로 제외한 범위

모든 항목을 기계적으로 채우지 않는다. 단순하고 자명한 변경에는 불필요한 본문을 강제하지 않는다.

본문에는 실제 수행하고 확인한 검증 결과만 기록한다. 수행하지 않은 test, build, runtime 검증 또는 review를 암시하지 않는다. 실패하거나 일부만 수행한 검증이 변경 판단에 중요하면 그 상태를 정확히 기록한다.

## 공개 이력 경계(Public History Boundary)

공개 branch의 history와 내부 작업 history는 같은 것으로 가정하지 않는다.

- AI 작업 상태, raw Evidence, 실행 준비 문서와 중간 산출물을 제품 commit에 혼합하지 않는다.
- 내부 validation branch의 history를 public branch의 부모로 연결할지는 적용 repository의 공개 정책과 승인된 통합 경계에 따라 명시적으로 결정한다.
- 공개가 승인된 source, test, configuration과 문서만 새로운 책임 단위로 선별 통합할 수 있다.
- 내부 산출물 자체의 공개가 승인된 목적이면 제품 변경과 분리된 문서 또는 관리 책임으로 commit한다.
- `.gitignore`는 아직 추적하지 않은 경로의 기본 포함을 막을 뿐, 이미 추적된 파일이나 public branch에 연결된 commit history를 숨기거나 제거하지 못한다.

공개 이력을 다시 쓰거나 이미 공개된 정보를 제거하는 행위는 이 문서가 자동으로 승인하지 않는다. 해당 repository의 권한, 위험과 변경 절차를 별도로 따라야 한다.

## AI agent 요구사항

AI agent는 commit 전에 다음 사항을 확인한다.

1. changed-file set이 하나의 commit 책임에 속하는지 검토한다.
2. 제목만으로 component와 실제 동작 또는 관리 효과를 식별할 수 있는지 확인한다.
3. 본문의 검증 설명이 실제 수행 결과와 일치하는지 확인한다.
4. 작업 전부터 존재한 변경이나 현재 책임과 무관한 변경을 사용자 승인 없이 포함하지 않는다.
5. 내부 작업 history와 공개 대상 file set을 구분한다.
6. 적용 repository의 기존 convention이 더 엄격한지 확인하고, 더 엄격하면 기존 규칙을 우선한다.

Commit 생성 권한과 remote push 권한은 별개다. Commit 생성 승인을 remote push 승인으로 해석하지 않는다.

## Attribution 경계

AI attribution은 commit의 책임·제목·본문 규칙과 분리한다. `Claude`, `Codex` 또는 다른 AI의 사용 사실만으로 `Co-authored-by` trailer를 자동 생성하지 않는다.

적용 repository의 attribution policy를 먼저 확인하고 다음 순서로 판정한다.

1. repository policy가 attribution을 필수 또는 금지하면 그 규칙을 따른다.
2. 별도 policy가 없으면 attribution은 선택(Optional)이며, 권한 있는 사용자의 명시적 지시와 확인된 attribution 정보가 있을 때만 추가한다.
3. 이름, email, 기여 사실 또는 사용자의 의사가 확인되지 않으면 attribution을 생성하지 않는다.

이 Framework repository의 canonical document, `AGENTS.md`, `README.md`와 `main` history에는 현재 AI co-author trailer의 필수 또는 금지 정책이 없다. 따라서 이 repository에서는 별도 정책이 생기기 전까지 위 선택 규칙을 적용한다.

## 예시

### 좋은 예

`chore(git): 내부 검증 산출물을 공개 대상에서 제외`

- 공개 범위 관리라는 하나의 책임과 효과가 드러난다.

`fix(worker): Redis PEL 항목을 명시적 ID로 안전하게 회수`

- component, 기존 위험과 교정 효과를 제목만으로 식별할 수 있다.

`feat(processing): DLT 재처리와 격리 경계를 추가`

- 제품 동작과 처리 경계가 구체적이다.

`build(container): Git SHA 기반 이미지 전달 경로를 추가`

- build·배포 책임이 제품 동작 변경과 분리되어 있다.

### 피해야 할 예

`feat(plan-93): 승인된 작업을 구현`

- 내부 작업 번호와 계획을 알아야 의미를 이해할 수 있다.

`fix(worker): 작업 완료`

- 실제로 교정한 동작이나 위험이 드러나지 않는다.

`chore(ai): Codex 결과 반영`

- AI 도구 사용 사실이 변경 책임을 대신한다.

`feat(processing): DLT 수정과 문서 및 배포 작업`

- 서로 독립적으로 검증·되돌릴 수 있는 책임을 한 제목에 섞는다.

검증하지 않은 상태에서 본문에 `모든 테스트 통과`라고 기록하는 것도 금지한다. 검증을 수행하지 않았다면 생략하거나 수행하지 않았음을 정확히 기록한다.

## Commit 전 확인

- changed-file set이 한 책임으로 설명되는가
- 제목이 정해진 형식과 type·scope 의미를 따르는가
- 제목만으로 component와 변경 효과가 드러나는가
- 본문이 필요한 인과관계, 검증과 제외 범위만 정확히 설명하는가
- 내부 산출물과 공개 대상이 분리되었는가
- `.gitignore`를 history 제거 수단으로 오해하지 않았는가
- attribution policy와 실제 attribution 정보가 확인되었는가
- commit과 push의 권한 경계를 각각 확인했는가
