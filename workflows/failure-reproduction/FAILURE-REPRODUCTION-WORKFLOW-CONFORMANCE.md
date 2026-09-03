# Failure Reproduction Workflow v0.1 Governance Conformance Record

Review Disposition: Passed

Reviewed Workflow Status: Effective

## 검토 대상과 Authority

- Reviewed Workflow: [`FAILURE-REPRODUCTION-WORKFLOW.md`](FAILURE-REPRODUCTION-WORKFLOW.md)
- Workflow Version: Failure Reproduction Workflow v0.1
- Parent Governance: [`../../governance/AI-ENGINEERING-GUIDELINES.md`](../../governance/AI-ENGINEERING-GUIDELINES.md), Status: Effective
- Scope Classification: Workflow
- Canonicalization Repository: `ai-native-engineering-framework`

이 Record는 승인된 Workflow Design의 repository canonicalization, Effective Framework Governance conformance와 권한 있는 Human의 Acceptance 결과를 기록한다. AI는 승인 주체가 아니며 Human Acceptance를 대신하지 않았다.

## Human Acceptance

- Acceptance Date: 2026-08-28
- Approved Target: Failure Reproduction Workflow v0.1
- Approved Transition: `Draft → Effective`
- Approved Scope: 승인된 Workflow Design의 canonicalization과 non-material Obligation traceability 정규화
- Approver Authority: 이 개인 repository와 project에 대한 권한 있는 Human authority
- Acceptance Source: 권한 있는 Human이 명시적으로 제공한 승인 지시

Canonical Artifact Review는 PASS했고 material design deviation은 발견되지 않았다. 승인 전 확인된 유일한 issue는 Conformance Record가 일부 Mandatory Rule의 활성화 조건을 Obligation 값에 결합한 non-material traceability 표현이었다. 승인 범위에 따라 이를 Foundation vocabulary와 분리된 Activation condition으로 정규화했으며 Rule의 Scope, Obligation 또는 활성화 의미는 변경하지 않았다.

### Design 53 후속 정본화(Canonicalization)

- Approved Design: Design 53 — Failure Reproduction Workflow Grouped Bounded Continuation Canonicalization
- Approval reference: 권한 있는 Human이 제공한 `# 53 — FRW Grouped Bounded Continuation Canonicalization Execution`의 Design 53 사람 승인 관문(Human Gate) `PASSED` 명시와 승인된 실행 범위
- Canonicalization Date: 2026-09-03
- Approved Scope: 기존 FRW-R09·FRW-R11의 운영 의미를 Workflow Definition과 이 Conformance Record에 구체화하고 조건부 산출물의 변경 필요성을 확인한다.

문제는 Framework 원칙의 부재가 아니라 Failure Reproduction Workflow의 운영 설명이 충분히 명시적이지 않았다는 점이다. 이 변경은 기존 승인 경계 안의 제한된 자율 실행을 구체화하며 Framework Governance 재설계, 새 Rule ID, Scope 승격·강등, Obligation 강화·완화 또는 다른 Workflow로의 전파를 포함하지 않는다. 2026-08-28의 최초 Acceptance 사실과 범위를 유지하며 과거 승인 범위를 소급하여 확대하지 않는다.

조건부 산출물은 다음과 같이 처리한다.

- 재현 기록(Reproduction Record) Template: 변경하지 않는다. 기존 `Authorized Execution Boundary`, `Approval reference`, 승인 대상·Scope·조건 및 기존 승인 경계 안의 변경 여부 필드가 승인 참조 유지를 지원한다. 승인 정보가 계약 수준에 있고 Run마다 승인을 요구하지 않으므로 후속 실행을 반복 승인 없이 표현할 수 있다. 실행, Verification, 인계 및 연결된 근거에 개별 상태와 결과를 기록할 수 있다.
- [`../../AGENTS.md`](../../AGENTS.md): 기존 저장소 실행 진입점에 FRW-R09·FRW-R11과 후속 실행 조건을 확인하는 짧은 안내를 추가한다. 정본 규칙은 Workflow Definition에서 관리한다.

