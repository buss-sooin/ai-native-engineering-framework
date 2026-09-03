# Project AI Capability & Collaboration Bootstrap Workflow v0.1

Status: Effective

Effective Date: 2026-09-03

## 목적과 Governance 위치

이 문서는 프로젝트 또는 장기 작업에 필요한 협업 구조를 초기 구성(Bootstrap)하고 재사용하기 위한 Workflow-level Canonical Definition이다. 세션 역할(Session Role), 실행 환경(Execution Surface), 역량(Capability), 사람·AI 책임, 권한 및 실행 경계(Authority / Execution Boundary), 인계와 반환(Handoff / Return)을 필요한 수준에서 정한다.

- 범위(Scope): Workflow
- 상위 권한 근거(Parent Authority): [AI Engineering Guidelines](../../governance/AI-ENGINEERING-GUIDELINES.md), Status: Effective
- 적용 원칙: `Canonical Context Authority`, `Engineering Phase and Decision Governance`, `AI Capability and Collaboration Governance`, `Information and Artifact Lifecycle`, `Rule Scope Classification`, `Rule Enforcement and Change Control`, `Verification and Session Accountability`

이 Workflow는 해당 원칙을 프로젝트 운영에 구체화한다. 상위 Governance의 의미, 권한 계층, 사람 승인 관문(Human Gate) 기준, 최소 권한(Least Privilege), 사람의 최종 책임과 검증 책임을 변경하지 않는다. 협업 구조의 초기 구성이 끝나면 기존 엔지니어링 또는 개별 Workflow 실행으로 이어진다.

## 조건부 활성화와 적용 수준

활성화 조건은 다음 하나로 정의한다. **프로젝트 협업의 복잡성이 반복되거나, 역량 선택·책임 배분·실행 라우팅이 엔지니어링 결과, 권한·위험 또는 검증에 의미 있는 차이를 만드는 경우 이 Workflow를 필요한 수준에서 적용한다.**

다음은 활성화 여부와 적용 수준을 판단할 때 확인할 협업 특성이다. 각각을 모든 프로젝트의 필수 구성요소로 요구하지 않는다.

- 여러 세션 역할이나 실행 환경을 사용한다.
- 역량 선택에 따라 결과, 권한, 위험 또는 검증이 의미 있게 달라진다.
- 사람·AI 책임을 명시적으로 배분할 필요가 있다.
- 세션 또는 실행 환경 사이의 인계가 반복된다.
- 저장소, 외부 시스템 또는 실행 환경의 상태를 변경한다.
- 실행 결과를 별도의 검증·종료 책임으로 반환해야 한다.
- 여러 작업에서 같은 협업 구조를 재사용한다.

전체 초기 구성(Full Bootstrap)의 적용 깊이는 목적과 협업 복잡성에 비례한다. 단순 질문, 일회성 읽기 전용 분석, 위험이 낮은 단일 세션 작업에는 전체 초기 구성 산출물을 요구하지 않으며 필요한 라우팅 판단만 수행할 수 있다. 이 Workflow의 성격은 조건부·비례적 적용(Conditional / Proportional)이며, 간소한 적용도 상위 Governance의 권한·검증 의무를 완화하지 않는다.

## 개념과 경계

| 개념 | 의미와 경계 |
| --- | --- |
| 프로젝트 / 작업 공간(Project / Workspace) | 프로젝트 맥락과 관련 세션·작업을 담는 상위 컨테이너다. 특정 제품의 프로젝트, 저장소 UI 또는 공급자 작업 공간에 종속되지 않으며, 소속 자체는 실행 권한을 부여하지 않는다. |
| 세션 역할(Session Role) | 현재 협업에서 세션이나 작업이 맡는 책임이다. 하나의 세션이 여러 역할을 맡거나 같은 역할을 서로 다른 실행 환경에서 수행할 수 있다. |
| 실행 환경(Execution Surface) | 실제 역량이 제공되고 행위가 수행되는 환경이다. 역할이나 제품 이름만으로 그 역량과 실행 의미를 추정하지 않는다. |
| 역량(Capability) | 현재 목적에 사용할 수 있는 수행 능력이다. 하나의 실행 환경이 여러 역량을 제공하고, 같은 역량이 여러 실행 환경에 존재할 수 있다. |
| 권한 및 실행 경계(Authority / Execution Boundary) | 적용 가능한 정본 권한 근거와 승인에 따라 허용된 행위·접근·범위 및 제한이다. 역량의 가용성이나 선택과 별도로 확인한다. |

다음 관계를 유지한다.

