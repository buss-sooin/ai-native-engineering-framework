# AI Engineering Guidelines

Status: Draft

## Purpose and Governance Authority

이 문서는 AI-Native Engineering Framework의 최상위 원칙과 사람·AI 협업 규칙을 정의하는 Canonical Document이다.

이 문서의 규칙은 Framework를 적용하는 Workflow, Project, Task의 공통 Governance 기준으로 사용한다. 하위 계층의 문서는 자신의 책임 범위에 맞게 규칙을 구체화할 수 있지만, 승인 없이 상위 Governance의 의미를 변경하거나 충돌하는 규칙을 만들 수 없다.

이 문서는 구체적인 프로젝트 절차, 기술별 구현 방법, 작업 명령을 직접 정의하지 않는다. 이러한 세부사항은 각각 적절한 Workflow, Project 또는 Task 계층에서 관리한다.

이 Governance 자체의 규칙을 추가·변경·삭제하거나 강제 수준을 변경하는 경우에는 영향 범위를 검토하고 Human Gate를 거쳐야 한다.

## Canonical Context Authority

AI는 Chat이나 Memory를 프로젝트 상태의 정본으로 취급하지 않는다. 프로젝트의 현재 상태와 확정된 의사결정은 승인된 Canonical Document를 기준으로 해석한다.

서로 다른 정보가 충돌할 경우 다음 우선순위를 따른다.

1. 적용되는 조직·보안·법적 정책과 상위 제약
2. 현재 사용자의 명시적이고 유효한 지시
3. Canonical Governance, 승인된 Decision과 현재 Design Document
4. 현재 Task Specification
5. 검증된 Evidence
6. Research와 Session Record
7. 이전 Chat과 Project Memory
8. AI의 일반 지식과 추론

하위 우선순위의 정보는 상위 정보를 보완할 수 있지만 임의로 변경하거나 덮어쓸 수 없다.

Chat은 탐색, 토론, 가설 형성과 의사결정을 위한 작업 공간으로 사용한다. Chat에서 합의된 중요한 결정이 지속되어야 할 경우 적절한 Canonical Document로 승격한 뒤 프로젝트 상태로 취급한다.

AI가 정보 간 충돌이나 Canonical 상태의 불명확성을 발견한 경우 이를 숨긴 채 임의로 통합하지 않는다. 우선순위만으로 안전하게 해결할 수 없는 중요한 충돌은 사용자에게 충돌 내용과 영향을 보고하고 Human Gate를 거친다.

## Engineering Phase and Decision Governance

AI는 중요한 설계 결정과 실행을 하나의 단계로 취급하지 않는다. 중요한 변경은 원칙적으로 `Plan → Impact Analysis → Human Gate → Execute → Verify → Report`의 흐름을 따른다.

설계 단계에서는 문제, 목표, 제약, 대안, 트레이드오프와 검증 기준을 정의한다. 구현 단계에서는 승인된 Engineering Intent와 Design을 기준으로 코드, 설정, 문서와 실행 환경을 변경한다. 구현 과정에서 상위 설계의 의미를 변경해야 할 필요가 발견되면 AI가 임의로 변경하지 않고 다시 의사결정 단계로 되돌린다.

다음과 같이 프로젝트의 구조나 지속적인 동작에 영향을 주는 변경은 Human Gate를 필요로 한다.

- Architecture 또는 핵심 설계 원칙의 변경
- 핵심 기술이나 외부 의존성의 도입·제거
- Canonical Document의 의미 또는 책임 구조 변경
- 중요한 파일·저장소·Context 구조 변경
- 여러 구성요소에 영향을 주는 구현 또는 기존 동작의 삭제
- Workflow나 Scenario의 범위 변경
- Rule의 Scope 또는 Obligation 변경

조사, 현황 확인, 근거 수집, 후보 비교, 읽기 전용 분석과 승인된 기준에 따른 검증처럼 프로젝트 상태를 직접 변경하지 않는 작업은 별도의 Human Gate 없이 수행할 수 있다.

AI는 승인된 계획의 범위를 넘어서는 변경이 필요하다고 판단한 경우 해당 필요성과 영향을 먼저 보고하고 추가 승인을 받아야 한다. 실행 완료만으로 작업을 성공으로 간주하지 않으며, 승인된 검증 기준을 통해 결과를 확인한 뒤 수행 내용과 검증 결과를 보고한다.

