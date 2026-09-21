# Failure Reproduction Workflow v0.1

Status: Effective

Effective Date: 2026-08-28

## 목적과 Governance 위치

이 문서는 관찰된 실패(Observed Failure)를 통제된 조건에서 재현하고 검증 가능한 근거와 함께 후속 작업으로 인계(Handoff)하기 위한 Workflow-level Canonical Definition이다. 상위 Authority는 [`../../governance/AI-ENGINEERING-GUIDELINES.md`](../../governance/AI-ENGINEERING-GUIDELINES.md)이며, 이 Workflow는 해당 Effective Framework Governance를 구체화하되 변경하지 않는다.

Workflow 책임은 다음으로 한정한다.

`Define → Reproduce → Verify → 인계(Handoff)`

종료점은 `Verified Reproduction`이다. 근본 원인(Root Cause) 판정, Remediation, production change, Engineering Report 작성 방식과 Portfolio README 작성 방식은 이 Workflow의 책임이 아니다.

## Scope

이 Workflow는 기술과 Project에 독립적으로 반복 가능한 실패 재현 방법과 협업 규칙을 정의한다. 구체적인 기술 topology, fault injection, monitoring 구현과 개별 실패 Scenario는 Project 또는 Task Scope에 둔다. 하나의 Project 또는 Task에서 생성하는 재현 기록(Reproduction Record)은 해당 Project 또는 Task에 속하고, 재사용 가능한 Workflow Definition과 Template만 이 위치에서 관리한다.

## 용어

- **관찰된 실패(Observed Failure)**: 로그, 측정값, 사용자 보고 또는 시스템 상태 같은 Evidence에서 직접 관찰된 실패 현상이다.
- **정의된 실패 시나리오(Defined Failure Scenario)**: 재현을 위해 Scope, 조건과 기대되는 실패 표현을 명시한 실행 가능한 Scenario다. 관찰된 실패 자체와 동일시하지 않는다.
- **재현 계약(Reproduction Contract)**: 판정 대상 실행(Material Run) 전에 고정하는 실행·검증 경계다.
- **계약 개정(Contract Revision)**: 특정 재현 계약 상태를 식별하는 변경 단위다.
- **판정 대상 실행(Material Run)**: 결과가 재현 Outcome 또는 검증된 재현 주장(Verified Reproduction Claim)의 근거가 될 수 있는 실행이다. 예비 탐색이 Claim 근거로 사용되는 순간 해당 실행도 판정 대상 실행으로 취급한다.
- **실패 징후(Failure Signature)**: 실패가 발생했다고 판정하기 위해 Evidence에서 확인할 식별 가능한 특징이다.
- **검증 기준(Verification Criteria)**: 실험 유효성(Experiment Validity), 증거 충분성(Evidence Sufficiency)과 실패 징후 충족 여부를 판단하는 사전 고정 기준이다.
- **실험 유효성(Experiment Validity)**: 실행이 계약 개정의 조건과 경계를 충족하여 Outcome 평가에 사용할 수 있는지에 대한 판정이다.
- **검증된 재현 주장(Verified Reproduction Claim)**: 검증된 Evidence가 직접 지지하는 범위 안에서만 작성한 재현 주장이다.
- **증거 자산(Evidence Assets)**: 로그, 측정값, 캡처, 명령 출력과 환경 정보 등 Record가 참조하는 원자료다.

## Canonical Lifecycle

`Define → Reproduce → Verify → 인계(Handoff)`

1. **Define**: 관찰된 실패와 정의된 실패 시나리오를 구분하고 재현 계약을 고정한다.
2. **Reproduce**: 승인된 실행 경계 안에서 계약 개정에 추적 가능한 판정 대상 실행을 수행하고 Evidence를 보존한다.
3. **Verify**: `실험 유효성(Experiment Validity) → 증거 충분성(Evidence Sufficiency) → 실패 징후 평가(Failure Signature Evaluation) → Outcome` 순서로 평가한다.
4. **인계(Handoff)**: Verified Evidence, Outcome, 검증된 재현 주장과 Claim limitations를 후속 책임자에게 전달한다.

Completion은 하나 이상의 판정 대상 실행에 대해 위 검증 순서를 완료하고, 허용된 Outcome을 기록하며, Evidence와 Claim 경계를 보존한 인계를 만들었을 때 성립한다. Evidence가 부족하거나 실험이 유효하지 않아도 `INCONCLUSIVE` Outcome과 그 근거를 기록하면 Workflow 자체는 종료할 수 있다.

## 재현 계약(Reproduction Contract)

판정 대상 실행 전에 다음 항목을 적용 가능한 범위에서 고정한다.

