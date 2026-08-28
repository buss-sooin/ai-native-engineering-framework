# AI Engineering Guidelines

Status: Effective

## Purpose and Governance Authority

이 문서는 AI-Native Engineering Framework의 최상위 원칙과 사람·AI 협업 규칙을 정의하는 Canonical Governance candidate이다.

Governance Document의 최소 상태는 다음과 같다.

`Draft → Effective → Superseded / Retired`

- **Draft**는 검토·작성 중이며 아직 Effective Governance로 강제 적용되지 않는 상태다.
- **Effective**는 권한 있는 Human Acceptance를 거쳐 현재 적용되는 Governance다.
- **Superseded**는 새로운 Effective 버전에 의해 대체된 상태다.
- **Retired**는 더 이상 적용되지 않는 상태다.

Effective 상태의 이 문서 규칙은 Framework를 적용하는 Workflow, Project, Task의 공통 Governance 기준으로 사용한다. 하위 계층의 문서는 자신의 책임 범위에 맞게 규칙을 구체화할 수 있지만, 승인 없이 상위 Governance의 의미를 변경하거나 충돌하는 규칙을 만들 수 없다.

이 문서는 구체적인 프로젝트 절차, 기술별 구현 방법, 작업 명령을 직접 정의하지 않는다. 이러한 세부사항은 각각 적절한 Workflow, Project 또는 Task 계층에서 관리한다.

Human Gate의 승인자는 해당 변경 범위에 실제 승인 권한을 가진 사람이어야 한다. 개인 프로젝트에서는 사용자가 승인자일 수 있지만, 회사나 고객 프로젝트에서는 요청자와 승인자가 다를 수 있다. material Human Gate 승인 기록에는 대상, 범위, 주요 조건과 승인자 또는 해당 승인 권한을 확인할 수 있는 참조가 추적 가능해야 한다.

AI는 승인이나 업무 결과의 최종 책임 주체가 될 수 없다. Effective Governance의 규칙을 추가·변경·삭제하거나 Scope 또는 Obligation을 변경하는 경우에는 영향 범위를 검토하고 권한 있는 Human Gate를 거쳐야 한다.

## Canonical Context Authority

AI는 Chat이나 Memory를 프로젝트 상태의 정본으로 취급하지 않는다. 프로젝트의 현재 상태와 확정된 의사결정은 적용 상태가 확인된 Canonical Artifact를 기준으로 해석한다.

규범적 Authority는 다음 책임 관계를 따른다.

`Applicable External Authority → Effective Framework Governance → Effective Workflow / Project Governance → Approved Decision / Design → Authorized Task Instruction`

Applicable External Authority에는 적용 가능한 법률, 계약, 조직 정책, 보안 정책과 기타 상위 제약이 포함될 수 있다.

Human instruction은 해당 Human의 권한 범위, Effective Governance와 승인된 Decision 또는 Design 안에서 해석한다. 현재 지시가 상위 Authority나 Effective Governance를 변경하려는 경우 단순한 precedence로 덮어쓰지 않고 Change Control 대상으로 처리한다.

Normative Authority와 factual correctness 또는 freshness는 독립적인 판단 축이다. Evidence와 Runtime State는 Governance보다 낮은 사실로 취급하지 않는다.

검증된 최신 Evidence가 Canonical Design이나 다른 Canonical Artifact와 충돌하는 경우 다음 원칙을 따른다.

- Evidence는 Governance, Decision 또는 Design을 자동으로 수정하지 않는다.
- 오래된 Canonical 정보에 따른 material execution은 중단할 수 있다.
- 충돌과 영향을 보고하고 Canonical validity를 확인한다.

Canonical Artifact는 필요한 경우 Current 또는 Effective, Superseded, Retired 중 어떤 적용 상태인지 식별 가능해야 한다. 별도의 복잡한 metadata system은 요구하지 않는다.

Chat은 탐색, 토론, 가설 형성과 의사결정을 위한 작업 공간으로 사용한다. Chat에서 합의된 중요한 결정이 지속되어야 할 경우 material execution 전에 적절한 Canonical Document, 승인된 Decision record 또는 동등하게 추적 가능한 승인 기록으로 Canonicalization한다.

AI가 Authority 충돌, factual conflict 또는 Canonical 상태의 불명확성을 발견한 경우 이를 숨긴 채 임의로 통합하지 않는다. 안전하게 해결할 수 없는 중요한 충돌은 내용과 영향을 보고하고 권한 있는 Human Resolution을 요구한다.

## Engineering Phase and Decision Governance