`Role ≠ Surface` · `Surface ≠ Capability` · `Capability ≠ Authority` · `Workspace ≠ Authority`

`Available ≠ Selected ≠ Authorized`

역할의 설명용 예로 협업 조율(Orchestration), 설계, 검토, 학습, 실행, 검증, 문서화와 종료가 있다. 실행 환경의 설명용 예로 대화형 추론 환경, 저장소·파일 접근 환경, 코딩 에이전트 환경, 사람이 사용하는 IDE·터미널, 전문 외부 도구와 연결 애플리케이션 환경이 있다. 역량의 설명용 예로 추론, 저장소 조사, 파일 변경, 명령 실행, 브라우저·외부 자료 조사, 연결 애플리케이션 상호작용, 산출물 생성과 실행 시점의 상태 관측이 있다. 이 예시들은 고정 열거형이나 필수 분류 체계가 아니다.

UI의 Section 같은 조직화·그룹화 기능은 작업을 묶어 보여주는 수단일 뿐, 권한·실행 의미·역량·승인 상태를 부여하는 거버넌스 기본 개념(Governance Primitive)이 아니다. 특정 제품 이름과 플랫폼별 대응 관계는 프로젝트 맥락에서만 관리하며 Workflow 규칙에 고정하지 않는다.

## 초기 구성 생명주기

`Orient → Assess → Allocate → Route & Bound → Define Handoff / Return → Verify Bootstrap`

이 생명주기는 협업 초기 구성의 책임을 나타내며 Framework의 엔지니어링 생명주기나 개별 Workflow의 생명주기를 대체하거나 확장하지 않는다.

### 1. 맥락 확인(Orient)

프로젝트 목표, 엔지니어링 의도(Engineering Intent), 정본 권한 근거(Canonical Authority), 범위, 주요 제약과 협업 맥락을 필요한 수준에서 확인한다. 현재 적용 상태가 확인된 정본 산출물을 기준으로 하며 모든 저장소나 역량을 빠짐없이 조사하는 단계로 사용하지 않는다.

### 2. 평가(Assess)

현재 목적에 필요한 역량과 실제 가능한 선택지를 평가한다. 최소 판단 관점은 필요 역량, 권한·접근 범위, 데이터 노출, 변경 필요성, 위험(Risk)·영향 범위(Blast Radius), 가역성(reversibility), 관측 가능성(Observability)·검증(Verification), 사람의 직접 참여 필요성이다. 각 관점의 검토 깊이는 작업에 비례한다.

### 3. 책임 배분(Allocate)

필요한 수준에서 다음 책임을 구분한다.

- 의사결정 권한(Decision Authority)
- 실행 책임(Execution Responsibility)
- 검증 책임(Verification Responsibility)
- 후속 실행 권한(Continuation Authority)

각 책임을 항상 서로 다른 사람이나 세션이 맡아야 한다는 의미는 아니다. 사람과 AI가 맡을 책임을 식별하되 사람의 최종 책임을 AI에 이전하지 않는다.

### 4. 실행 배정과 경계 확인(Route & Bound)

작업 특성과 필요 역량에 맞는 실행 환경 및 사람·AI 책임 배분을 선택한다. 그 후 실행 권한, 접근 범위, 승인된 실행 경계, 금지 행위와 적용 가능한 중단 조건을 별도로 확인한다. 환경이나 역량의 선택 자체는 승인이 아니다. 권한·데이터 취급 조건의 불명확성이나 해결되지 않은 정본 충돌은 상위 Governance의 중단·보고·사람의 판단과 해결(Human Resolution) 기준으로 처리한다.

### 5. 인계와 반환 정의(Define Handoff / Return)

역할이나 실행 환경 사이의 이동이 필요하면 목적지 역할, 실행 환경, 필요한 맥락, 기대 결과(Expected Result), 반환·종료 목적지(Return / Closure Destination)를 정한다. 아래 인계 계약의 활성화 조건이 충족되면 최소 인계 맥락을 보존한다.

### 6. 초기 구성 검증(Verify Bootstrap)

초기 구성의 완료 전에 다음을 확인한다.

- 필요한 역량을 선택한 실행 환경에서 실제로 수행할 수 있다.
- 세션 역할과 실행 환경이 구분되어 있다.
- 역량의 가용성·선택과 실행 권한이 구분되고 적용 가능한 실행 경계가 확인되어 있다.
- 사람의 책임과 직접 참여가 부당하게 제거되지 않았다.
- 검증 책임이 존재한다.
- 필요한 인계·반환 경로가 연결되어 다음 책임자와 반환·종료 목적지를 식별할 수 있다.

