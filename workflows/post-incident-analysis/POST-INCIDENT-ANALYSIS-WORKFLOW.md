# Post-Incident Analysis Workflow

Status: Draft

## 목적과 Governance 위치

이 문서는 활성 인시던트(Active Incident)의 즉각적인 안정화 이후, 필요한 경우 장애 근거와 실패 메커니즘을 재구성하고 기술적 결론 및 예방·개선 책임으로 인계하기 위한 Workflow-level Draft Definition이다. Draft 상태이므로 아직 Effective Workflow로 강제 적용되지 않는다.

- 범위(Scope): Workflow
- 상위 권한 근거(Parent Authority): [AI Engineering Guidelines](../../governance/AI-ENGINEERING-GUIDELINES.md), Status: Effective
- 관련 Workflow: [Failure Reproduction Workflow](../failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md), Status: Effective

이 Workflow는 상위 Governance의 사람 승인 관문(Human Gate), 권한 계층, 정보·산출물 생명주기와 사람의 최종 책임을 재정의하지 않는다. Project별 권한, 역할 분리, escalation path와 Evidence retention은 적용 가능한 Project Collaboration Profile 및 authority binding을 따른다.

## 활성화 조건과 입력

이 Workflow는 활성 인시던트의 즉각적인 안정화를 지연시키지 않는다. 안정화 이후 장애의 기술적 의미, 복구의 완결성, 재발 방지 또는 개선 책임을 분석할 필요가 있을 때 필요한 수준에서 활성화한다.

입력은 다음과 같은 근거 중 적용 가능한 항목일 수 있다.

- production incident Evidence
- 로그, metric, trace, queue·stream 상태와 같은 runtime record
- 운영 대응과 상태 전이 기록
- Failure Reproduction Workflow의 검증된 재현 인계(Verified Reproduction Handoff)

Failure Reproduction의 성공은 활성화 전제조건이 아니다. 재현 결과가 없거나 `NOT_REPRODUCED`, `INCONCLUSIVE`인 경우에도 이용 가능한 Evidence와 주장 경계(Claim Boundary)를 명시하여 분석할 수 있다. 입력의 존재는 그 해석, 인과관계 또는 근본 원인(Root Cause)을 자동으로 증명하지 않는다.

## Workflow 책임과 생명주기

Workflow 책임은 다음 흐름으로 한정한다.

`방향 설정과 경계 확정(Orient & Bound) → Evidence와 실패 메커니즘 재구성(Reconstruct Evidence and Failure Mechanism) → 조건부 식별자·책임 조정(Reconcile Identity / Ownership when applicable) → 복구 의미 검증(Validate Recovery Semantics) → 활성화된 중요 사람 검토(Material Human Review when activated) → 기술적 결론 기록(Record Technical Conclusion) → 예방·개선 인계(Prevention / Remediation Handoff)`

### 1. 방향 설정과 경계 확정(Orient & Bound)

분석 대상 인시던트, 시간 범위, 영향을 받은 시스템과 사용자, 적용 가능한 Authority, 분석 질문, 제외 범위와 사용할 Evidence locator를 식별한다. 직접 확인된 사실·관측, 해석, 가설과 제안을 구분하고, 현재 Evidence가 지지할 수 있는 주장 경계를 정한다.

### 2. Evidence와 실패 메커니즘 재구성(Reconstruct Evidence and Failure Mechanism)

시간 순서, 관련 상태 전이, 제어·데이터 흐름과 실패 조건을 Evidence에 연결한다. 실패 메커니즘과 causal claim은 직접 지지하는 Evidence 및 반대 Evidence와 함께 기술한다. 시간적 선후관계나 상관관계만으로 인과관계를 확정하지 않으며, 미검증 가설을 확정된 기술적 결론으로 표현하지 않는다.

### 3. 조건부 식별자·책임 조정(Reconcile Identity / Ownership when applicable)

재시도(Retry), replay, pending, DLT, quarantine 또는 asynchronous processing으로 논리적 처리 책임이 이동한 경우 PIA-R03에 따라 식별자와 책임을 조정한다. 해당 이동이 없거나 현재 Claim을 검증하는 데 필요하지 않으면 이 단계를 강제하지 않는다.

### 4. 복구 의미 검증(Validate Recovery Semantics)

관찰된 복구 신호가 어떤 복구 단계를 직접 지지하는지 확인한다. infrastructure 정상화, 처리 재개, 백로그 해소와 종단 간 복구 완료(End-to-End Recovery Complete)를 구분하고, 한 단계의 충족을 다음 단계의 증명으로 확대하지 않는다.

### 5. 활성화된 중요 사람 검토(Material Human Review when activated)

PIA-R02의 활성화 조건이 충족되면 상위 Governance의 사람 승인 관문을 적용한다. 검토자는 PIA-R01의 의사결정 인터페이스를 통해 문제, 근거, 시스템 의미, 선택지, 경계와 결과를 이해할 수 있어야 한다.

### 6. 기술적 결론 기록(Record Technical Conclusion)

