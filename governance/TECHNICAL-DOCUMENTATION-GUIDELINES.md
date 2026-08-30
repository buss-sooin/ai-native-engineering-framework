# Technical Documentation Guidelines

Status: Effective

## 목적

이 문서는 AI-Native Engineering Framework 아래에서 새로 작성하거나 실질적으로 수정하는 한국어 기술 산출물의 용어와 표현을 일관되게 관리하기 위한 프레임워크(Framework) 수준의 조건부 거버넌스(Conditional Governance)를 정의한다.

한국어 설명만으로 핵심 개념을 이해할 수 있게 하면서 원래 영어 기술 용어와의 대응 관계, 공식 식별자와 기술적 정확성을 보존하는 것이 목적이다. 이 규칙은 영어를 제거하거나 모든 기술 요소를 번역하기 위한 것이 아니다.

## 적용 범위

이 문서는 Framework, Workflow, Project 또는 Task에서 새로 작성하거나 실질적으로 수정하는 다음 한국어 기술 산출물에 적용한다.

- Governance와 Workflow 정의
- Project 설계와 Architecture 문서
- 장애 재현 기록, 운영 진단 가이드와 런북
- 기술 보고서와 README
- Template의 한국어 설명과 필드
- 그 밖에 Framework 아래에서 작성하는 한국어 기술 설명

저장소 문서뿐 아니라 적용 중인 Framework 작업에서 생성하는 한국어 기술 설명도 같은 활성화 조건을 충족하면 범위에 포함한다.

## 규칙 분류와 의무

- 범위(Scope): Framework
- 의무(Obligation): Conditional
- 활성화 조건(Activation Condition): Framework 아래에서 한국어 기술 산출물을 새로 작성하거나 기존 한국어 기술 산출물을 실질적으로 수정하는 경우

활성화 조건이 충족되면 이 문서의 용어 분류, 식별자 보존과 문서 수준 일관성 규칙을 반드시 적용한다. 영어 기술 산출물, 단순 조회, 내용 변화가 없는 형식 정리 또는 인용한 원문의 표기에는 한국어 우선 표기를 강제하지 않는다.

## 비목표

이 문서는 다음 책임을 정의하거나 변경하지 않는다.

- Engineering 실행 절차, Architecture 설계 또는 Workflow 동작
- 개별 기술의 구현 방법과 제품 선택
- README, 기술 보고서 또는 런북의 별도 작성 Workflow
- 문서 생명주기, 승인 절차 또는 새로운 Enforcement Mechanism
- 증거 품질(Evidence Quality), 증거 수집 또는 검증 충분성에 관한 새로운 의무
- 공식 식별자, 상태 값, Rule ID 또는 역사적 승인 기록의 변경

## 용어 분류 우선순위

용어가 둘 이상의 분류에 해당할 수 있으면 다음 우선순위로 판정한다.

1. 공식 식별자(Official Identifier)
2. 제품·기술·표준 약어·프로토콜(Product / Technology / Standard Acronym / Protocol)
3. Framework 또는 Workflow에서 정의한 파생 정식 용어(Framework / Workflow Derived Formal Term)
4. 자연스럽게 번역할 수 있는 핵심 기술 개념(Naturally Translatable Core Technical Concept)
5. 한국 개발 현장에서 자연스러운 외래어(Natural Korean Developer Loanword)

상위 분류의 보존 규칙은 하위 분류의 한국어 표기 규칙보다 우선한다. 분류가 불명확하고 번역이 의미를 넓히거나 좁힐 가능성이 있으면 원문을 유지하고 설계 후속 검토 대상으로 보고한다.

## 공식 식별자 보존

실행, 검색, 관측, 상호운용 또는 추적에 사용하는 공식 식별자는 번역하거나 철자, 대소문자, 구분자를 임의로 변경하지 않는다. 한국어 설명이 필요하면 식별자와 분리해 추가한다.

다음과 같은 값은 원문을 정확히 보존한다.