- Contract ID와 계약 개정(Contract Revision)
- 관찰된 실패(Observed Failure) 참조
- 정의된 실패 시나리오(Defined Failure Scenario)
- Scope와 Preconditions
- 통제할 조건과 의도적으로 변화시킬 조건
- 실패 징후(Failure Signature)
- Verification Criteria와 Evidence 요구사항
- authorized execution boundary
- exclusions와 prohibited actions
- 필요한 사람 승인 관문(Human Gate) 참조

실패 징후와 Verification Criteria는 관련 판정 대상 실행 전에 고정해야 한다. 모든 판정 대상 실행은 정확히 하나의 식별 가능한 계약 개정에 속해야 하며, Run Record가 해당 Revision을 직접 참조해야 한다.

## 실행 경계와 계약 개정(Contract Revision)

권한 있는 사람 승인 관문(Human Gate)이 경계를 승인한 경우 다음 실행을 허용한다.

`Approved Boundary → Bounded Autonomous Execution → Verify → Record`

이미 승인된 경계 안의 정상 실행에는 반복 사람 승인 관문을 요구하지 않는다. 조건, 절차, 실패 징후, Verification Criteria 또는 Evidence 요구사항의 material한 experiment redesign은 새 계약 개정으로 기록한다.

새 계약 개정 생성 자체가 항상 새 사람 승인 관문을 뜻하지는 않는다. 다음과 같이 approval boundary가 material하게 바뀔 때 새 사람 승인 관문이 필요하다.

- 승인된 Engineering Intent 또는 Scope 변경
- authority 또는 access 확대·변경
- Risk 또는 Blast Radius의 의미 있는 증가
- irreversible 또는 high-impact action 추가
- approved execution boundary 변경

승인 경계를 바꾸지 않는 Revision은 기존 승인 참조와 경계 안에서 실행할 수 있다. 경계 변경 여부가 불명확하면 판정 대상 실행을 중단하고 Human Resolution을 요청한다.

### 제한된 후속 실행 묶음(Grouped Bounded Continuation)

생명주기 상태 경계(Lifecycle State Boundary)와 사람 승인 관문 경계(Human Gate Boundary)는 구분한다. 생명주기 상태 전환 자체가 새 사람 승인 관문을 만들지는 않는다. 다음 내용은 FRW-R09의 승인 경계 내 실행 허용과 FRW-R11의 승인 경계 변경 시 승인 요구를 운영상 구체화한다.

이미 승인된 실행 경계 안에서 다음 전제조건이 모두 유지되면 결정적이고 범위가 제한된 후속 작업을 하나의 제한된 후속 실행 묶음으로 수행할 수 있다.

- 이전 단계의 PASS가 다음 단계의 사전조건을 충족한다는 관계가 명시되어 있다.
- 후속 작업의 수행 내용이 결정적이며 범위가 제한되어 있다.
- 엔지니어링 의도(Engineering Intent)가 변경되지 않는다.
- 범위(Scope)가 확대되지 않는다.
- 권한 또는 접근 범위(authority / access)가 확대되지 않는다.
- 위험(Risk) 또는 영향 범위(Blast Radius)가 의미 있게 증가하지 않는다.
- 새로운 비가역적·파괴적·고영향 작업이 추가되지 않는다.
- 중요한 설계 결정이 새로 도입되지 않는다.
- 승인된 설계나 실행 경계에서 중요한 이탈(material deviation)이 없다.
- 검증 기준(Verification Criteria), 수락 기준(acceptance criteria)과 주장 경계(Claim Boundary)가 변경되지 않는다.
- 해결되지 않은 권한 충돌이나 정본 충돌(authority or canonical conflict)이 없다.

후속 실행 묶음은 기존 승인 참조와 승인 대상·범위·조건을 유지한다. 각 생명주기 상태와 적용 가능한 검증·동기화·종료 결과는 묶음 안에서도 개별적으로 식별하고 재현 기록 또는 그에 연결된 실행·검증 근거에 기록한다. 단계의 PASS는 해당 단계의 사전 기준 충족을 나타내며 재현 Outcome을 대체하지 않는다. 동기화와 종료 결과의 기록은 `Define → Reproduce → Verify → 인계(Handoff)`에 새로운 생명주기 상태를 추가하지 않는다.

전제조건이 더 이상 유지되지 않거나 승인 경계가 실질적으로 변경되면 후속 실행을 중단한다. 전제조건이 충족되지 않거나 충족 여부·경계가 불명확하거나 충돌이 있으면 사람의 판단과 해결(Human Resolution)을 요청하고, 승인 경계의 실질적 변경에는 FRW-R11에 따라 새 사람 승인 관문을 거친다. 전제조건 미충족 자체를 승인 경계 변경으로 간주하지 않는다.