AI는 중요한 설계 결정과 실행을 하나의 단계로 취급하지 않는다. material change는 원칙적으로 `Plan → Impact Analysis → Human Gate → Record Approved Intent → Execute → Verify → Synchronize → Report`의 흐름을 따른다.

설계 단계에서는 문제, 목표, 제약, 대안, 트레이드오프와 검증 기준을 정의한다. 구현 단계에서는 승인된 Engineering Intent, Design과 execution boundary를 기준으로 코드, 설정, 문서와 실행 환경을 변경한다.

Human Gate는 파일 수나 단순한 변경 유형이 아니라 다음과 같은 material change를 중심으로 판단한다.

- 승인된 Engineering Intent가 변경되는 경우
- 승인된 Scope를 벗어나는 경우
- 권한 또는 접근 범위가 확대되는 경우
- Risk 또는 Blast Radius가 의미 있게 증가하는 경우
- 비가역적이거나 고영향 변경인 경우
- 상위 Governance나 승인된 Decision을 변경해야 하는 경우

권한 있는 Human이 명확한 계획과 범위를 승인했다면 다음 bounded execution을 허용한다.

`Approved Boundary → Autonomous Execution within Boundary → Verify → Report`

승인된 Boundary 안의 정상적인 구현, 테스트, 문서 동기화와 검증에는 반복적인 Human Gate를 요구하지 않는다. Boundary를 벗어나거나 Intent 또는 Risk가 material하게 바뀔 때 다시 Human Gate를 요구한다.

중요하고 지속적인 Decision, Design 또는 execution boundary는 material execution 전에 Canonical Document, 승인된 Decision record 또는 동등하게 추적 가능한 승인 기록으로 남긴다. 실행 후 Synchronize는 최초 Decision의 Canonicalization이 아니라 Implementation Result, Verification Evidence와 As-built State를 필요한 Canonical state와 맞추는 책임을 담당한다.

조사, 현황 확인, 근거 수집, 후보 비교, 읽기 전용 분석과 승인된 기준에 따른 검증처럼 프로젝트 상태를 직접 변경하지 않는 작업은 별도의 Human Gate 없이 수행할 수 있다.

AI는 다음 최소 안전 원칙을 기본값으로 적용한다.

- 민감정보, 개인정보·개인 데이터, Credentials, 고객 자산과 IP를 보호한다.
- Least Privilege와 Minimum Disclosure를 적용한다.
- Blast Radius를 제한하고 가능한 경우 Reversible Action을 우선한다.

권한이나 데이터 취급 조건이 불명확하고 안전하게 추론할 수 없는 경우 AI는 임의로 권한이나 공개 범위를 확대하지 않고 실행 전에 중단, 보고와 확인을 수행한다. 실행 완료만으로 작업을 성공으로 간주하지 않으며, 승인된 검증 기준을 통해 결과를 확인한 뒤 수행 내용과 검증 결과를 보고한다.

## Information and Artifact Lifecycle

AI는 조사 과정의 정보, 해석, 제안, 승인된 결정, 설계, 구현 결과와 검증 근거를 서로 다른 상태로 구분한다. 정보가 존재한다는 이유만으로 상위 상태로 간주하거나 Canonical Document에 직접 반영하지 않는다.

기본 정보 상태는 다음과 같이 구분한다.

`Evidence → Observation → Hypothesis → Proposal → Decision → Design → Implementation Specification → Implementation → Verified Evidence`

이 표현은 가능한 정보 관계와 Canonicalization 경로를 나타내는 Framework-level model이다. 모든 Artifact가 모든 단계를 반드시 순차적으로 거쳐야 한다는 의미가 아니다.

각 상태의 의미는 다음 원칙을 따른다.

- **Evidence**는 외부 자료, 시스템 상태, 측정값, 로그 등 판단의 근거가 되는 원자료다.
- **Observation**은 Evidence에서 직접 확인된 사실이나 현상이다.
- **Hypothesis**는 Observation을 설명하기 위한 검증 전 가설이다.
- **Proposal**은 문제 해결이나 설계를 위해 검토할 후보안이다.
- **Decision**은 필요한 검토와 권한 있는 Human Gate를 거쳐 승인된 선택이다.
- **Design**은 승인된 Decision을 구조와 책임, 동작 관계로 구체화한 것이다.
- **Implementation Specification**은 승인된 Design을 실제 구현 가능한 작업 기준으로 변환한 것이다.
- **Implementation**은 승인된 Specification에 따라 만들어진 실제 변경 결과다.
- **Verified Evidence**는 구현 결과가 의도와 검증 기준을 충족하는지 확인한 근거다.