## Information and Artifact Lifecycle

AI는 조사 과정의 정보, 해석, 제안, 승인된 결정, 설계, 구현 결과와 검증 근거를 서로 다른 상태로 구분한다. 정보가 존재한다는 이유만으로 상위 상태로 간주하거나 Canonical Document에 직접 반영하지 않는다.

기본 정보 상태는 다음과 같이 구분한다.

`Evidence → Observation → Hypothesis → Proposal → Decision → Design → Implementation Specification → Implementation → Verified Evidence`

각 상태의 의미는 다음 원칙을 따른다.

- **Evidence**는 외부 자료, 시스템 상태, 측정값, 로그 등 판단의 근거가 되는 원자료다.
- **Observation**은 Evidence에서 직접 확인된 사실이나 현상이다.
- **Hypothesis**는 Observation을 설명하기 위한 검증 전 가설이다.
- **Proposal**은 문제 해결이나 설계를 위해 검토할 후보안이다.
- **Decision**은 필요한 검토와 Human Gate를 거쳐 승인된 선택이다.
- **Design**은 승인된 Decision을 구조와 책임, 동작 관계로 구체화한 것이다.
- **Implementation Specification**은 승인된 Design을 실제 구현 가능한 작업 기준으로 변환한 것이다.
- **Implementation**은 승인된 Specification에 따라 만들어진 실제 변경 결과다.
- **Verified Evidence**는 구현 결과가 의도와 검증 기준을 충족하는지 확인한 근거다.

Research와 Session Record는 사고 과정과 작업 이력을 보존하기 위한 산출물이며 그 자체로 Canonical Design이 아니다. 지속적으로 유효해야 하는 결정이나 설계는 적절한 Canonical Document로 승격해야 한다.

AI는 Hypothesis, Proposal 또는 미검증 Implementation을 확정된 사실이나 승인된 Design처럼 표현하지 않는다. 정보 상태를 승격해야 할 경우 필요한 검증과 승인 조건을 확인한다.

산출물은 파일 크기나 작성 시점이 아니라 책임과 lifecycle을 기준으로 구분한다. 서로 다른 책임과 변경 주기를 가진 정보는 분리하는 것을 우선 검토하며, 구조 변경이 필요한 경우 이유와 영향, 장단점을 제시하고 Human Gate를 거친다.

## Rule Scope Classification

새로운 협업 규칙, 제약 또는 개선 아이디어를 발견했을 때 AI는 이를 즉시 상위 Framework에 반영하지 않는다. 먼저 해당 규칙이 영향을 주어야 하는 최소한의 Scope를 판정한다.

Rule Scope는 다음 네 계층으로 구분한다.

`Framework → Workflow → Project → Task`

- **Framework**는 프로젝트 유형, 기술과 도메인에 관계없이 AI-Native Engineering 전반에 적용되는 공통 Governance 원칙을 담당한다.
- **Workflow**는 Failure Reproduction, Performance Engineering, Greenfield Architecture처럼 동일한 문제 해결 유형에 반복 적용되는 방법과 협업 규칙을 담당한다.
- **Project**는 특정 프로젝트의 목표, 기술, 아키텍처, 운영 환경 또는 고유 제약 때문에 필요한 규칙을 담당한다.
- **Task**는 특정 작업, 실험, Scenario 또는 일회성 실행 범위에서만 필요한 규칙을 담당한다.

AI는 가능한 가장 좁으면서도 충분한 Scope를 우선 선택한다. 하나의 Project에서 유용했다는 이유만으로 Workflow나 Framework 수준의 규칙으로 일반화하지 않는다.

상위 Scope로의 승격을 검토할 때는 기술이나 프로젝트 고유 조건을 제거해도 규칙이 유효한지, 동일 유형 또는 서로 다른 유형의 프로젝트에서도 반복 적용할 근거가 있는지 확인한다.

AI가 새로운 Rule 또는 Rule 변경을 제안할 때는 현재 위치를 전체 계층 안에서 표시하고 권장 Scope와 그 이유를 함께 보고한다. Scope를 상위 또는 하위 계층으로 변경하는 것은 Rule Change로 취급하며 승인된 Change Control을 따른다.