충족되지 않은 항목은 관련 초기 구성 판단으로 돌아가 해결한다. 초기 구성 완료는 후속 작업 자체의 성공이나 새 실행 권한의 부여를 뜻하지 않는다. 완료 후 기존 엔지니어링 또는 개별 Workflow의 실행·검증 기준을 따른다.

## 역량과 실행 환경 라우팅

라우팅 판단은 다음 순서로 수행한다.

`Work Characteristics → Capability Requirement → Feasible Surface → Collaboration Fit → Responsibility Allocation → Authority Check → Return Routing`

즉, 작업 특성에서 필요 역량을 도출하고 가능한 실행 환경을 찾은 뒤 협업 적합성을 평가한다. 책임을 배분하고 권한을 확인한 다음 결과의 반환 경로를 연결한다. 이 순서는 초기 구성 생명주기를 대체하는 별도 실행 생명주기가 아니다.

필요한 판단에는 추론, 저장소·파일 접근, 변경, 명령 실행, 외부 조사, 연결 애플리케이션, 산출물 생성, 실행 시점의 상태 관측, 맥락 연속성, 권한·접근, 데이터 노출, 실행 자율성, 위험·영향 범위·가역성, 관측 가능성·검증, 사람의 학습·판단 요구를 포함할 수 있다. 특정 실행 환경을 항상 우선하는 계층을 두지 않는다. 최소 권한은 현재 작업에 필요한 행위와 접근 범위를 기준으로 적용하며, 더 강한 역량을 선택했다는 이유로 검증 요구를 낮추지 않는다.

### 사람의 직접 엔지니어링 수행(Human Direct Engineering)

사람의 직접 수행은 정상적인 실행 선택지다. 코드·설정을 따라가며 이해하는 것이 목적에 포함되거나 실행 시점의 동작·근거를 직접 확인하는 것이 판단 품질을 높일 때 적절할 수 있다. 사람의 판단이 핵심인 작업, 사람이 수행하는 편이 더 단순하고 안전한 작업, 위험이 크거나 비가역적·고영향인 작업, 학습 자체가 엔지니어링 목표인 작업에서도 선택할 수 있다.

AI가 기술적으로 수행할 수 있다는 이유만으로 사람의 직접 작업을 제거하지 않는다. 사람 직접 수행, AI 자문, AI 분석 후 사람 실행, 제한된 AI 실행 등은 협업 선택지이며 성숙도 계층이 아니다. 자동화 수준이나 AI 사용량 자체를 더 나은 협업의 기준으로 삼지 않는다.

### 협업 조율 책임과 전담 Control Plane

여러 역할이나 실행 환경을 연결하는 협업에는 필요한 수준의 조율 책임이 명확해야 한다. 조율 책임은 현재 상태(Current State), 현재 관문(Current Gate), 다음 책임, 인계 목적지와 반환·종료 목적지를 추적할 수 있다.

전담 Control Plane 세션은 조건부로 선택할 수 있는 권고(Advisory) 구현 방식이다. 여러 세션·실행 환경을 사용하는 장기 프로젝트, 여러 Workflow 병행, 여러 중요한 사람 승인 관문, 반복되는 상태·라우팅 유실에서 유용할 수 있다. 모든 프로젝트의 필수 구성요소가 아니며 이 Workflow는 별도의 세션 조율 Workflow(Session Orchestration Workflow)를 정의하지 않는다.

## 인계 계약(Handoff Contract)

다음 중 하나 이상이 발생하는 인계에 계약을 적용한다.

- 세션 역할 변경
- 실행 환경 변경
- 실행 의미(execution semantics) 변경
- 변경 권한(mutation authority)의 차이
- 책임자 변경
- 중요한 맥락이 다른 세션으로 이동
- 검증·종료 책임으로 결과 반환

역할·환경·권한·책임 또는 중요한 맥락의 이동이 없는 같은 세션 안의 작은 단계 변경에는 강제하지 않는다.

### 최소 인계 맥락

계약이 활성화되면 필요한 수준의 상세도로 다음을 보존한다.

1. 프로젝트 / 작업 공간(Project / Workspace)
2. 목적지 세션 역할(Destination Session Role)
3. 실행 환경(Execution Surface)
4. 엔지니어링 목표(Engineering Objective)
5. 현재 상태 / 현재 관문(Current State / Current Gate)
6. 적용 가능한 정본 권한 근거 또는 대상(Applicable Canonical Authority / Target)
7. 승인된 실행 경계 또는 권한 상태(Approved Execution Boundary / Authority Status)
8. 요구되는 책임(Required Responsibility)
9. 금지 행위 / 범위 밖 행위(Prohibited / Out-of-scope Action)
10. 검증 / 기대 결과(Verification / Expected Result)
11. 반환·종료 목적지(Return / Closure Destination)