- Rule ID: `FRW-R01`, `FRW-R15`
- 상태와 Outcome 값: `REPRODUCED`, `PARTIALLY_REPRODUCED`, `NOT_REPRODUCED`, `INCONCLUSIVE`
- 명령과 프로토콜 식별자: `XACK`
- API 이름, class 이름, method 이름과 코드 식별자
- configuration key와 CLI 명령
- log field 이름과 metric identifier
- repository path와 외부 시스템 locator

공식 식별자가 제품명이나 기술 용어와 겹치더라도 공식 식별자 보존 규칙을 먼저 적용한다.

## 제품·기술·표준 약어·프로토콜

제품명, 기술명, 표준 약어와 프로토콜명은 국내 개발 현장에서 통용되는 원문을 유지한다. 예를 들어 Kafka, Redis, MySQL, Spring Boot, Prometheus, Grafana, DLQ, DLT, PEL과 API는 기계적으로 번역하지 않는다.

설명이 필요하면 원문을 바꾸지 않고 별도의 한국어 설명을 덧붙인다. 표준 약어의 공식 확장형이 독자의 이해에 필요하면 최초 사용이나 정의 위치에 함께 제시할 수 있다.

## Framework·Workflow 파생 정식 용어

Framework 또는 Workflow에서 특정 의미로 정의한 파생 정식 용어는 `한국어 표현(English Term)` 형식으로 대응 관계를 명확히 한다. 공식 정의, 중요한 최초 사용, 독립적으로 읽는 규칙 표와 의미 대응이 중요한 Template 필드에서는 한국어와 영어를 함께 쓴다.

| English Term | 승인된 한국어 표기 |
| --- | --- |
| Human Gate | 사람 승인 관문(Human Gate) |
| Failure Domain | 장애 영역(Failure Domain) |
| Recovery Complete | 복구 완료(Recovery Complete) |
| Observed Failure | 관찰된 실패(Observed Failure) |
| Defined Failure Scenario | 정의된 실패 시나리오(Defined Failure Scenario) |
| Reproduction Contract | 재현 계약(Reproduction Contract) |
| Contract Revision | 계약 개정(Contract Revision) |
| Material Run | 판정 대상 실행(Material Run) |
| Failure Signature | 실패 징후(Failure Signature) |
| Experiment Validity | 실험 유효성(Experiment Validity) |
| Evidence Sufficiency | 증거 충분성(Evidence Sufficiency) |
| Verified Reproduction Claim | 검증된 재현 주장(Verified Reproduction Claim) |
| Evidence Assets | 증거 자산(Evidence Assets) |
| Root Cause | 근본 원인(Root Cause) |
| Handoff | 인계(Handoff) |

영어 병기는 대응 관계를 식별하기 위한 것이며 모든 문장에서 반복할 필요는 없다. 정의 후에는 같은 문서에서 선택한 한국어 표현을 일관되게 사용한다.

## 자연스럽게 번역할 수 있는 핵심 기술 개념

한국어로 자연스럽고 정확하게 설명할 수 있는 핵심 기술 개념은 중요한 최초 사용이나 정의에서 `한국어 표현(English Term)` 형식을 우선한다.

| English Term | 승인된 한국어 표기 |
| --- | --- |
| Consumer Lag | 소비자 지연(Consumer Lag) |
| Idempotency | 멱등성(Idempotency) |
| Retry | 재시도(Retry) |
| Observability | 관측 가능성(Observability) |

`Consumer Lag`는 제품명이나 공식 식별자가 아니라 자연스럽게 번역할 수 있는 핵심 기술 개념으로 분류한다. 따라서 한국어 기술 설명에서는 소비자 지연(Consumer Lag)으로 표기한다.

번역이 기술적 의미를 왜곡하거나 국내 개발 현장의 일반적인 용례와 크게 어긋나면 추측해 새 번역을 만들지 않는다. 원문을 유지하고 필요한 한국어 설명을 분리해 제공한다.

## 한국 개발 현장의 자연스러운 외래어

한국 개발 현장에서 한글 외래어 사용이 자연스럽고 의미가 분명한 용어는 억지로 번역하거나 영어로 되돌리지 않는다.