Project별 협업 규칙이나 권한 제약은 허용되는 후속 실행 범위를 더 좁힐 수 있으며 이 Workflow로 해당 제약을 우회할 수 없다. 원격 또는 비로컬 동기화는 그 작업 자체가 이미 승인된 실행 경계에 포함되어 있을 때만 후속 실행 묶음에 포함할 수 있다. 이 구체화를 근거로 과거 승인 범위를 소급하여 확대하지 않는다.

## 실험 유효성(Experiment Validity), 증거 충분성(Evidence Sufficiency)과 Outcome

검증은 반드시 다음 순서를 따른다.

`실험 유효성(Experiment Validity) → 증거 충분성(Evidence Sufficiency) → 실패 징후 평가(Failure Signature Evaluation) → Outcome`

- 실험 유효성이 확인되기 전에 Outcome을 배정하지 않는다.
- 증거 충분성은 사전에 정의된 Evidence 요구사항과 Verification Criteria를 기준으로 평가한다.
- 실패 징후 평가는 고정된 Signature의 충족, 부분 충족 또는 불충족을 Evidence에 연결한다.
- Outcome은 다음 네 값 중 하나만 사용한다.

  - `REPRODUCED`
  - `PARTIALLY_REPRODUCED`
  - `NOT_REPRODUCED`
  - `INCONCLUSIVE`

`NOT_REPRODUCED`는 유효하고 충분한 실험에서 정의된 실패 징후가 확인되지 않았음을 뜻한다. `INCONCLUSIVE`는 실험 유효성, 증거 충분성 또는 판정 가능성이 부족하여 재현 여부를 결론낼 수 없음을 뜻한다. 두 Outcome은 서로 대체할 수 없다.

검증된 재현 주장(Verified Reproduction Claim)은 Evidence가 직접 지지하는 환경, 조건, 범위와 관찰까지만 진술한다. 일부 Signature만 확인되면 그 제한을 명시한다. causal hypothesis는 별도 causal verification 없이 근본 원인(Root Cause)으로 승격하지 않는다.

## Artifact Boundary

다음 책임을 분리한다.

1. **Workflow Definition**: 반복 적용할 방법, 규칙, lifecycle과 책임 경계를 정의한다.
2. **재현 기록(Reproduction Record)**: 특정 Project 또는 Task의 계약 개정(Contract Revision), Run, 검증, Outcome과 인계(Handoff)를 기록한다.
3. **증거 자산(Evidence Assets)**: Record가 참조하는 원자료를 보존한다.

재현 기록 Template은 [`templates/REPRODUCTION-RECORD.md`](templates/REPRODUCTION-RECORD.md)에서 관리한다. 증거 자산은 Record 본문에 복제하는 대신 안정적인 Project/Task locator와 무결성 정보로 참조하는 것을 우선한다. Engineering Report와 Portfolio README는 downstream Communication Artifact이며 이 Workflow는 그 작성 형식을 정의하지 않는다.

## 인계 계약(Handoff Contract)

인계에는 최소한 다음을 보존한다.

- 사용한 Contract ID와 계약 개정(Contract Revision)
- 판정 대상 실행(Material Run) 및 Verified Evidence locator
- 실험 유효성(Experiment Validity)과 증거 충분성(Evidence Sufficiency) 결과
- 네 값 중 하나인 Outcome
- 검증된 재현 주장(Verified Reproduction Claim)
- Claim limitations
- 미검증 causal hypotheses가 있다면 그 상태와 근거
- 후속 책임 범위와 unresolved issue

인계는 근본 원인(Root Cause), Remediation 또는 production change를 선언하지 않는다. 후속 Workflow가 이 Evidence를 사용하더라도 해당 Workflow의 별도 검증과 Authority를 따라야 한다.

검증된 재현 인계(Verified Reproduction Handoff)는 필요한 경우 Effective [Post-Incident Analysis Workflow](../post-incident-analysis/POST-INCIDENT-ANALYSIS-WORKFLOW.md)의 입력으로 사용할 수 있다. 이는 선택 가능한 downstream navigation이며 Failure Reproduction Workflow의 생명주기, Outcome, 완료 조건 또는 책임 범위를 변경하지 않는다.

## Rules와 Obligations