대상 저장소, 대상 산출물, 특정 역량 요구, 사람 책임, AI 책임, 중단 조건, 근거 요구사항, 승인 참조, 추론 수준, 브랜치·리비전·환경, 미해결 문제는 적용되는 경우에만 추가한다. 별도 Template 파일을 요구하지 않는다.

다음 책임자는 무엇을 하는지, 어디에서 하는지, 어디까지 허용되는지, 무엇이 금지되는지, 성공을 어떻게 판단하는지, 결과를 어디로 반환하는지 다시 추측하지 않아야 한다.

### 모호한 목적지 표현 방지

역량, 변경 권한 또는 실행 의미가 다른 환경으로 라우팅하거나 인계할 때는 **세션 역할과 실행 환경을 각각 명시한다.** `Chat`, `session`, `workspace` 같은 일반 표현만으로 목적지를 지정하지 않는다. 이 규칙은 실행의 정확성을 위한 것이며 특정 제품의 이름 규칙이 아니다. 제품 이름이 필요한 구체적인 대응 관계는 프로젝트 맥락에서만 식별한다.

## 재사용과 영향 부분 재평가

`Reuse Valid Collaboration Structure → Re-evaluate Affected Part on Trigger`

유효한 협업 구조를 재사용하고 매 작업마다 초기 구성을 처음부터 반복하지 않는다. 다음과 같은 실질적인 협업 변화가 있으면 영향을 받은 판단만 필요한 수준에서 재평가한다.

- 엔지니어링 의도의 중요한 변경 또는 새로운 Workflow 도입
- 새로운 실행 환경·연결 시스템의 도입 또는 권한·접근 범위 변경
- 위험·영향 범위의 의미 있는 변경
- 반복되는 협업·라우팅 실패
- 새로운 관련 역량 또는 플랫폼·도구 가용성의 변경
- 검증 역량 또는 사람의 학습·판단 목표 변경
- 기존 실행 환경이 필요 역량을 더 이상 제공하지 못함

영향 부분 재평가(Targeted Re-evaluation)를 허용하며 항상 전체 초기 구성을 반복하지 않는다. 재평가 자체가 새 사람 승인 관문을 의미하지 않는다. 엔지니어링 의도, 범위, 권한·접근, 위험·영향 범위, 비가역적·고영향 행위 또는 승인된 실행 경계의 실질적 변경 여부를 상위 Governance 기준으로 별도 판단한다.

## 산출물과 다른 Workflow의 경계

v0.1의 필수 정본 산출물은 이 Workflow Definition 하나다. 활성화, 개념, 생명주기, 라우팅, 책임, 인계와 재평가의 의미 요구사항을 이 문서에서 관리한다.

프로젝트 협업 프로필(Project Collaboration Profile)은 조건부 프로젝트 산출물(Conditional Project Artifact) 후보일 뿐이다. 여러 작업에 걸친 구조 재사용, 여러 실행 환경 사용, 같은 라우팅 판단의 반복, 지속적인 책임 배분 관례가 생길 때 필요성을 검토할 수 있다. 플랫폼 역량 프로필(Platform Capability Profile)도 필수 산출물이 아니다. 전체 역량 목록을 지속적으로 유지하도록 요구하지 않는다.

v0.1에서는 프로젝트·플랫폼 프로필이나 해당 Template, 초기 구성 기록(Bootstrap Record), 역량 목록 산출물, `templates/HANDOFF.md`, 세션 조율 Workflow, 새로운 세션 기록 분류 체계를 만들지 않는다. 특정 제품·플랫폼의 대응 관계를 이 Definition에 고정하지 않는다.

[Failure Reproduction Workflow](../failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW.md)의 `FRW-R01`~`FRW-R15`, 특히 `FRW-R09`·`FRW-R11`, 제한된 후속 실행 묶음(Grouped Bounded Continuation), `Define → Reproduce → Verify → 인계(Handoff)` 생명주기와 [Conformance Record](../failure-reproduction/FAILURE-REPRODUCTION-WORKFLOW-CONFORMANCE.md)는 이 Workflow로 변경하지 않는다. 프로젝트별 협업·권한 제약은 FRW의 허용 실행 경계를 더 좁힐 수 있으며 FRW는 해당 제약을 우회할 수 없다. 이는 새 권한 계층을 만드는 것이 아니다.