## Conformance 결과

| 검토 영역 | 결과 | 근거 |
| --- | --- | --- |
| Scope | PASS | 기술·Project 독립적인 Failure Reproduction 방법만 Workflow Scope에 두고, 구체적 기술 구현과 Scenario는 Project/Task Scope로 제한했다. |
| Authority | PASS | Effective Framework Governance를 parent Authority로 유지하고 상위 규칙을 변경하지 않았다. Project별 협업·권한 제약은 후속 실행 범위를 좁힐 수 있으며 Workflow로 우회할 수 없다. |
| 사람 승인 관문(Human Gate) | PASS | 생명주기 상태 경계(Lifecycle State Boundary)와 사람 승인 관문 경계(Human Gate Boundary)를 구분한다. 상태 전환만으로 새 승인을 요구하지 않으며, 전제조건 미충족이나 승인 경계의 실질적 변경 시 후속 실행을 중단하고 사유에 따라 사람의 판단과 해결(Human Resolution) 또는 새 사람 승인 관문으로 전환한다. |
| 제한된 후속 실행 묶음(Grouped Bounded Continuation) | PASS | FRW-R09의 기존 승인 경계 안에서 이전 단계 PASS와 다음 단계 사전조건의 명시적 연결 및 결정적이고 제한된 후속 작업을 전제로 한다. 엔지니어링 의도(Engineering Intent) 불변, 범위(Scope)·권한·접근 범위 비확대, 위험(Risk)·영향 범위(Blast Radius)의 의미 있는 증가 없음, 새로운 비가역적·파괴적·고영향 작업 없음, 새 중요 설계 결정과 중요한 이탈(material deviation) 없음, 검증 기준(Verification Criteria)·수락 기준(acceptance criteria)·주장 경계(Claim Boundary) 불변, 미해결 권한·정본 충돌 없음이라는 모든 조건을 유지한다. |
| 상태와 결과 기록 | PASS | 기존 승인 참조를 유지하며 각 생명주기 상태와 적용 가능한 검증·동기화·종료 결과를 개별적으로 식별하고 기록한다. 단계 PASS가 재현 Outcome을 대체하지 않는다. |
| 동기화 경계 | PASS | 원격 또는 비로컬 동기화는 그 작업 자체가 이미 승인된 실행 경계에 있을 때만 포함한다. 과거 승인 범위를 소급하여 확대하지 않는다. |
| Information Lifecycle | PASS | 관찰된 실패(Observed Failure), 정의된 실패 시나리오(Defined Failure Scenario), Evidence, causal hypothesis와 검증된 재현 주장(Verified Reproduction Claim)을 구분한다. |
| Artifact Lifecycle | PASS | Workflow Definition, Project/Task 재현 기록(Reproduction Record)과 증거 자산(Evidence Assets)의 책임 및 변경 주기를 분리한다. |
| Rule / Obligation | PASS | FRW-R01부터 FRW-R15까지 Scope, Obligation과 FRW-R11 활성화 조건을 보존했다. |
| Verification | PASS | `실험 유효성(Experiment Validity) → 증거 충분성(Evidence Sufficiency) → 실패 징후 평가(Failure Signature Evaluation) → Outcome` 순서와 네 개의 Outcome만 허용한다. |
| 인계(Handoff) | PASS | Verified Evidence, Outcome, 검증된 재현 주장(Verified Reproduction Claim)과 Claim limitations를 필수로 보존한다. |
| Lifecycle | PASS | 권한 있는 Human Acceptance에 따른 `Draft → Effective` 전환과 승인 일자를 보존했다. FRW 생명주기는 `Define → Reproduce → Verify → 인계(Handoff)`로 유지하며 동기화·종료를 새 상태로 추가하지 않았다. |

## Rule / Obligation Traceability