검증된 사실, 해석, 남은 가설, 적용 가능한 근본 원인 주장, 복구 상태, Claim limitations와 미해결 사항을 구분하여 기록한다. 기술적 결론은 이용 가능한 Evidence가 지지하는 범위를 넘지 않는다.

### 7. 예방·개선 인계(Prevention / Remediation Handoff)

기술적 결론과 우선순위가 정해진 예방·개선 책임을 적절한 downstream owner 또는 Workflow로 인계한다. 인계에는 적용 가능한 Authority, 승인 상태, Evidence locator, Claim boundary, 미해결 위험, 검증 기대사항과 금지된 행위를 보존한다.

## PIA-R01 — 사람이 이해할 수 있는 의사결정 인터페이스(Human-Comprehensible Decision Interface)

사람의 중요한 판단(material judgment)이 필요한 경우, 상위 [AI Engineering Guidelines](../../governance/AI-ENGINEERING-GUIDELINES.md)의 사람 결정 요청의 전달(Human Decision Communication)을 따른다. 이 규칙은 장애 분석에서 기술적 주장과 복구 판단에 필요한 정보를 판단 범위에 비례하여 구체화한다.

- Problem
- Evidence와 그 출처·한계
- causal / system meaning
- 검토할 alternatives 또는 states
- 현재 Claim 및 execution boundary
- 각 선택이나 상태의 consequences
- 명시적인 Human decision point

단순 acceptance 또는 승인 표시는 사람이 문제와 결과를 이해했다는 Evidence로 확대하지 않는다. 이 규칙은 활성 인시던트의 즉각적인 안정화를 지연시키는 선행 의무가 아니며, 안정화 이후 필요한 분석·의사결정에 적용한다.

## PIA-R02 — 중요 의사결정 지점의 사람 검토(Material Decision Point Human Review)

사람 검토는 다음 중 하나가 중요하게(materially) 변경되거나 권한 있는 사람의 판단이 필요한 경우 활성화한다.

- 엔지니어링 의도(Engineering Intent)
- architecture 또는 design meaning
- 주장 경계(Claim Boundary)
- 위험(Risk)
- recovery semantics
- safe continuation
- 결론이나 조치의 applicability / non-applicability

파일 수, 산출물 수 또는 고정된 순차 승인 횟수로 활성화하지 않는다. 기존 승인 경계 안의 정상적인 분석과 검증에 반복 승인을 요구하지 않는다. 사람 검토가 활성화되면 [AI Engineering Guidelines](../../governance/AI-ENGINEERING-GUIDELINES.md)의 사람 승인 관문 기준, 승인 권한과 추적 가능성을 적용하며 별도의 승인 체계를 만들지 않는다.

## PIA-R03 — 식별자 책임성과 복구 완료(Identity Accountability and Recovery Complete)

재시도, replay, pending, DLT, quarantine 또는 asynchronous processing으로 logical ownership이 이동하고 그 이동이 현재 Claim에 관련된 경우 다음 연결을 Evidence로 조정한다.

`accepted logical identity → current state / ownership → correct continuation → final disposition`

처리량, 소비자 지연(Consumer Lag), pending count와 같은 집계 신호는 진행 또는 문제 범위 축소 Evidence가 될 수 있다. 그러나 개별 logical identity와 최종 disposition의 조정 없이 accountability Evidence로 확대하지 않는다.

`count / lag / pending → progress / narrowing Evidence`

`identity reconciliation → accountability Evidence`

복구 주장은 다음 단계를 구분한다.

`Infrastructure Recovery → Processing Recovery → Backlog Recovery → End-to-End Recovery Complete`

각 단계의 충족은 자동으로 다음 단계를 증명하지 않는다. logical ownership 이동이 없거나 식별자 조정이 현재 Claim에 필요하지 않으면 identity reconciliation을 요구하지 않는다.

## PIA-R04 — 독자 책임과 유연한 산출물 구조(Reader Responsibility and Flexible Artifact Topology)

분석 결과를 지속적으로 보존하거나 전달할 산출물이 필요한 경우, 이번 분석에서 독자에게 실제로 필요한 설명을 먼저 판정한다. 이미 있는 문서가 그 역할을 하면 재사용하고, 부족한 설명만 기존 또는 신규 산출물에 추가한다. 필요하지 않은 설명을 만들기 위해 산출물을 늘리지 않는다.

다음 네 항목은 판정할 독자 책임의 후보이며, 항상 모두 적용되는 필수 항목은 아니다. 적용되는 책임은 해당 설명을 담는 산출물에 대응시키고, 적용되지 않는 책임은 `N/A`로 둘 수 있다.

1. AI와 사람의 responsibility and authority
2. failure mechanism과 Claim
3. 사람의 troubleshooting / operational response
4. 적용 가능한 경우 concise external / README summary

여러 책임을 하나의 산출물에 함께 둘 수 있고, 서로 다른 변경 주기나 독자가 있을 때 분리할 수 있다. 이 Workflow는 고정된 파일 수, 파일명 taxonomy 또는 작성 순서를 요구하지 않는다.

## 산출물과 책임 경계

필수 결과는 특정 파일 집합이 아니라 다음 의미가 추적 가능한 분석 상태다.