## 규칙과 의무(Rules and Obligations)

아래 여섯 규칙의 범위는 모두 `Workflow`다. 의무(Obligation)와 활성화 조건(Activation Condition)을 분리하며 앞의 운영 설명은 이 규칙들을 구체화한다.

| Rule ID / 이름 | Scope | Obligation | Activation condition | 규칙 |
| --- | --- | --- | --- | --- |
| PCBW-R01 — Proportional Activation | Workflow | Conditional | 프로젝트 협업의 복잡성이 반복되거나, 역량 선택·책임 배분·실행 라우팅이 엔지니어링 결과, 권한·위험 또는 검증에 의미 있는 차이를 만드는 경우 | Workflow를 필요한 수준에서 적용한다. 단순 작업에 전체 초기 구성(Full Bootstrap)을 강제하지 않는다. |
| PCBW-R02 — Concept Separation | Workflow | Mandatory | Workflow 활성화 시 | 프로젝트 / 작업 공간(Project / Workspace), 세션 역할(Session Role), 실행 환경(Execution Surface), 역량(Capability), 권한 및 실행 경계(Authority / Execution Boundary)를 구분한다. 작업 공간 소속이나 실행 환경·역량의 가용성은 실행 권한이 아니다. `Available ≠ Selected ≠ Authorized`를 유지한다. |
| PCBW-R03 — Capability-Aware Routing | Workflow | Mandatory | Workflow 활성화 시 | 필요 역량과 협업 적합성을 평가한 뒤 실행 환경(Execution Surface)과 사람·AI 책임을 선택하고 실행 권한을 별도로 확인한다. 특정 실행 환경을 항상 우선하는 계층을 만들지 않는다. |
| PCBW-R04 — Human Direct Engineering | Workflow | Mandatory | Workflow 활성화 시 | 사람의 직접 엔지니어링 수행(Human Direct Engineering)이 이해·판단·학습·위험 통제 또는 실행 단순성에 더 적합하면 정상적인 실행 선택지로 선택할 수 있다. AI 역량의 존재만으로 사람의 직접 작업을 제거하지 않는다. |
| PCBW-R05 — Bounded Handoff | Workflow | Conditional | 역할·실행 환경 사이의 인계 또는 맥락·권한·책임 손실 위험이 있는 인계 발생 시 | 다음 책임자가 현재 상태, 실행 경계, 검증 요구와 반환 목적지를 추측하지 않도록 인계 계약(Handoff Contract)의 맥락을 보존한다. 역량·변경 권한·실행 의미가 다른 환경으로 이동할 때 세션 역할(Session Role)과 실행 환경(Execution Surface)을 각각 명시하며 일반적인 `Chat` 표현만으로 목적지를 지정하지 않는다. |
| PCBW-R06 — Targeted Re-evaluation | Workflow | Conditional | 엔지니어링 의도, Workflow, 실행 환경, 역량 가용성, 권한·접근, 위험, 검증 또는 협업 효과에 실질적 변화 발생 시 | 영향을 받은 초기 구성 판단을 필요한 수준에서 재평가한다. 재평가 자체는 새 사람 승인 관문(Human Gate)을 뜻하지 않으며 승인 경계 변경 여부는 상위 Governance에 따라 별도 판단한다. |

## 승인과 정본화 근거

- 승인 설계: `55 — Project AI Capability & Collaboration Bootstrap Workflow Design`
- 승인 참조: 권한 있는 사용자가 제공한 `# 55 — Project AI Capability & Collaboration Bootstrap Workflow Canonicalization` 실행 지시의 사람 승인 관문 `PASS` 및 `HG-55-01`~`HG-55-06` 승인 명시
- 승인 범위와 조건: Design 55를 Workflow Definition 하나로 정본화하고, 의미 적합성 검증과 정본 상태 확인을 통과하면 `Effective`로 처리한다. README의 최소 색인 추가 및 커밋·원격 동기화를 포함하며 상위 Governance와 FRW는 변경하지 않는다.

상위 Governance는 권한 있는 사람의 승인과 추적 가능성을 요구하며, 모든 Workflow에 별도 Conformance 파일을 요구하지 않는다. 기존 FRW의 Definition·Template·Conformance Record 구성을 새 Workflow에 자동 적용하지 않는다. 이 문서는 위 승인 범위 안에서 Design 55의 의미와 여섯 규칙을 검증하여 정본화했으며, v0.1의 산출물 최소화에 따라 별도 Conformance 파일을 만들지 않는다. AI는 승인 주체가 아니며 사용자가 제공한 승인을 대체하거나 확대하지 않았다.
