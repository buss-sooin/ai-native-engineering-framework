# 재현 기록(Reproduction Record)

이 Template의 인스턴스는 해당 Project 또는 Task Scope에 저장한다. Template 자체는 Failure Reproduction Workflow의 재사용 가능한 mechanism이며, 적용 규칙은 [`../FAILURE-REPRODUCTION-WORKFLOW.md`](../FAILURE-REPRODUCTION-WORKFLOW.md)를 따른다.

## Record Metadata

- Record ID:
- Project / Task Scope:
- Owner:
- Created At:
- Updated At:
- Workflow Version: Failure Reproduction Workflow v0.1
- Record Status:

## 관찰된 실패(Observed Failure)

- 관찰된 실패(Observed Failure) ID / Reference:
- 관찰 내용:
- 관찰 시점과 환경:
- Source Evidence locator:
- Observation limitations:

## 재현 계약(Reproduction Contract)

- Contract ID:
- 계약 개정(Contract Revision):
- Revision effective point:
- 이전 Revision:
- Revision reason:
- 기존 사람 승인 관문(Human Gate) 경계 안의 변경 여부:

### 정의된 실패 시나리오(Defined Failure Scenario)

- Scenario:
- 관찰된 실패(Observed Failure)와의 관계:

### Scope와 Exclusions

- 포함 Scope:
- Exclusions:
- Prohibited actions:

### Preconditions와 Conditions

- Preconditions:
- Controlled conditions:
- Intentionally varied conditions:

### 실패 징후(Failure Signature)

- Signature 구성 요소:
- 각 구성 요소의 판정 방법:

### Verification Criteria와 Evidence 요구사항

- 실험 유효성(Experiment Validity) criteria:
- 증거 충분성(Evidence Sufficiency) criteria:
- 실패 징후(Failure Signature) evaluation criteria:
- Required Evidence:

### Authorized Execution Boundary

- 허용된 action:
- authority / access 범위:
- Risk / Blast Radius 제한:
- irreversible / high-impact action:
- 기타 경계:

### 사람 승인 관문(Human Gate)

- 사람 승인 관문(Human Gate) 필요 여부:
- Approval reference:
- Authorized approver / authority reference:
- 승인 대상, Scope와 주요 조건:

## 판정 대상 실행(Material Run) 목록

각 판정 대상 실행(Material Run)마다 아래 블록을 복제한다. 하나의 Run에는 하나의 계약 개정(Contract Revision)만 기록한다.

### Run `<Run ID>`

- Run ID:
- Contract ID:
- 계약 개정(Contract Revision):
- 실행 시각:
- 실행 주체:
- 실제 환경과 조건:
- 수행 action:
- Deviation 또는 anomaly:
- 증거 자산(Evidence Assets) locator:
- Evidence integrity 정보(해시, 크기, 생성 시각 등 적용 가능한 값):

## Verification

아래 순서를 바꾸지 않는다.

### 1. 실험 유효성(Experiment Validity)

- 평가:
- 기준별 근거:
- 유효하지 않은 Run과 이유:

### 2. 증거 충분성(Evidence Sufficiency)

- 평가:
- 기준별 근거:
- 누락 또는 제한:

### 3. 실패 징후 평가(Failure Signature Evaluation)

- 평가:
- Signature 구성 요소별 Evidence:
- 부분 충족 또는 불충족 내용:

### 4. Outcome

- Outcome: `<REPRODUCED | PARTIALLY_REPRODUCED | NOT_REPRODUCED | INCONCLUSIVE>`
- Outcome rationale:

`NOT_REPRODUCED`는 유효하고 충분한 실험에서 Signature가 확인되지 않은 경우에만 사용한다. 판정 근거가 부족하면 `INCONCLUSIVE`를 사용한다.

## 검증된 재현 주장(Verified Reproduction Claim)

- Claim:
- Claim을 직접 지지하는 Evidence:
- 적용 환경과 조건:
- Claim limitations:

## Causal Hypotheses

이 항목은 검증 전 가설이며 근본 원인(Root Cause) 판정이 아니다.

- Hypothesis:
- Supporting / contradicting Evidence:
- Verification status:

## 인계(Handoff)

- Contract ID / 계약 개정(Contract Revision):
- 판정 대상 실행(Material Run) references:
- Verified Evidence locators:
- 실험 유효성(Experiment Validity):
- 증거 충분성(Evidence Sufficiency):
- Outcome:
- 검증된 재현 주장(Verified Reproduction Claim):
- Claim limitations:
- Unverified causal hypotheses:
- Unresolved issues:
- Downstream owner / responsibility:

## Record Integrity Checks

- [ ] 관찰된 실패(Observed Failure)와 정의된 실패 시나리오(Defined Failure Scenario)를 구분했다.
- [ ] 판정 대상 실행(Material Run) 전에 Contract, 실패 징후(Failure Signature)와 Verification Criteria를 고정했다.
- [ ] 모든 판정 대상 실행(Material Run)이 정확히 하나의 계약 개정(Contract Revision)을 참조한다.
- [ ] material experiment redesign을 새 계약 개정(Contract Revision)으로 기록했다.
- [ ] approval boundary의 material 변경에 새 사람 승인 관문(Human Gate) 참조가 있다.
- [ ] 실험 유효성(Experiment Validity)을 Outcome보다 먼저 평가했다.
- [ ] 증거 충분성(Evidence Sufficiency)을 실패 징후(Failure Signature)와 Outcome보다 먼저 평가했다.
- [ ] Outcome은 허용된 네 값 중 하나다.
- [ ] `NOT_REPRODUCED`와 `INCONCLUSIVE`를 구분했다.
- [ ] Claim이 Evidence 범위를 넘지 않는다.
- [ ] causal hypothesis를 근본 원인(Root Cause)으로 표현하지 않았다.
- [ ] 증거 자산(Evidence Assets)을 Record 책임과 분리해 참조했다.
- [ ] 인계(Handoff)가 Evidence, Outcome, Claim과 limitations를 보존한다.