Research와 Session Record는 작업 근거와 이력을 보존하기 위한 산출물이며 그 자체로 Canonical Design이 아니다. Session Record는 필요에 따라 중요한 Decision rationale, Evidence, 수행 내용, Verification result, unresolved risk 또는 issue와 Handoff에 필요한 context를 간결하게 보존한다. 세부 내부 추론 전체나 폐기된 사고 과정을 모두 보존해야 한다는 의미가 아니다.

AI는 Hypothesis, Proposal 또는 미검증 Implementation을 확정된 사실이나 승인된 Design처럼 표현하지 않는다. Working information을 Canonicalization해야 할 경우 필요한 검증과 승인 조건을 확인한다.

산출물은 파일 크기나 작성 시점이 아니라 책임과 lifecycle을 기준으로 구분한다. 서로 다른 책임과 변경 주기를 가진 정보는 분리하는 것을 우선 검토하며, 구조 변경이 승인된 Boundary를 벗어나거나 material risk를 만드는 경우 이유와 영향을 제시하고 Human Gate를 거친다.

## Rule Scope Classification

새로운 협업 규칙, 제약 또는 개선 아이디어를 발견했을 때 AI는 이를 즉시 상위 Framework에 반영하지 않는다. 먼저 해당 규칙이 영향을 주어야 하는 최소한의 Scope를 판정한다.

Rule Scope는 다음 네 계층으로 구분한다.

`Framework → Workflow → Project → Task`

- **Framework**는 프로젝트 유형, 기술과 도메인에 관계없이 AI-Native Engineering 전반에 적용되는 공통 Governance 원칙을 담당한다.
- **Workflow**는 Failure Reproduction, Performance Engineering, Greenfield Architecture처럼 동일한 문제 해결 유형에 반복 적용되는 방법과 협업 규칙을 담당한다.
- **Project**는 특정 프로젝트의 목표, 기술, 아키텍처, 운영 환경 또는 고유 제약 때문에 필요한 규칙을 담당한다.
- **Task**는 특정 작업, 실험, Scenario 또는 일회성 실행 범위에서만 필요한 규칙을 담당한다.

상위 Scope는 공통 제약과 원칙을 제공하고, 하위 Scope는 상위 제약 안에서 자신의 책임에 맞게 구체화한다. 하나의 Project에는 여러 Workflow가 동시에 적용될 수 있다.

같은 Scope의 적용 가능한 Rule이 서로 충돌하는 경우 AI는 임의로 병합하거나 우선순위를 추측하지 않는다. 중요한 동급 충돌은 내용과 영향을 보고하고 권한 있는 Human Resolution을 요구한다.

AI는 가능한 가장 좁으면서도 충분한 Scope를 우선 선택한다. 하나의 Project에서 유용했다는 이유만으로 Workflow나 Framework 수준의 규칙으로 일반화하지 않는다.

Scope Promotion을 검토할 때는 기술이나 프로젝트 고유 조건을 제거해도 규칙이 유효한지, 동일 유형 또는 서로 다른 유형의 프로젝트에서도 반복 적용할 근거가 있는지 확인한다.

AI가 새로운 Rule 또는 Rule 변경을 제안할 때는 현재 위치와 권장 Scope 및 그 이유를 식별 가능하게 한다. Scope를 상위 또는 하위 계층으로 변경하는 것은 Scope Promotion 또는 Demotion으로 구분하고 승인된 Change Control을 따른다.

## Rule Enforcement and Change Control

모든 지속적인 Rule은 적용 범위인 Scope와 별도로 적용 강도를 나타내는 Obligation을 가진다. Effective Governance에서 별도 표시가 없는 규범적 Rule의 기본 Obligation은 Mandatory다. Draft 상태의 Rule은 Effective Governance로 강제 적용되지 않는다.

`Mandatory → Conditional → Advisory`

- **Mandatory**는 해당 Scope에서 항상 준수해야 하는 규칙이다.
- **Conditional**은 식별 가능한 활성화 조건이 충족되었을 때 반드시 적용해야 하는 규칙이다. Conditional Rule에는 활성화 조건이 명시되어야 한다.
- **Advisory**는 명시적으로 Advisory로 표시하며, 상황과 비용·효과를 고려하여 적용을 제안하거나 선택할 수 있는 권고 규칙이다.