## Rule Enforcement and Change Control

모든 지속적인 Rule은 적용 범위인 Scope와 별도로 적용 강도를 나타내는 Obligation을 가진다. AI는 규칙의 중요성과 실행 조건을 혼동하지 않도록 다음 세 수준으로 구분한다.

`Mandatory → Conditional → Advisory`

- **Mandatory**는 해당 Scope에서 항상 준수해야 하는 규칙이다.
- **Conditional**은 정의된 활성화 조건이 충족되었을 때 반드시 적용해야 하는 규칙이다.
- **Advisory**는 상황과 비용·효과를 고려하여 AI가 적용을 제안하거나 선택할 수 있는 권고 규칙이다.

Rule의 Obligation과 이를 구현하는 Enforcement Mechanism은 분리해서 관리한다. 규칙이 Mandatory라는 이유만으로 특정 구현 장치에 종속시키지 않는다. 규칙의 성격에 따라 Instructions, `AGENTS.md`, Skill, Hook, Validator, Approval Gate, CI 또는 기타 적절한 수단을 선택할 수 있다.

중요한 규칙일수록 자연어 지침에만 의존하지 않고 기술적으로 검증하거나 차단할 수 있는 Enforcement Mechanism의 사용을 우선 검토한다. 단, 새로운 자동화나 강제 장치는 실제 필요성과 비용을 검증한 뒤 도입한다.

AI는 Rule의 Scope, Obligation, 활성화 조건 또는 Enforcement Mechanism을 임의로 변경하지 않는다. 변경이 필요하다고 판단한 경우 다음을 포함한 Change Proposal을 먼저 제시한다.

- 현재 Scope와 Obligation
- 제안하는 변경
- 변경 이유
- 영향을 받는 Workflow, Project 또는 Task
- 기존 Rule 및 Enforcement와의 충돌 가능성
- 적용·미적용 시 예상되는 효과와 비용

Rule의 Promotion, Demotion 또는 Enforcement 강화·완화는 영향 분석과 Human Gate를 거쳐 승인된 뒤 적용한다.

반복 사용 결과 규칙의 가치가 낮거나 비용이 과도한 것으로 확인되면 `Mandatory → Conditional → Advisory` 방향으로 완화할 수 있고, 반복적인 누락이나 품질 저하가 확인되면 반대 방향으로 강화할 수 있다. 이러한 변경 역시 검증 가능한 경험을 근거로 한다.

## Governance Impact Traceability

AI는 지속적인 Rule을 새로 제안하거나 기존 Rule의 Scope, Obligation, 책임 또는 적용 위치를 변경할 때 변경 내용만 설명하지 않는다. 사용자가 해당 Rule이 전체 Framework 구조에서 어디에 위치하고 어떤 범위에 영향을 주는지 파악할 수 있도록 Traceability 정보를 함께 제공한다.

중요한 Rule의 추가·변경 보고에는 원칙적으로 다음 네 가지 정보를 포함한다.

- **Scope**: Framework, Workflow, Project, Task 전체 계층 안에서 현재 Rule의 위치를 표시한다.
- **Applied Path**: Rule 또는 관련 Canonical 정보가 실제로 반영되는 저장소와 파일 위치를 표시한다.
- **Propagation**: 해당 Rule이 어떤 하위 Workflow, Project 또는 Task까지 영향을 미치는지 표시한다.
- **Dependencies**: Rule이 어떤 상위 원칙을 따르고 어떤 하위 규칙이나 산출물에 영향을 주는지 주요 의존관계를 표시한다.

계층 관계는 대상 이름만 단독으로 제시하기보다 가능한 경우 짧은 ASCII 구조로 전체 계층 안의 현재 위치를 함께 표시한다.

예:

`Framework → Workflow → [Project] → Task`

파일 위치와 Rule의 전파 범위는 서로 다른 개념으로 취급한다. Applied Path는 정보가 저장된 위치를 나타내고, Propagation은 해당 Rule의 영향이 전달되는 범위를 나타낸다.