| Rule ID | Rule | Obligation | Activation condition |
| --- | --- | --- | --- |
| FRW-R01 | Workflow 책임을 `Define → Reproduce → Verify → 인계(Handoff)`로 제한한다. | Mandatory | 항상 |
| FRW-R02 | 관찰된 실패(Observed Failure)와 정의된 실패 시나리오(Defined Failure Scenario)를 구분한다. | Mandatory | 항상 |
| FRW-R03 | 판정 대상 실행(Material Run) 전에 재현 계약(Reproduction Contract), 실패 징후(Failure Signature)와 Verification Criteria를 고정한다. | Mandatory | 판정 대상 실행(Material Run) 수행 시 |
| FRW-R04 | 모든 판정 대상 실행(Material Run)을 하나의 식별 가능한 계약 개정(Contract Revision)에 연결한다. | Mandatory | 항상 |
| FRW-R05 | Outcome 배정 전에 실험 유효성(Experiment Validity)을 평가한다. | Mandatory | 항상 |
| FRW-R06 | Outcome은 `REPRODUCED`, `PARTIALLY_REPRODUCED`, `NOT_REPRODUCED`, `INCONCLUSIVE`만 사용한다. | Mandatory | 항상 |
| FRW-R07 | 검증된 재현 주장(Verified Reproduction Claim)을 이용 가능한 Evidence 범위 밖으로 일반화하지 않는다. | Mandatory | 항상 |
| FRW-R08 | 별도 검증 없이 causal hypothesis를 근본 원인(Root Cause)으로 승격하지 않는다. | Mandatory | 항상 |
| FRW-R09 | 승인된 재현 경계 안에서 제한된 자율 실행(Bounded Autonomous Execution)을 허용하며, 명시된 모든 전제조건이 유지되는 후속 작업은 기존 승인 참조를 유지하는 제한된 후속 실행 묶음(Grouped Bounded Continuation)으로 수행할 수 있다. | Mandatory | 승인된 경계가 존재할 때 |
| FRW-R10 | material experiment redesign마다 새 계약 개정(Contract Revision)을 만든다. | Mandatory | 항상 |
| FRW-R11 | 승인 경계를 실질적으로 변경하는 재설계에는 새 사람 승인 관문(Human Gate)을 요구한다. 생명주기 상태 전환 자체는 새 승인 관문을 만들지 않으며, 후속 실행 전제조건 미충족이나 승인 경계의 실질적 변경 시 실행을 중단하고 해당 사유에 따라 사람의 판단과 해결(Human Resolution) 또는 새 사람 승인 관문으로 전환한다. | Conditional | 승인된 Intent, Scope, authority/access, Risk, Blast Radius, irreversible/high-impact action 또는 execution boundary의 material 변경 |
| FRW-R12 | Workflow Definition, 재현 기록(Reproduction Record)과 증거 자산(Evidence Assets)의 책임을 분리한다. | Mandatory | 항상 |
| FRW-R13 | 인계(Handoff)에 Verified Evidence, Outcome, 검증된 재현 주장(Verified Reproduction Claim)과 Claim limitations를 보존한다. | Mandatory | 항상 |
| FRW-R14 | Engineering Report와 Portfolio README 작성 형식을 Workflow 밖에 둔다. | Mandatory | 항상 |
| FRW-R15 | 기술별 재현 구현을 별도 Governance 근거 없이 Workflow-level Rule로 일반화하지 않는다. | Mandatory | 항상 |

## 최소 Enforcement 전략

- 판정 대상 실행 시작 전 재현 기록의 Contract, 실패 징후, Verification Criteria와 사람 승인 관문 조건을 검토한다.
- Run마다 계약 개정 참조가 정확히 하나 존재하는지 확인한다.
- 검증 표에서 단계 순서와 허용 Outcome vocabulary를 확인한다.
- Evidence locator와 Claim 문장을 대조하여 일반화 범위를 검토한다.
- 인계 전 Artifact Boundary와 causal hypothesis 상태를 점검한다.

자동화는 반복 사용에서 필요성과 비용이 검증될 때 별도 제안한다. 이 Effective Workflow는 특정 자동화나 기술 구현을 Mandatory Enforcement Mechanism으로 지정하지 않는다.

## 완료 기준

- 관찰된 실패와 정의된 실패 시나리오가 분리되어 있다.
- 적용한 재현 계약과 계약 개정이 식별 가능하다.
- 각 판정 대상 실행이 하나의 계약 개정에 추적 가능하다.
- 검증이 정해진 순서로 수행되었다.
- Outcome이 허용된 네 값 중 하나다.
- Verified Evidence, Claim과 limitations가 서로 정합하다.
- causal hypothesis가 근본 원인과 구분되어 있다.
- Workflow Definition, 재현 기록과 증거 자산의 책임이 분리되어 있다.
- 인계가 필수 정보를 보존한다.