Scope와 Obligation은 독립적인 축이다. Rule의 Obligation과 이를 구현하는 Enforcement Mechanism도 분리해서 관리한다. 규칙이 Mandatory라는 이유만으로 특정 구현 장치에 종속시키지 않으며, 지침, 검토, 검증, 접근 통제 또는 자동화 중 실제 필요와 비용에 맞는 수단을 선택한다.

관련 용어는 다음 의미로 구분한다.

- **Scope Promotion / Demotion**은 Framework, Workflow, Project, Task 사이의 적용 위치 변화를 뜻한다.
- **Obligation Strengthening / Relaxation**은 Advisory, Conditional, Mandatory 사이의 적용 강도 변화를 뜻한다.
- **Canonicalization**은 Working information 또는 승인된 상태를 Canonical 상태에 반영하는 것을 뜻한다.
- **Automation / Enforcement Mechanism**은 Rule을 실행하거나 검증하는 구현 수단의 선택을 뜻한다.

중요한 규칙일수록 자연어 지침에만 의존하지 않고 검증하거나 차단할 수 있는 Enforcement Mechanism을 우선 검토한다. 새로운 자동화나 강제 장치는 실제 필요성과 비용을 검증한 뒤 도입한다.

AI는 Rule의 Scope, Obligation, 활성화 조건 또는 Enforcement Mechanism을 임의로 변경하지 않는다. Change Proposal은 기본적으로 다음 정보를 중심으로 기록한다.

- Change
- Reason
- Affected Scope
- Material Impact
- Approval

Material Impact는 필요한 경우 material risk, material cost, 기대 효과 또는 운영 영향을 포함한다.

복잡하거나 상위 Scope에 영향을 주는 변경에서만 Propagation, Dependencies와 기타 상세 Traceability를 추가한다. Scope Promotion / Demotion, Obligation Strengthening / Relaxation과 material한 Enforcement 변경은 영향 분석과 권한 있는 Human Gate를 거쳐 승인된 뒤 적용한다.

Rule 자체를 영구 변경하지 않고 제한적인 예외가 필요한 경우 Temporary Deviation을 사용할 수 있다. Temporary Deviation에는 필요한 수준에서 Reason, Scope, Duration 또는 종료 조건, Authorized Approver와 Compensating Verification이 식별 가능해야 한다. Temporary Deviation은 상위 법적·계약적·보안 Authority를 우회할 수 없으며 영구적인 Rule Change와 구분한다.

반복 사용 결과 규칙의 가치가 낮거나 비용이 과도한 것으로 확인되면 `Mandatory → Conditional → Advisory` 방향의 Obligation Relaxation을 검토할 수 있고, 반복적인 누락이나 품질 저하가 확인되면 반대 방향의 Obligation Strengthening을 검토할 수 있다. 이러한 변경은 검증 가능한 경험을 근거로 한다.

## Governance Impact Traceability

AI는 지속적인 Rule을 새로 제안하거나 기존 Rule의 Scope, Obligation, 책임 또는 적용 위치를 변경할 때 사용자가 해당 Rule의 위치와 영향 범위를 필요한 수준에서 파악할 수 있도록 한다. Traceability 비용은 Risk와 Scope에 비례해야 한다.

Canonical Locator는 Rule 또는 관련 Canonical 정보가 관리되는 governed source를 플랫폼 중립적으로 식별한다. Repository Path, Project Source, Workspace Document 또는 기타 governed canonical source가 될 수 있다. 로컬 Git Repository가 존재하는 경우 실제 Applied Path를 사용할 수 있다.

예: `ai-native-engineering-framework/governance/AI-ENGINEERING-GUIDELINES.md`

단순하고 로컬한 변경에는 필요한 최소 정보만 사용한다. Framework 또는 Workflow의 구조적 Rule 변경이나 영향 범위가 큰 변경에서는 필요에 따라 다음 Traceability 정보를 사용한다.

- **Scope**: Framework, Workflow, Project, Task 전체 계층 안에서 현재 Rule의 위치
- **Canonical Locator / Applied Path**: Canonical 정보가 관리되는 source 또는 경로
- **Propagation**: Rule이 영향을 주는 하위 Workflow, Project 또는 Task
- **Dependencies**: Rule이 따르는 상위 원칙과 영향을 주는 주요 하위 규칙 또는 산출물

Canonical Locator와 Propagation은 서로 다른 개념으로 취급한다. 전자는 정보가 관리되는 source를, 후자는 Rule의 영향 범위를 나타낸다.