| Rule | Scope | Obligation | Activation condition | Canonical 위치 | Template Enforcement |
| --- | --- | --- | --- | --- | --- |
| FRW-R01 | Workflow | Mandatory | 항상 | 책임과 lifecycle | Template 인계(Handoff) 경계 |
| FRW-R02 | Workflow | Mandatory | 항상 | 용어, Define | 관찰된 실패(Observed Failure) / Scenario 분리 |
| FRW-R03 | Workflow | Mandatory | 판정 대상 실행(Material Run) 수행 시 | 재현 계약(Reproduction Contract) | 사전 Contract 필드와 integrity check |
| FRW-R04 | Workflow | Mandatory | 항상 | 판정 대상 실행(Material Run) traceability | Run별 단일 Revision 필드 |
| FRW-R05 | Workflow | Mandatory | 항상 | Verification 순서 | 순서화된 Verification section |
| FRW-R06 | Workflow | Mandatory | 항상 | Outcome | 제한된 enum placeholder |
| FRW-R07 | Workflow | Mandatory | 항상 | Claim boundary | Evidence와 limitations 필드 |
| FRW-R08 | Workflow | Mandatory | 항상 | causal hypothesis boundary | 별도 Causal Hypotheses section |
| FRW-R09 | Workflow | Mandatory | 승인된 경계가 존재할 때 | 실행 경계와 제한된 후속 실행 묶음(Grouped Bounded Continuation)의 모든 전제조건 | Authorized Execution Boundary, 기존 Approval reference, 실행·검증·인계 기록과 연결된 근거 |
| FRW-R10 | Workflow | Mandatory | 항상 | 계약 개정(Contract Revision) 규칙 | Revision reason과 integrity check |
| FRW-R11 | Workflow | Conditional | 승인된 Intent, Scope, authority/access, Risk, Blast Radius, irreversible/high-impact action 또는 execution boundary의 material 변경 | 생명주기 상태 경계와 사람 승인 관문(Human Gate) 경계 구분, 후속 실행 중단 및 Human Resolution / 새 승인 전환 | 기존 승인 경계 안의 변경 여부, Approval reference와 boundary check |
| FRW-R12 | Workflow | Mandatory | 항상 | Artifact Boundary | Evidence locator 방식 |
| FRW-R13 | Workflow | Mandatory | 항상 | 인계 계약(Handoff Contract) | 인계(Handoff) 필수 필드 |
| FRW-R14 | Workflow | Mandatory | 항상 | Scope와 Artifact Boundary | 해당 작성 형식 없음 |
| FRW-R15 | Workflow | Mandatory | 항상 | Scope | 기술별 필드 없음 |

## Repository Path 검증

- Workflow Definition: `workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md`
- 재현 기록(Reproduction Record) Template: `workflows/failure-reproduction/templates/REPRODUCTION-RECORD.md`
- Conformance Record: `workflows/failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW-CONFORMANCE.md`

기존 repository에는 Workflow, Decision, Review 또는 Session Record directory convention이 없었다. Framework Governance가 `Framework → Workflow → Project → Task` Scope를 정의하고 Failure Reproduction을 Workflow 예시로 명시하므로, `workflows/failure-reproduction/`을 세 Artifact의 공통 canonical location으로 선택했다. 별도의 범용 review taxonomy는 만들지 않았다.

## 검출된 Conflict와 Deviation

- Effective Framework Governance와 승인된 Workflow Design 사이의 material conflict: 없음
- approved design에서의 material deviation: 없음
- 승인 전 non-material issue: Obligation과 Activation condition이 일부 traceability cell에 결합됨
- resolution: Foundation vocabulary만 Obligation에 사용하고 활성화 조건을 별도 column으로 분리함. Rule 의미 변경 없음
- Foundation modification: 없음
- 기술별 Project/Task 구현 추가: 없음

## Final Disposition

Canonical Artifact Review, non-material traceability 정규화와 repository synchronization을 완료했다. 권한 있는 Human Acceptance에 따라 Failure Reproduction Workflow v0.1의 상태는 `Effective`다. unresolved Governance issue는 없다.