Traceability 표현은 구조 이해를 돕기 위한 수단이며 과도한 문서화를 목적으로 하지 않는다. 단순하거나 일회성인 Task까지 반복적으로 상세 구조를 출력할 필요는 없으며, Rule의 추가·변경·승격·강등 또는 책임 경계 변경처럼 구조적 이해가 중요한 경우에 우선 적용한다.

AI는 Traceability 정보를 통해 상위 Rule이 하위 Scope로 과도하게 전파되거나 Project·Task 고유 규칙이 Framework 수준으로 잘못 승격되는 징후도 함께 점검한다.

## Learning and Rule Promotion

하나의 Project에서 발견된 유용한 방법이나 협업 개선 아이디어를 즉시 상위 Framework Rule로 만들지 않는다. 새로운 아이디어는 먼저 Candidate Rule로 취급하고 제한된 Scope에서 실제 효과와 비용을 검증한다.

Rule의 기본 학습과 승격 lifecycle은 다음과 같다.

`Improvement Idea → Candidate Rule → Local Trial → Validated Rule → Promotion Proposal → Human Gate → Canonical Rule`

Project Scope의 Rule을 Workflow Scope로 승격할 때는 다음을 확인한다.

- 특정 Project나 기술의 조건을 제거해도 Rule이 유효한가
- 동일한 문제 해결 유형에서 반복 적용할 수 있는가
- 실제 사용 결과와 검증 가능한 근거가 존재하는가

Workflow Scope의 Rule을 Framework Scope로 승격할 때는 더 엄격한 기준을 적용한다.

- 서로 다른 Project 유형에서도 Rule이 유효한가
- 기술과 도메인에 독립적인 AI-Human Engineering 원칙인가
- 상위 Scope에서 지속적으로 적용할 실질적인 근거가 있는가

Prompt, Template, Workflow, Skill, Hook, Plugin을 포함한 재사용 또는 자동화 수단도 검증 전에 성급하게 승격하지 않는다. 기본적인 재사용 승격 방향은 다음과 같다.

`수동 규칙/Prompt → 반복 검증 → Template/Workflow → 다수 Project 검증 → Skill/Automation`

구체적인 Skill 제작법이나 Plugin 구현법은 이 Governance 문서에서 정의하지 않는다. Rule의 Promotion과 Demotion은 `Rule Enforcement and Change Control`을 따르며, 영향 분석과 Human Gate를 거쳐 승인된 뒤 Canonical 상태에 반영한다.

## Verification and Session Accountability

중요한 작업 세션은 단순한 실행 완료로 끝내지 않는다. 세션의 상위 lifecycle은 다음과 같다.

`Orient → Explore → Propose → Human Gate → Execute → Verify → Promote → Handoff`

모든 세션이 모든 단계를 반드시 수행해야 하는 것은 아니다. 단순 조회나 작은 작업에는 목적과 위험에 필요한 단계만 적용할 수 있다. 중요한 설계, Canonical Document 변경, 여러 파일에 걸친 변경 또는 Rule 변경처럼 지속적인 영향을 주는 작업에는 검증과 상태 반영이 필요하다.

- **Verify**에서는 수행 결과가 승인된 목표와 검증 기준을 충족하는지 확인한다.
- **Promote**에서는 세션에서 확정된 지속적인 정보가 적절한 Canonical Document에 반영됐는지 확인한다.
- **Handoff**에서는 다음 세션이 과거 Chat 전체를 다시 읽지 않아도 현재 상태, 완료된 결정과 필요한 다음 맥락을 이해할 수 있도록 한다.

Session Record는 사고 과정과 작업 이력을 보존하지만 그 자체로 Canonical Design이 아니다. 지속되어야 하는 Decision과 Design은 적절한 Canonical Document로 승격해야 한다.

중요한 세션을 종료할 때는 필요에 따라 다음 Artifact Boundary를 검토한다.

- Research가 Design으로 잘못 승격되지 않았는가
- Hypothesis나 Proposal이 승인된 Decision처럼 기록되지 않았는가
- Implementation Plan이 Architecture를 임의로 변경하지 않았는가
- Project-specific Rule이 Framework Scope로 잘못 승격되지 않았는가
- 지속되어야 하는 Decision이 Canonical Document에 반영됐는가

구체적인 Handoff Template이나 Reviewer 구현 방식은 이 Governance 문서에서 정의하지 않는다.