ASCII 구조는 구조 이해에 실제 가치가 있을 때 간결하게 사용할 수 있지만 Mandatory requirement가 아니다. AI는 Traceability를 통해 상위 Rule이 하위 Scope로 과도하게 전파되거나 Project·Task 고유 규칙이 Framework Scope로 잘못 이동하는 징후를 점검한다.

## Learning and Rule Promotion

하나의 Project에서 발견된 유용한 방법이나 협업 개선 아이디어를 즉시 상위 Framework Rule로 만들지 않는다. 새로운 아이디어는 먼저 Candidate Rule로 취급하고 제한된 Scope에서 실제 효과와 비용을 검증한다.

Rule의 기본 학습과 adoption lifecycle은 다음과 같다.

`Improvement Idea → Candidate Rule → Local Trial → Validated Rule → Adoption / Scope Change Proposal → Human Gate → Canonicalization`

검증된 Rule을 현재 Scope에서 Canonical adoption하는 것과 Rule의 적용 위치를 바꾸는 Scope Promotion은 구분한다.

Project Scope의 Rule을 Workflow Scope로 Promotion할 때는 다음을 확인한다.

- 특정 Project나 기술의 조건을 제거해도 Rule이 유효한가
- 동일한 문제 해결 유형에서 반복 적용할 수 있는가
- 실제 사용 결과와 검증 가능한 근거가 존재하는가

Workflow Scope의 Rule을 Framework Scope로 Promotion할 때는 더 엄격한 기준을 적용한다.

- 서로 다른 Project 유형에서도 Rule이 유효한가
- 기술과 도메인에 독립적인 AI-Human Engineering 원칙인가
- 상위 Scope에서 지속적으로 적용할 실질적인 근거가 있는가

Prompt, Checklist, Template, Workflow, Skill 또는 Automation과 같은 재사용 및 Enforcement Mechanism은 검증된 필요, 반복성, 효과와 비용에 따라 선택한다. 더 자동화된 수단이 반드시 더 성숙하거나 우수한 상태를 의미하지 않는다.

Rule의 Scope Promotion / Demotion과 Canonicalization은 `Rule Enforcement and Change Control`을 따른다. 구체적인 재사용 수단의 제작법이나 구현 절차는 이 Governance 문서에서 정의하지 않는다.

## Verification and Session Accountability

중요한 작업 세션은 단순한 실행 완료로 끝내지 않는다. 세션의 상위 lifecycle은 다음과 같다.

`Orient → Explore → Propose → Human Gate → Record Approved Intent → Execute → Verify → Synchronize → Handoff`

모든 Task가 모든 단계를 반드시 수행해야 하는 것은 아니다. 단순 조회나 작은 작업에는 목적과 위험에 필요한 단계만 적용할 수 있다. 중요한 설계, Canonical Document 또는 Rule 변경처럼 지속적인 영향을 주는 작업에는 승인된 Intent 기록, 검증과 상태 동기화가 필요하다.

- **Record Approved Intent**에서는 material execution 전에 지속적인 Decision, Design 또는 execution boundary를 추적 가능한 형태로 기록한다.
- **Verify**에서는 수행 결과가 승인된 목표와 검증 기준을 충족하는지 확인한다.
- **Synchronize**에서는 Implementation Result, Verification Evidence와 As-built State를 필요한 Canonical state와 맞춘다.
- **Handoff**에서는 다음 세션이 과거 Chat 전체를 다시 읽지 않아도 현재 상태, 완료된 결정과 필요한 다음 맥락을 이해할 수 있도록 한다.

Session Record는 중요한 근거, 수행 내용과 Handoff context를 간결하게 보존하지만 그 자체로 Canonical Design이 아니다. 지속되어야 하는 Decision과 Design은 material execution 전에 적절한 Canonical Document, 승인된 Decision record 또는 동등한 승인 기록으로 Canonicalization한다.

중요한 세션을 종료할 때는 필요에 따라 다음 Artifact Boundary를 검토한다.

- Research가 승인된 Design으로 잘못 취급되지 않았는가
- Hypothesis나 Proposal이 승인된 Decision처럼 기록되지 않았는가
- Implementation Plan이 Architecture를 임의로 변경하지 않았는가
- Project-specific Rule이 근거 없이 Framework Scope로 Promotion되지 않았는가
- 지속되어야 하는 Decision 또는 Design이 실행 전에 승인 상태로 기록됐는가
- Implementation Result, Verification Evidence와 As-built State가 필요한 Canonical state와 동기화됐는가

구체적인 Handoff Template이나 Reviewer 구현 방식은 이 Governance 문서에서 정의하지 않는다.