- 분석 Scope, Authority와 Claim boundary
- Evidence에 연결된 failure mechanism
- 적용 가능한 identity / ownership reconciliation과 recovery state
- 활성화된 사람 검토의 대상·결정·권한 참조
- 검증된 기술적 결론과 limitations
- 예방·개선 downstream responsibility 및 인계 경계

Project 상황에 따라 기존 incident record, decision record, runbook, issue 또는 README를 재사용할 수 있다. 산출물의 위치와 보존 기간은 Project의 authority binding과 Evidence retention 조건을 따른다.

## 종료점과 Downstream 경계

Workflow 종료점은 `Validated Technical Conclusion and Prevention / Remediation Handoff`다.

다음 행위는 이 Workflow 밖이며, 필요한 경우 적용 가능한 Authority와 별도 downstream responsibility로 라우팅한다.

- remediation implementation
- application / configuration mutation
- production deployment 또는 production change
- remediation effectiveness의 별도 실행 검증

인계는 위 행위의 실행 권한이나 완료를 뜻하지 않는다. downstream 실행은 해당 Workflow, Project Governance, 승인 경계와 검증 기준을 별도로 따라야 한다.

## 규칙과 의무(Rules and Obligations)

아래 규칙의 범위는 모두 `Workflow`다. Draft 상태에서는 Effective Governance로 강제 적용되지 않는다.

| Rule ID / 이름 | Scope | Obligation | Activation condition | 규칙 |
| --- | --- | --- | --- | --- |
| PIA-R01 — Human-Comprehensible Decision Interface | Workflow | Conditional | 사람의 중요한 판단이 필요한 경우 | 상위 Governance의 사람 결정 요청 전달 규칙을 따르고, 장애 분석의 Problem, Evidence, causal / system meaning, alternatives / states, boundary, consequences와 Human decision point를 판단 범위에 비례하여 제공한다. 단순 acceptance를 understanding Evidence로 확대하지 않으며 활성 인시던트 안정화를 지연시키지 않는다. |
| PIA-R02 — Material Decision Point Human Review | Workflow | Conditional | Engineering Intent, architecture / design meaning, Claim Boundary, risk, recovery semantics, safe continuation 또는 applicability / non-applicability의 material change나 권한 있는 사람 판단이 필요한 경우 | 상위 Governance의 사람 승인 관문을 적용한다. 파일 수나 고정된 순차 승인 횟수로 활성화하지 않으며 기존 사람 승인 관문을 재정의하지 않는다. |
| PIA-R03 — Identity Accountability and Recovery Complete | Workflow | Conditional | logical ownership이 이동하고 identity reconciliation이 현재 Claim에 관련된 경우 | accepted logical identity부터 final disposition까지 조정하고 집계 진행 Evidence와 accountability Evidence를 구분한다. Infrastructure, Processing, Backlog와 End-to-End Recovery를 구분하며 각 단계가 다음 단계를 자동 증명하지 않도록 한다. |
| PIA-R04 — Reader Responsibility and Flexible Artifact Topology | Workflow | Conditional | 분석 결과를 지속적으로 보존하거나 전달할 산출물이 필요한 경우 | 네 독자 책임 후보 중 실제 필요한 항목을 판정하고, 적용되는 책임만 기존 또는 신규 산출물에 대응시킨다. 기존 산출물이 충족하면 재사용하고 적용되지 않는 책임은 `N/A`로 둘 수 있다. 고정된 파일 수·파일명·작성 순서를 요구하지 않는다. |

## 최소 검증과 완료 기준

- 활성 인시던트의 즉각적인 안정화가 이 Workflow의 선행 의무로 지연되지 않았다.
- Failure Reproduction 성공을 활성화 전제조건으로 사용하지 않았다.
- Evidence, 관측된 사실, 해석, 가설, 제안과 확정된 결론을 구분했다.
- failure mechanism과 기술적 결론이 Evidence 및 Claim boundary에 연결되어 있다.
- 해당되는 경우 identity / ownership 이동과 final disposition이 조정되어 있다.
- count, lag 또는 pending을 accountability의 충분한 Evidence로 확대하지 않았다.
- Infrastructure, Processing, Backlog와 End-to-End Recovery 단계를 구분했다.
- 사람 검토는 PIA-R02의 material decision 기준으로 활성화되었고, 활성화된 경우 PIA-R01의 정보와 권한 참조를 보존했다.
- 분석 산출물이 필요한 경우 PIA-R04의 독자 책임별 적용 여부를 판정하고, 적용되는 설명은 기존 산출물의 충족 여부를 확인한 뒤 필요한 위치에 보존했다.
- 고정된 파일 taxonomy 또는 순차적 사람 승인 체계를 만들지 않았다.
- 기술적 결론, limitations, 미해결 사항과 예방·개선 인계 책임이 식별 가능하다.
- remediation 구현, production change와 별도 효과 검증을 Workflow 완료로 포함하지 않았다.

위 조건을 충족하고 `Validated Technical Conclusion and Prevention / Remediation Handoff`가 기록되면 Workflow를 종료할 수 있다.