- 백로그
- 오프셋
- 커밋

자연스러운 한국어 기술 표현이 있는 경우에는 어색한 음역을 피한다. 예를 들어 `Retry`는 재시도(Retry)로 표기한다.

## 문서 수준 일관성

한 문서에서는 같은 개념에 하나의 표기를 사용한다. 공식 정의, 중요한 최초 사용, 독립적으로 읽는 표와 의미 대응이 중요한 Template 필드에서는 한국어와 영어를 병기하고, 그 뒤에는 문맥이 명확한 범위에서 승인된 한국어 표현을 사용할 수 있다.

다음 원칙을 함께 적용한다.

- 서로 다른 한국어 번역을 같은 Formal Term에 혼용하지 않는다.
- 영어 병기를 모든 문장에 기계적으로 반복하지 않는다.
- 공식 식별자와 자연어 설명을 구분한다.
- 용어 정규화 과정에서 modal 의미, 부정, 활성화 조건, 순서, 책임 주체, Rule ID, 상태 값, 경로와 역사 기록을 변경하지 않는다.
- 번역이 기존 의미를 넓히거나 좁히면 해당 변경을 중단하고 설계 후속 검토 대상으로 보고한다.

## 전환 정책(Migration Policy)

### A. 새 산출물(New Artifact)

활성화 조건을 충족하는 새 산출물은 작성 시점부터 이 문서를 준수한다.

### B. 실질적으로 수정한 산출물(Materially Modified Artifact)

변경한 구역과 그 구역의 의미를 직접 지지하는 정의, 규칙 표와 Template 필드를 함께 정규화한다. 변경과 무관한 legacy 문구를 기계적으로 전면 수정하지 않는다.

### C. 기존 Effective 산출물(Existing Effective Artifact)

이 문서가 도입되었다는 이유만으로 기존 Effective 산출물을 Invalid로 간주하지 않는다. 기존 산출물의 용어는 계획된 정규화 대상으로 관리하며, 승인 상태와 기존 의미는 유지한다.

### D. 정규화 집합(Normalization Set)

같은 파생 정식 용어를 공유하는 Workflow Definition과 실행 Template은 하나의 의미 집합으로 정규화한다. Conformance 이력은 현재 용어 표기를 정규화할 수 있지만 당시의 검토 결과, 승인 대상, 승인 범위, 승인 일자와 PASS / FAIL 사실을 역사적으로 정확하게 보존해야 한다.

## 기존 Effective 산출물 처리

기존 Effective 산출물의 용어 차이는 그 자체로 Governance 위반이나 효력 상실을 의미하지 않는다. 다음 material 변경 시 관련 구역을 정규화하거나 별도의 승인된 정규화 작업에서 처리한다.

정규화는 문서 의미를 보존하는 편집이다. 기존 규칙의 Scope, Obligation, 활성화 조건, 책임, 순서 또는 승인 사실을 변경해야 한다면 용어 정규화로 처리하지 않고 해당 Governance의 Change Control을 따른다.

## 적합성 기대사항

활성화 조건을 충족하는 산출물은 검토 시 다음을 확인한다.

- 용어 분류 우선순위를 적용했다.
- 공식 식별자와 제품·기술·약어·프로토콜 원문을 보존했다.
- Framework·Workflow 파생 정식 용어와 자연스럽게 번역할 수 있는 핵심 기술 개념에 승인된 대응 표기를 사용했다.
- 한국 개발 현장의 자연스러운 외래어와 문서 수준 일관성 규칙을 지켰다.
- 전환 정책에 따라 변경 범위를 정규화하고 기존 Effective 상태와 역사 기록을 보존했다.
- 의미 보존이 불확실한 변경은 적용하지 않고 충돌 또는 설계 후속 검토 대상으로 보고했다.

이 적합성 검토는 용어·표현과 의미 보존만을 대상으로 한다. 새로운 증거 품질, 증거 수집 또는 Workflow 검증 의무를 추가하지 않는다.
