# Collaboration Routing Engine v0 및 Operator-mediated Integration

Status: Operator-mediated Project-level Local Trial Integration

## 목적과 승인 경계

이 도구는 구조화된 필수 행위에서 필요한 역량과 실행 환경(Execution Surface)을 결정하고, 사람·AI 책임 및 실행 권한을 별도로 검증한다. 검증된 라우팅 결과(Routing Result)를 기계 소비용 계약으로 반환하며 `PASS`에서만 Markdown 지시문을 생성한다. 명령·Git 작업·런타임 조작을 실제 수행하지 않는다.

승인된 통합 로컬 시험은 독립 구현된 Engine 앞뒤에 얇은 통합 어댑터(Integration Adapter)를 둔다. Adapter는 요청을 검증하고 기존 Engine과 Renderer를 순서대로 호출한 뒤, Renderer를 호출하지 않는 독립 지시문 검증기(Directive Validator)가 결과와 Markdown의 의미 일치를 확인한 경우에만 사람이 붙여 넣을 수 있는 지시문을 반환한다. 이는 ChatGPT-native mandatory interceptor가 아니라 운영자가 명시적으로 실행하는 프로젝트 수준 흐름이다.

- 적용 프로젝트: `AI-Native Engineering Framework Lab`
- 승인 설계: `62 — AI-Native Collaboration Routing Engine v0 Design`
- 승인 근거: 사용자가 제공한 `63 Implementation Directive`의 `HG-62-01 — PASS` 및 후속 Resume의 `PASS / remains valid`
- 승인 범위: 프로젝트 수준의 로컬 시험 구현, 스키마·프로필·CLI·회귀 검증·최소 사용 문서
- 구현 브랜치: `feat/collaboration-routing-v0`
- 시작 리비전: `d934887ce0530ef0ad6b775b42092903fc022002`
- 반환 목적지: `00B — AI-Native Engineering Framework Control Plane`

통합 로컬 시험의 추가 승인 설계는 `66 — AI-Native Collaboration Routing Engine v0 Integration Boundary Design`, 승인 참조는 `HG-66-01 — Collaboration Routing Integration Local Trial Implementation`, 구현 브랜치는 `feat/collaboration-routing-integration-v0`, 시작 리비전은 `bf71895f6183772005d3d76134df57be7399b60b`다. 이 승인은 standalone Engine의 판단 의미 변경을 허용하지 않는다.

PCBW-R07 집행 확장의 승인 설계는 `67 — PCBW AI Execution Continuity & Human Interruption Boundary Design`, 승인 참조는 `HG-67-01 = PASS`다. 승인 범위는 PCBW-R07 정본화, 기존 action 계약의 최소 확장, 결정론적 사람 위임 판정과 기존 PASS-only 방출 관문의 연계다. 상위 Governance, Failure Reproduction Workflow, 자동 orchestration과 실행 어댑터는 범위에 포함하지 않는다.

적용 정본은 [AI Engineering Guidelines](../../governance/AI-ENGINEERING-GUIDELINES.md)와 [Project Collaboration Bootstrap Workflow](../../workflows/project-collaboration-bootstrap/PROJECT-COLLABORATION-BOOTSTRAP-WORKFLOW.md)다. 이 디렉터리의 코드·프로필·결과는 해당 문서를 대체하거나 Framework·Workflow 규칙을 변경하지 않는다. 한국어 문서는 [Technical Documentation Guidelines](../../governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md)를 따른다.

## 실행 방법

Python 3.8 이상의 표준 라이브러리만 사용한다. 외부 패키지 설치와 서비스 연결이 없다. 아래 명령은 저장소 루트에서 실행한다.

```sh
python3 tools/collaboration-routing/src/cli.py route \
  --request tools/collaboration-routing/tests/fixtures/inspection.request.json \
  --profile tools/collaboration-routing/profiles/framework-lab.v0.4.0.json

python3 tools/collaboration-routing/src/integration_cli.py \
  --request tools/collaboration-routing/tests/fixtures/inspection.request.json \
  --profile tools/collaboration-routing/profiles/framework-lab.v0.4.0.json

python3 -m unittest discover -s tools/collaboration-routing/tests -v
```

CLI는 표준 출력에 JSON 객체 하나를 반환한다. 종료 코드는 `PASS=0`, `FAIL=1`, `UNRESOLVED=2`다. 잘못된 CLI 옵션은 argparse의 사용법 오류로 종료한다. 도구 자체는 출력 파일을 만들거나 원격 전송하지 않는다.

| 출력 필드 | 의미 |
| --- | --- |
| `routing_status` | 전체 검증 결과 |
| `failure_codes` | 확인된 계약 위반 |
| `unresolved_issues` | 확정할 수 없는 입력·가용성·권한·검증기 상태 |
| `resolution_action` | 입력 수정, PCBW-R06 영향 부분 재평가 또는 사람의 판단 후 재검증 안내 |
| `targeted_re_evaluation` | `INVALID_HUMAN_DELEGATION`에 대한 PCBW-R06 재평가 대상 action과 적합한 AI 후보 |
| `result` | 유효한 입력으로 구성한 구조화된 결과. 입력 형식 오류나 검증기 오류 시 `null` |
| `directive` | 검증된 `PASS` 지시문. 그 밖의 모든 경우 `null` |

통합 CLI는 위 필드와 함께 `integration_status`, `directive_validation`, `emission_outcome`, `evidence`를 반환한다. `PASS + 독립 지시문 검증 PASS`만 `EMITTED`가 될 수 있다. Engine이 반환한 의미적 `FAIL`·`UNRESOLVED`는 `BLOCKED_BY_ROUTING`으로 보존한다. 요청 직렬화, Adapter, Engine 호출, Renderer 또는 Validator 장애와 결과·지시문 불일치는 별도의 `INTEGRATION_BLOCKED`이며 종료 코드 `3`을 사용한다. 이 상태는 Design 62의 Routing Result 상태를 확장하거나 바꾸지 않는다.

`FAIL`·`UNRESOLVED`의 `result`에는 진단을 위한 실행 계획 후보가 남을 수 있다. 이 후보는 실행 가능한 지시문이 아니며 상태를 무시하고 소비해서는 안 된다.

예제는 **읽기 전용 요청 형식 예시**다. 대상 문자열·상태·검증 책임자·리비전을 실제 값으로 교체해야 한다. 테스트의 승인 참조는 가상 데이터이며 실제 실행 승인이 아니다.

## 구성과 책임 분리

```text
Structured Request → Schema Validation → Capability Resolution
 → Profile / Feasible Surface → Plan / Responsibility
 → Authority / Boundary → Internal Conformance → Status
 → PASS only → Renderer → Rendered Conformance
```

통합 로컬 시험의 방출 흐름은 다음과 같다.

```text
Routing Request → Integration Adapter → Request Validation
 → Existing Deterministic Engine → Independent Complete-result Revalidation
 → Existing Renderer → Independent Directive Validator
 → Result-bound Validation PASS only → Human-visible Pasteable Directive
```

책임 경계는 분리되어 있다. standalone Routing Engine은 결정과 의미 상태를 소유한다. Adapter는 호출 순서와 방출 차단만 담당하며 경로·권한·추천을 선택하거나 덮어쓰지 않는다. Renderer는 검증된 결과를 Markdown으로 투영한다. 독립 Validator는 Renderer를 재호출하지 않고 헤더, 제목, 필수 인계 맥락, 실행 환경, 역할, 책임, 권한, 추천과 반환 목적지를 구조적으로 파싱해 Routing Result와 대조한다. 지시문은 사람에게 보이는 산출물일 뿐 실행이 아니며, downstream execution은 이 구현 범위 밖이다.

| 파일 | 책임 |
| --- | --- |
| `schemas/routing-request.schema.json` | 필수 행위와 명시적 입력 상태 |
| `schemas/project-routing-profile.schema.json` | 프로젝트의 행위·역량·환경 매핑 |
| `schemas/routing-result.schema.json` | 기계 소비용 결과 계약 |
| `profiles/framework-lab.v0.4.0.json` | Framework Lab의 PCBW-R07 신뢰 Human 책임·action handoff·운영 인터페이스·가용성 선언 |
| `project-integration/framework-lab.reusable-directive-emission.v0.1.0.json` | 실제 Project Instructions에 동기화할 재사용 지시문 방출 의무와 저장소/플랫폼 경계 |
| `src/schema_validation.py` | 번들 스키마에서 사용하는 JSON Schema 부분집합 검증 |
| `src/engine.py` | 라우팅, 책임 배분, 권한·경계 검증 및 내부 적합성 검사 |
| `src/directive.py` | 결정론적 표현과 지시문 적합성 검증 |
| `src/cli.py` | 로컬 입력 및 JSON 출력 |
| `src/directive_conformance.py` | Renderer와 독립적인 지시문 구조·의미 검증 |
| `src/integration.py` | Engine 의미를 변경하지 않는 호출 조율과 fail-closed 방출 관문 |
| `src/integration_cli.py` | 운영자 매개 통합 흐름의 로컬 JSON 입출력 |
| `tests/fixtures/` | 예제 요청, 고정 회귀 A–I와 역사적 지시문 실패 fixture |
| `tests/test_routing.py` | 정상·오류·변조·CLI 검증 |
| `tests/test_integration.py` | 계약 보존, 역사적 실패, 장애 주입과 방출 차단 검증 |

요구사항 추출(Requirement Extraction)은 호출자의 책임이다. Engine은 자연어 목표나 본문에서 명령을 추출하지 않으며 `required_actions[]`만 행위 판정의 입력으로 사용한다. 목표·행위·대상 간 자연어 의미의 정확성은 요청 작성자와 검토자가 확인해야 한다.

`Routing Decision ≠ Authority`, `Routing Result ≠ Directive`, `Directive ≠ Execution`을 유지한다. 운반 어댑터(Execution Adapter)는 포함하지 않는다.

통합 Adapter는 Routing Request의 자연어로 결정 필드를 다시 만들지 않는다. 실행 환경, 세션 역할, 책임, 권한 평가, 모델·추론 추천과 Route Leg는 검증된 Routing Result만 따른다. Adapter는 Engine이 `PASS`를 반환해도 원본 요청·프로필에서 결과를 다시 계산해 완전 일치를 확인한다. 독립 Directive Validator의 `PASS`에는 `routing_result_id`, 의미 지문과 지시문 지문이 결합되어야 한다. 일반 요청 맥락은 Engine이 보존한 `source_request`에서 읽지만, PCBW-R07 Human Execution Responsibility의 필수 설명과 인터페이스는 `source_profile`의 신뢰 선언과 해석된 Route Leg에서 생성한다. `Available ≠ Selected ≠ Authorized`와 `Recommended ≠ Selected ≠ Authorized`를 유지한다.

## 통합 실패 차단과 근거

의미적 `FAIL`·`UNRESOLVED`는 기존 Engine의 진단과 해결 경로를 그대로 반환하고 Renderer를 호출하지 않는다. 통합 인프라 실패는 `INTEGRATION_BLOCKED`로 구분하며 유효한 `PASS` 결과가 없는 경우, Renderer가 실패한 경우 또는 독립 Validator가 거부한 경우 항상 `directive=null`이다. Adapter는 실패를 Engine의 의미 상태로 승격·강등하지 않고 승인이나 누락된 권한을 합성하지 않는다.

통합 근거 메타데이터는 요청, 결과, 렌더링된 지시문과 Validator 결과의 SHA-256 지문, 요청·결과 ID 및 최종 방출 상태를 포함한다. 차단된 렌더링 결과는 실행 가능한 지시문 필드로 노출하지 않고 지문만 보존한다. 이 지문은 전자서명, 승인 또는 실행 권한이 아니며 Design 62 스키마에는 저장되지 않는다.

역사적 실패 fixture는 누락·후치 Routing Header, Role/Surface 혼동, 잘못된 Surface, Result/Directive Surface 불일치, 권한 강화와 필수 인계 맥락 누락을 의도적으로 주입한다. Renderer가 평소 올바른 출력을 만든다는 사실과 별개로 독립 Validator가 각 변조를 거부하는지 검증한다.

통합 구현 검증 시 전체 61개 테스트가 통과했다. 기존 standalone 49개와 통합 12개를 함께 실행했으며, Regression A–I, 정상 단일·AI/Human 복합 경로, 의미적 `FAIL`·`UNRESOLVED`, 통합 장애 주입, 계약 보존, 결과·지시문 drift, 독립 Validator 및 결정론적 근거 지문을 포함한다.

## 요청 계약과 명시적 상태

판정에 필요한 값은 다음 형태를 사용한다. `UNKNOWN`이나 `NOT_REQUIRED`에 `value`를 추가하면 스키마 위반이다. 누락·`null`·빈 문자열은 상태를 대신하지 않는다.

```json
{"state":"KNOWN","value":"confirmed value"}
{"state":"UNKNOWN"}
{"state":"NOT_REQUIRED"}
```

필수 맥락은 프로젝트, 제목, 목표, 세션 역할, 대상, 현재 상태·관문, 정본 참조, 실행 경계, 금지 행위 목록, 의사결정·검증 책임자, 검증 계약과 반환 계약이다. 이 필드의 `UNKNOWN`은 `UNRESOLVED`, `NOT_REQUIRED`는 계약 모순이다. 금지 행위가 없으면 `KNOWN`과 빈 배열로 명시한다. `return_contract.value`는 반환 목적지 `destination`과 행위별 `human_action_returns[]`를 가진다. 각 Human action의 반환 종류는 action 자체의 `human_return_responsibility.value.kind`와 일치해야 하며, 누락·불일치 또는 AI action에 대한 Human 반환 선언은 계약 위반이다.

중단 조건·근거 요구·브랜치/리비전/환경은 적용되지 않을 때 `NOT_REQUIRED`를 허용한다. 적용 여부를 아직 모르는 `UNKNOWN`은 보수적으로 `UNRESOLVED`다. `surface_selection=NOT_REQUIRED`는 명시적 선택 없이 프로필로 선택하라는 뜻이다. `KNOWN`이면 모든 action ID를 한 번씩 지정해야 한다.

각 필수 행위는 `id`, `kind`, `target`, `effects`, `source_references`, `actor`, `human_direct`, `session_role`, `verification_requirement`, `authority`, `approval_reference`를 가진다. PCBW-R07 확장 필드는 `human_necessity_basis`, `human_return_responsibility`, `targeted_re_evaluation_established`, `human_facing_semantics`다. `human_direct`는 사람이 직접 수행하는지 명시하며 `actor`와 일치해야 한다. AI 실행에는 네 확장 필드를 생략하거나 `NOT_REQUIRED`로 선언할 수 있다. 사람 실행에는 사람 필요성 근거(Human Necessity Basis), 행위에 결합된 사람 반환 책임(Human Return Responsibility)과 사람 대상 운영 의미가 의미상 필수다. Human action의 `human_necessity_basis={"state":"NOT_REQUIRED"}`는 사람 필요성을 평가했으며 필요하지 않다고 확인한 상태로, 필드 누락 또는 `UNKNOWN`과 다르다. `KNOWN`의 인식되지 않은 basis도 스키마 형태는 보존하되 Engine에서 의미상 무효로 판정한다. `human_return_responsibility`는 승인·위험 통제·영향 범위 통제·직접 관측·학습·직접 엔지니어링 결과와 `ACK_ONLY`·`RAW_OUTPUT_ONLY`를 구분하고, 설명과 근거 참조를 함께 가진다. `human_facing_semantics`에는 구조화된 신뢰 reference와 선택적인 `supplemental_note`만 허용한다. action·target·capability·surface·verification·사람 반환 책임 binding이나 Profile interface 해석이 실패하면 차단한다. `NO_SUITABLE_AUTHORIZED_AI_SURFACE`에는 확인된 영향 부분 재평가가 추가로 필요하다. 행위별 대상은 승인 경계의 대상과 정확히 대조한다. 동일 행위 종류를 여러 번 사용하려면 서로 다른 ID를 사용한다. 미등록 종류는 `REQUIRED_CAPABILITY_UNKNOWN`이다.

프로필 요청은 정확한 ID·버전으로 지정한다. 다른 버전이 제공되면 `PROFILE_VERSION_UNAVAILABLE`이며 암묵적으로 최신 버전으로 교체하지 않는다. 정본 충돌 상태는 `CLEAR / CONFLICT / UNKNOWN`으로 구분하며, 충돌 또는 미확정은 `CANONICAL_CONFLICT`로 반환한다.

## 프로필과 실행 계획

제품명은 프로필의 표시 이름에만 존재한다. Engine의 역량 모델에는 ChatGPT·Codex 제품명을 고정하지 않는다.

| 행위 종류 | 필요 역량 | 기본 실행 환경 |
| --- | --- | --- |
| `reason_context` | `context_reasoning` | ChatGPT 일반 Chat |
| `inspect_repository` | `repository_inspection` | ChatGPT Work mode |
| `edit_document` | `document_edit` | ChatGPT Work mode |
| `mutate_repository` | `repository_mutation` | Codex CLI |
| `git_branch` | `git_operation` | Codex CLI |
| `run_command`, `run_tests` | `command_execution` | Codex CLI |
| `observe_runtime` | `runtime_observation` | Human IDE / Terminal |
| `mutate_runtime` | `runtime_mutation` | Human IDE / Terminal |

프로필은 Local Trial에 제공된 개념적 환경 매핑과 가용성 선언이다. `actions[].human_handoff`는 action 종류별 Human Goal·관측·판단·기대 해석의 신뢰 가능한 설명을 제공한다. `operational_interfaces`는 named interface의 표시 이름, 호환 Human surface와 적용 capability를 선언한다. 제품명은 Framework 코드 allowlist가 아니라 버전이 지정된 프로젝트 Profile 데이터로 관리한다. 실제 제품 접근·계정 권한·접속 상태를 탐지한 결과는 아니며, 호출자는 현재 환경의 가용성을 확인하고 변경한 프로필은 새 버전으로 관리해야 한다. 모델·추론 추천은 이 시험 프로필에서 `Surface-managed / N/A`로 두며 특정 모델 선택 알고리즘은 포함하지 않는다.

환경은 행위에 필요한 **모든** 역량과 effect, 요청에서 선택한 AI/HUMAN 책임 및 `KNOWN true` 가용성을 충족해야 후보가 된다. 프로필 action의 `actor`는 기본 책임이며, 정당한 사람 직접 수행을 선택할 때는 동일한 역량·effect 계약을 유지한 채 `actor=HUMAN`으로 재배정할 수 있다. `required_capabilities ⊆ surface.capabilities`와 `required_effects ⊆ surface.supported_effects`는 독립적으로 검사한다. 둘 다 위반하면 두 진단을 보존한다. 권한이 `AUTHORIZED`라도 `SURFACE_EFFECT_MISMATCH`를 면제하지 않는다. 실효 effect는 프로필의 행위별 최소 effect와 요청의 명시적 effect를 합친 값이다. 요청이 최소 effect를 지우거나 추가 변경 effect의 권한 검사를 우회할 수 없다. 후보 중 명시적 선택이 있으면 이를 검증한다. 없으면 프로필의 `preferred_surfaces` 순서를 동률 해소 기준으로 사용한다. 선호 후보가 없을 때 유일한 적합 후보만 선택하며 여러 후보가 남으면 `AMBIGUOUS_SURFACE_SELECTION`이다. 필요한 역량을 갖추지 못한 환경으로의 하향 대체는 없다.

계획은 요청의 행위 순서를 보존한다. v0의 각 실행 구간(Route Leg)은 행위 하나를 배정하며 `leg_id=leg-<action id>`를 사용한다. 각 구간에 `actor`, `session_role`, `execution_surface`, 원본 행위 전체를 담은 `assigned_actions`, `required_capabilities`, `effect_conformance`, `authority_status`, `model_recommendation`, `reasoning_recommendation`을 보존한다. `effect_conformance`의 `PASS`는 effect 적합성만 의미하며 실행 권한은 `authority_status`로 별도 확인한다. 이전의 `action_id`, `kind`, `surface_id`, `surface_label`, `capabilities`, `effects`는 조회용 투영으로 유지하고 내부 적합성 검사에서 상세 계약과 대조한다. 선택 환경이 하나면 `SINGLE`, 둘 이상이면 `COMPOSITE`이며, 미완성 계획은 `UNSELECTED`다. 복합 계획은 AI와 사람의 실행 책임을 각각 보존한다. 작업 의존성 스케줄링, 병렬 실행과 자동 인계는 하지 않는다.

## 권한과 실행 경계

권한 입력은 `AUTHORIZED / DENIED / UNKNOWN / NOT_REQUIRED`다. 가용성·선택·추천과 별개의 축이다.

`authority_assessment.input_status`는 요청자의 선언을 보존하고 `status`는 승인 참조와 실행 경계를 적용한 평가다. 예를 들어 선언이 `AUTHORIZED`라도 허용 effect를 벗어나면 평가 결과는 `DENIED`다.

- `AUTHORIZED`에는 확인된 승인 참조가 필요하다. Engine은 참조의 존재와 구조를 확인하며 외부 승인 기록의 진위나 승인자 권한을 조회하지 않는다.
- `DENIED`는 `AUTHORITY_DENIED`, `UNKNOWN`은 `AUTHORITY_UNKNOWN`이다.
- `NOT_REQUIRED`는 프로필에서 승인을 요구하지 않는 `READ_ONLY` 행위에만 허용한다.
- 파일·저장소 변경, 명령 실행, 런타임 관측·변경과 외부 부작용은 이 v0에서 명시적 권한을 요구한다. 프로필 데이터로 이를 면제할 수 없다.
- `approved_execution_boundary`는 정확히 같은 대상 문자열, 허용 action ID 및 허용 effect를 지정한다. 승인 경계의 대상·action ID·effect 부족은 각각 `BOUNDARY_TARGET_INSUFFICIENT`, `BOUNDARY_ACTION_INSUFFICIENT`, `BOUNDARY_EFFECT_INSUFFICIENT`이며 `HUMAN_GATE`로 반환한다. 명시적 권한 거부의 `AUTHORITY_DENIED → HUMAN_RESOLUTION`과 구분한다. 경로 포함 관계, glob 또는 저장소 권한 상속을 추론하지 않는다.
- `prohibited_actions`는 action ID, 등록 행위 종류 또는 effect와 정확히 대조한다. 일치하면 `PROHIBITED_ACTION`이다. 자연어 금지 조건의 의미 분석은 하지 않는다.

의사결정 책임자와 검증 책임자는 요청에서 보존하고, 실행 책임은 각 계획 단계의 AI/HUMAN 및 환경으로 배분한다. `continuation_authority`는 후속 실행의 상태다. `DENIED`·`NOT_REQUIRED`는 현재 요청 밖의 후속 실행을 허용하지 않는 상태로 보존한다. `UNKNOWN`은 인계 권한을 확정할 수 없으므로 `UNRESOLVED`다. 사람의 최종 책임을 AI에 이전하는 자동 승인 기능은 없다.

## PCBW-R07 사람 위임 집행

프로필 action의 `deterministic`은 사람 위임 경계를 평가하는 입력이다. 사람이 선택된 경우 Engine은 요청된 역량·effect를 만족하는 `KNOWN true` AI 환경과 확정된 권한을 독립적으로 대조한다. 현재 표면의 역량 부족을 사람이 입력한 주장으로 신뢰하지 않고 전체 프로젝트 프로필에서 적합한 AI 환경을 계산한다.

| 조건 | 판정 |
| --- | --- |
| 사람 실행 + `human_necessity_basis` 누락 또는 `UNKNOWN`, 다른 구조에서 부재를 확정할 수 없음 | `UNRESOLVED / HUMAN_NECESSITY_BASIS_MISSING` |
| 결정론적 사람 실행 + `human_necessity_basis=NOT_REQUIRED` + 적합하고 권한 있는 AI 환경 존재 | `FAIL / INVALID_HUMAN_DELEGATION` |
| 결정론적 사람 실행 + 인식되지 않은 basis 또는 basis와 불일치하는 반환 책임 + 적합하고 권한 있는 AI 환경 존재 | `FAIL / INVALID_HUMAN_DELEGATION` |
| 결정론적 사람 실행 + `ACK_ONLY` 또는 `RAW_OUTPUT_ONLY` + 적합하고 권한 있는 AI 환경 존재 | `FAIL / INVALID_HUMAN_DELEGATION` |
| `NO_SUITABLE_AUTHORIZED_AI_SURFACE` + 재평가 미확인 | `UNRESOLVED / TARGETED_RE_EVALUATION_NOT_ESTABLISHED` |
| 결정론적 사람 실행 + `NO_SUITABLE_AUTHORIZED_AI_SURFACE` + 적합하고 권한 있는 AI 환경 존재 | `FAIL / INVALID_HUMAN_DELEGATION` |
| 비결정론적 사람 실행 + `NO_SUITABLE_AUTHORIZED_AI_SURFACE` + 적합하고 권한 있는 AI 환경 존재 | `FAIL / NO_SUITABLE_AI_SURFACE_CONTRADICTION` |
| 사람 실행 + 사람 대상 운영 의미 미확정 | `FAIL / HUMAN_FACING_SEMANTICS_INSUFFICIENT` |
| 승인된 다른 사람 필요성 근거 + 완전한 운영 의미 | 기존 역량·effect·권한·경계 검증을 계속 수행하고 모두 충족하면 `PASS` |

사람 대상 운영 의미에는 Human Goal, Human Necessity Basis, 주 운영 인터페이스·도구, 관측 대상, 사람의 판단 사항, 사람 반환 책임, 기대 해석과 적용 가능한 CLI 대체 절차가 포함된다. 필수 설명은 Profile action의 `human_handoff`와 실제 target·capability·verification context에서 결정론적으로 생성한다. 다만 Profile의 일반적인 `decision` 문장만으로 `Human Decision Required`를 성립시키지 않는다. `decision_criterion_reference=ACTION_HUMAN_RETURN_RESPONSIBILITY`가 실제 action의 구조화된 반환 책임에 결합되어야 한다. `ACK_ONLY`와 `RAW_OUTPUT_ONLY`는 `Human Decision Required={"state":"NOT_REQUIRED"}`로 투영되어 승인·판단·직접 관측 책임처럼 보이지 않는다. 요청이 제공할 수 있는 `supplemental_note`는 별도 표시만 하며 필수 의미를 만들거나 덮어쓰지 않는다. Interface는 실제 선택 surface를 참조하는 `SELECTED_EXECUTION_SURFACE` 또는 Profile registry를 참조하는 `PROFILE_OPERATIONAL_INTERFACE`만 허용한다. 요청은 interface 표시 이름을 선언할 수 없다. CLI fallback도 같은 reference로 해석하거나 `NOT_REQUIRED`로 명시한다.

Engine은 action ID, target state, capability 집합, 선택 surface, action 검증 요구를 실제 요청·Profile 계산 결과와 대조한다. named interface reference는 선택 Profile에 존재하고 실제 Human surface 및 전체 action capability와 호환되어야 한다. Profile의 Human handoff 설명은 불투명한 ID만으로 구성되지 않도록 최소 구조를 검증한다. 따라서 `banana`, 새로운 동의어 또는 요청 내부의 중복 self-declaration은 신뢰를 만들 수 없다. 자연어의 진실성이나 외부 제품 존재 여부는 판단하지 않는다.

Human Route Leg가 있으면 Renderer는 검증된 Profile과 Route Leg로 `Human Execution Responsibility`를 다시 해석한다. Human Goal에는 trusted action 설명과 실제 target, 관측에는 trusted 설명·target·capability·verification requirement, 판단과 기대 해석에는 Profile handoff 설명을 투영한다. Interface와 fallback 표시 이름도 Profile 또는 선택 surface에서 해석한다. 독립 Directive Validator가 같은 신뢰 문맥에서 예상 책임을 재구성하므로, 결과와 지시문이 같은 임의 문자열을 담았다는 사실만으로 적합해지지 않는다. Engine의 `FAIL`·`UNRESOLVED`, Renderer 검증 실패와 독립 Validator의 `FAIL`은 모두 방출되지 않는다.

## 결과 재검증과 의미 지문

의미 지문(Semantic Fingerprint)은 ID·지문 필드 자체를 제외한 전체 결과를 키 정렬·고정 구분자의 UTF-8 JSON으로 직렬화해 SHA-256으로 계산한다. 결과에는 원본 요청과 프로필 스냅샷도 포함한다. 목표·행위·대상·환경·역할·책임·권한·금지 행위·검증·반환 계약의 변경이 모두 지문에 반영된다. 배열 순서는 의미가 있는 것으로 보존한다.

지문은 전자서명이나 승인 증명이 아니다. Renderer는 결과를 다시 계산하고 전체 결과를 대조한 후 표현한다. 따라서 결과 일부를 바꾸고 지문만 다시 계산해도 `PASS`를 재사용할 수 없다. 원본 요청·프로필까지 함께 바뀐 경우를 확인하려면 호출자가 신뢰하는 현재 입력을 기준으로 아래 CLI를 사용한다.

첫 `route` 출력에서 `result` 객체를 `result.json`으로, `directive` 문자열을 `directive.md`로 분리해 저장한 경우:

```sh
python3 tools/collaboration-routing/src/cli.py validate-directive \
  --request current-request.json \
  --profile current-profile.json \
  --result result.json \
  --directive directive.md
```

현재 입력으로 다시 계산한 결과와 전달된 결과가 다르면 `MATERIAL_DIRECTIVE_DRIFT`다. 지시문은 라우팅 결과의 결정론적 렌더링과 대조한다. 헤더 변경은 추가로 `HEADER_BODY_MISMATCH`를 보고한다. 반환 지시문에 새 책임이나 허가를 덧붙일 수 없다.

표시상 변경은 CRLF/LF, 빈 줄, 줄 끝 공백만 허용한다. 본문 내부 공백, 제목, JSON 값, 필드 순서 등 그 밖의 편집은 보수적으로 재검증 대상으로 처리한다. 임의의 Markdown 동치성을 판정하지 않는다. PASS 지시문은 여섯 필드의 Routing Header 바로 뒤에 `# <Recommended Session / Work Title>`을 표시하고 이어서 `## Engineering Objective`를 배치한다. 제목도 의미 변경 검증 대상이며 개행과 Markdown 경계 문자를 이스케이프한다. 본문은 JSON 코드 블록으로 표현하며 입력 문자열의 개행·백틱·HTML 경계 문자를 이스케이프해 새 섹션 삽입을 방지한다.

## 스키마 검증과 실패 처리

번들 스키마는 JSON Schema 2020-12 문서다. 내장 검증기는 이 문서들이 사용하는 `type`, `properties`, `required`, `additionalProperties`, `items`, `minItems`, `uniqueItems`, `minLength`, `enum`, `oneOf`만 처리한다. 지원하지 않는 키워드를 추가하면 검증기 오류로 차단한다. 범용 JSON Schema 엔진을 구현하거나 외부 라이브러리를 도입하지 않았다. 문자열 공백만 있는 값도 유효한 필수 텍스트로 인정하지 않는다.

```sh
python3 tools/collaboration-routing/src/cli.py validate-schema \
  --kind project-routing-profile \
  --document tools/collaboration-routing/profiles/framework-lab.v0.4.0.json
```

`validate-schema`의 `PASS`는 `SCHEMA_ONLY`로 표시하며 실행 가능한 결과의 의미 검증을 뜻하지 않는다. 프로필의 경우 중복 식별자·참조·권한 면제도 함께 검사한다. 라우팅과 지시문의 의미 검증은 `route`와 `validate-directive`를 사용한다.

확인된 위반과 미확정 문제가 동시에 있으면 `FAIL`을 우선하고 두 진단을 보존한다. 잘못된 입력 구조는 `ROUTING_CONTRACT_CONTRADICTION`, 검증기 예외는 `VALIDATOR_ERROR`, 검증 시간 초과는 `VALIDATOR_TIMEOUT`이다. 어느 경우에도 실행 가능한 지시문을 반환하지 않는다.

시간 제한은 로컬 계산 단계 사이에서 확인하는 협력적 제한이다. 중단된 프로세스나 무한정 블로킹하는 외부 호출을 강제 종료하는 장치는 없다. CLI의 JSON 파일 읽기도 이 계산 제한 밖이다. v0에는 외부 호출이 없으며, 계산이 제한을 넘으면 최종 결과 반환 전에 차단한다. 향후 서비스 수준의 강제 실행 시간 제한이 필요하면 별도 통합 범위에서 검토한다.

## 검증 근거와 완료 경계

`python3 -m unittest discover -s tools/collaboration-routing/tests -v`로 전체 테스트를 실행한다. 회귀 A–H의 입력 변경과 기대 상태·코드는 [regressions.json](tests/fixtures/regressions.json)에 고정했다. H의 전체 입력은 [regression-h.request.json](tests/fixtures/regression-h.request.json)이다.

두 번째 Review 64의 해결 경로 보정 후 Python 3.8.2로 49개 테스트 메서드와 내부 하위 사례가 모두 통과했다. CLI 재실행 출력 일치, 세 스키마 검증, 필수 회귀 A–H 및 아래 정상·오류 사례를 포함한다.

| 검증 | 기대 결과 |
| --- | --- |
| A: 일반 Chat + 저장소 직접 조사 | `FAIL / SURFACE_CAPABILITY_MISMATCH` |
| B: Work mode + Git·명령·테스트 | `FAIL / HEADER_BODY_MISMATCH` 및 역량 불일치 |
| C: 조사 역량의 환경 사용 불가 | `UNRESOLVED`, 일반 Chat 대체 없음 |
| D: 올바른 환경 + 권한 UNKNOWN | `UNRESOLVED / AUTHORITY_UNKNOWN` |
| E: 올바른 환경 + 권한 DENIED | `FAIL / AUTHORITY_DENIED` |
| F: 검증기 예외·시간 초과 | `UNRESOLVED`, 지시문 없음 |
| G: 검증 이후 환경·책임 변경 | `FAIL / MATERIAL_DIRECTIVE_DRIFT` |
| H: context_reasoning + REPOSITORY_MUTATION + 일반 Chat + AUTHORIZED | `FAIL / SURFACE_EFFECT_MISMATCH`, 지시문 `null` |
| 정상 9개 행위, 사람 관측·변경 + AI 추론·조사 | `PASS`, 단일·복합 계획 |
| 동률·미확정·중복·경계 위반·금지 행위 | 해당 상태·코드 및 지시문 차단 |
| 지문 재계산을 동반한 결과 변조 | 재계산 결과 대조로 차단 |
| 같은 입력 재실행·표시상 공백 변경 | 결정론적 출력·제한된 표시 변경 허용 |
| 현재 원본 입력이 바뀐 뒤 기존 지시문 검증 | 이전 `PASS` 재사용 차단 |

검증은 로컬 계약 동작에 한정된다. 실제 ChatGPT·Codex·Human IDE 환경 실행이나 승인 시스템 연동을 검증한 것은 아니다. Profile 가용성과 승인 근거의 실제성은 호출자 책임으로 남는다.

Review 64 시점의 보정에서는 Framework Governance, PCBW, Project Instructions를 변경하지 않았다. Skill·hook·ChatGPT 통합, 서버·큐·스케줄러, 자동 운반·실행·승인·orchestration 및 Scope Promotion은 포함하지 않았다. 해당 보정 결과의 당시 반환 목적지는 `00B`였다.

## Review 64 적합성 보정

이번 보정은 사용자가 제공한 `63 — Conformance Correction`의 명시적 요구에 따라 수행했다. 기존 `HG-62-01` 범위 안이며 커밋·푸시는 하지 않는다. 아직 게시하지 않은 v0 계약을 보완한 것이므로 파일 이름과 버전 식별자는 유지했다. 이전 형식 요청은 추가 필수 필드를 채워 다시 검증해야 하며 묵시적 기본값으로 변환하지 않는다.

| 보정 항목 | 구현 및 검증 근거 |
| --- | --- |
| Finding 1 — 환경 effect 적합성 | Surface `supported_effects`를 스키마와 프로필에 추가했다. 후보 계산과 내부 PASS 검사에서 역량·effect 포함 관계를 각각 검사한다. H와 Work Git·명령·테스트의 effect 단독 불일치를 검증했다. |
| Finding 2 — 완전한 행위 계약 | 대상·effect·출처·사람 직접 수행·검증 요구·구간 역할을 필수 상태 필드로 보존한다. 승인 참조는 기존 authority 규칙을 유지한다. 결과와 지시문의 원본 행위 보존, 미확정 입력 차단, 대상 경계 검사를 검증했다. |
| Finding 3 — 실행 구간 계약 | 구간 ID·역할·환경·배정 행위·역량·effect 평가·권한·모델·추론 추천을 보존한다. 동일 환경의 여러 행위와 Human+AI 복합 구간을 각각 검증했다. |
| Finding 4 — 원인별 해결 경로 | 아래 여섯 해결 유형을 원인 코드에 대응한다. 정상 요청의 해결 목록은 비어 있으며 위반·미확정·오류 요청은 실제 원인에 따라 분기한다. |
| Finding 5 — 지시문 제목 | Routing Header 직후 명시적 H1 제목을 렌더링한다. 순서·제목 변경 차단·제목을 통한 섹션 삽입 방지를 검증했다. |

`resolution_action[]`은 `kind`, `causes[]`, `instruction`을 가진 구조화된 안내다. 자동 실행이나 자동 승인을 뜻하지 않는다. 여러 원인이 있으면 해당 해결 경로를 함께 보존한다.

| 해결 유형 | 대표 원인 | 책임과 다음 동작 |
| --- | --- | --- |
| `INPUT_COMPLETION` | 필수 입력·역량 종류 미확정, 구조적 계약 모순 | 입력을 보완·수정한 뒤 재검증 |
| `TARGETED_RE_EVALUATION` | `INVALID_HUMAN_DELEGATION` | 반환된 적합 AI 후보로 PCBW-R06 영향 부분 재평가. 거부한 사람 지시문을 자동 재작성·방출하지 않음 |
| `ENVIRONMENT_RESOLUTION` | 프로필 버전·환경 미가용, 역량·effect 불일치 | 요구 수준을 낮추지 않고 적합한 환경을 확인한 뒤 재검증 |
| `HUMAN_RESOLUTION` | 정본 충돌, 동률 선택, 권한 미확정·거부, 금지 행위, 책임 불일치 | 책임 있는 사람에게 판단을 반환. 새로운 승인이 필요하다고 자동 단정하지 않음 |
| `HUMAN_GATE` | `AUTHORITY_REQUIRED` 또는 `BOUNDARY_TARGET_INSUFFICIENT`, `BOUNDARY_ACTION_INSUFFICIENT`, `BOUNDARY_EFFECT_INSUFFICIENT` | 대상·행위·effect를 포함하는 승인을 받거나 요청을 기존 승인 경계 안으로 축소한 뒤 재검증. 기존 금지·거부를 무효화하지 않음 |
| `REVALIDATE` | 지시문 의미 변경, 헤더·본문 불일치 | 이전 PASS를 폐기하고 계약 재검증 및 지시문 재생성 |
| `INTERNAL_RESOLUTION` | 검증기 오류·시간 초과 | 내부 오류를 해결한 뒤 재검증 |

Regression H의 입력은 `kind=reason_context`, 선언 effect `REPOSITORY_MUTATION`, 선택 환경 `general-chat`, 권한 `AUTHORIZED`, 가상 승인 참조 `fixture-H-authorized`다. 프로필이 제공하는 역량은 `context_reasoning`, 일반 Chat의 지원 effect는 `READ_ONLY`다. 실제 결과는 `FAIL`, `SURFACE_EFFECT_MISMATCH` 및 `HEADER_BODY_MISMATCH`, CLI 종료 코드 `1`, `directive=null`이다. 역량 불일치나 권한 거부에 의존하지 않고 effect 검사로 차단했다. 실효 effect에는 행위 최소값 `READ_ONLY`도 보존된다.

## 두 번째 Review 64: 승인 경계 부족의 해결 경로

기존 구현은 명시적 권한 거부와 승인 경계 부족에 모두 `AUTHORITY_DENIED`를 사용했다. 이 때문에 유효한 승인 참조가 있어도 요청한 effect가 승인 범위 밖이면 `HUMAN_RESOLUTION`으로 반환했다. 보정은 이 원인 분류와 해결 경로에 한정한다. 환경 적합성, 행위·실행 구간 계약, 제목 Renderer 및 Regression H의 의미는 변경하지 않는다.

| 원인 | 진단 코드 | 해결 경로 |
| --- | --- | --- |
| 명시적 `authority=DENIED`, 승인 경계는 충분 | `AUTHORITY_DENIED` | `HUMAN_RESOLUTION` |
| 요청 전체 또는 행위별 대상이 승인 대상 밖 | `BOUNDARY_TARGET_INSUFFICIENT` | `HUMAN_GATE` |
| 요청 action ID가 허용 목록 밖 | `BOUNDARY_ACTION_INSUFFICIENT` | `HUMAN_GATE` |
| 행위의 실효 effect가 허용 목록 밖 | `BOUNDARY_EFFECT_INSUFFICIENT` | `HUMAN_GATE` |

현재 경계 계약의 행위 차원은 `allowed_action_ids`로 판정한다. 별도 operation 허용 목록이나 경로 포함 관계를 새로 도입하지 않는다. 명시적 거부와 여러 경계 부족이 동시에 있으면 각 진단과 해결 경로를 함께 보존하며, 경계 확대 승인이 명시적 거부를 자동 해제한다고 해석하지 않는다. 권한 평가의 `status=DENIED`는 현재 실행을 허용할 수 없다는 결과이고, 원래 선언은 `input_status`, 실패 원인은 차원별 진단 코드로 식별한다.

[Regression I 입력](tests/fixtures/regression-i.request.json)은 `run_command`, `COMMAND_EXECUTION`, `AUTHORIZED`, 확인된 가상 승인 참조, 명시적으로 선택한 Codex 환경과 승인 effect `READ_ONLY`를 사용한다. 실제 결과는 `FAIL / BOUNDARY_EFFECT_INSUFFICIENT`, 해결 유형은 `HUMAN_GATE` 하나, 지시문은 `null`, CLI 종료 코드는 `1`이다. 다른 실패 코드와 미확정 문제가 없으며 환경의 effect 적합성은 `PASS`이므로 승인 경계 부족만으로 실패함을 확인했다.

대조 사례는 같은 명령 행위에 충분한 승인 경계를 두고 권한만 `DENIED`로 지정한다. 실제 결과는 `FAIL / AUTHORITY_DENIED`, 해결 유형은 `HUMAN_RESOLUTION` 하나, 지시문은 `null`이다. 추가로 대상·action ID 경계 부족 및 여러 원인이 동시에 발생하는 사례를 검증했다. 전체 49개 테스트에는 기존 A–H, 정상 단일·복합 경로, 지시문 차단, 지문·재검증 및 결정론적 CLI 검증이 포함된다.

이 보정은 커밋·푸시하지 않는다. `00B`의 수락 후 `64 — AI-Native Collaboration Routing Engine v0 Implementation Review`에서 독립 재검토하며, `PASS / READY FOR COMMIT` 전에는 커밋·푸시하지 않는다.

## Design 67: PCBW-R07 정본화 및 결정론적 방출 집행

`HG-67-01 = PASS`에 따라 PCBW-R07을 Effective PCBW Definition에 추가하고 기존 Engine의 action 판정 경계에 연결했다. 최초 구현 리비전의 계약 버전은 Routing Schema `1.1`, Engine·Integration `0.2.0`, Framework Lab 프로필 `0.2.0`이었다. 프로필 의미를 같은 ID/version에 덮어쓰지 않도록 `framework-lab.v0.1.0.json`을 `framework-lab.v0.2.0.json`으로 승격했다.

프로필 action의 `actor`는 기본 책임이고 요청의 `actor`는 선택된 실행 책임이다. 책임 재배정은 action의 역량·effect·권한·실행 경계를 약화하지 않는다. Human IDE / Terminal에는 사람의 정당한 명령 실행을 표현할 수 있도록 `command_execution`과 `COMMAND_EXECUTION`을 추가했지만, 결정론적 명령을 사람에게 배정할 때는 사람 필요성 근거와 운영 의미를 별도로 검증한다. 적합하고 권한 있는 Codex가 존재하는데 `NO_SUITABLE_AUTHORIZED_AI_SURFACE`를 주장하면 `INVALID_HUMAN_DELEGATION`으로 실패한다.

전체 71개 테스트 메서드와 내부 하위 사례가 통과했다. 신규 회귀는 결정론적 사전 점검·반복 폴링·정합성 확인·경계가 정해진 술어 기반 상태 전이·현재 Chat의 shell 부재를 사람 명령 전달로 바꾸는 false-PASS, 여섯 사람 필요성 근거의 유효 경로, basis 누락, 영향 부분 재평가 미확인, 사람 대상 운영 의미 누락·변조 및 `FAIL`·`UNRESOLVED` 방출 차단을 포함한다. 기존 Regression A–I와 정상 단일·복합 PCBW-R01~R06 경로도 함께 통과했다.

Framework Governance와 Failure Reproduction Workflow·Conformance·Reproduction Record Template은 변경하지 않았다. 자동 orchestration, 실행 어댑터와 범용 세션 번호 규칙을 추가하지 않았다.

## Review 69 교정: 사람 대상 의미 충분성

독립 검토에서 `FS-07 / C0 / Gate PASS / C1 / PASS`처럼 필수 필드가 비어 있지 않다는 이유만으로 Engine과 지시문 방출이 `PASS`하는 결함이 확인됐다. 이때 적용한 버전은 Routing Schema `1.1`, Engine·Integration `0.2.1`, Framework Lab 프로필 `0.2.0`이다. 요청 스키마는 필수 구조와 공백 값을 차단하고, `semantic_sufficiency.py`의 순수 결정론적 판정은 구조적으로 유효한 값의 최소 운영 의미를 Engine·내부 적합성 검사·독립 Directive Validator에 공통 적용한다. Renderer는 의미를 보완하거나 설명을 발명하지 않으며, 검증되지 않은 `PASS` 결과를 독립 호출해도 지시문을 만들지 않는다.

프로필의 실제 action 모델에서 사전 점검은 `run_tests`, 반복 상태 확인·정합성 확인·술어 기반 전이·명령 실행은 `run_command`로 표현된다. 인위적인 action 종류를 추가하지 않고 `objective`, `session_role`, `verification_requirement`, `source_references`로 각 실행 의미를 구분해 회귀를 검증한다. 전체 79개 테스트 메서드는 식별자·상태·플레이스홀더·부분 의미의 차단, 위조된 `PASS`의 내부/Renderer/독립 검증 차단, 통합 비방출, 간결한 실제 인터페이스와 정당한 Human Direct Engineering의 정상 방출을 포함한다. 이 교정은 정본 PCBW-R07의 의미를 변경하지 않는다.

## 조합형 제어·메타 토큰 우회 교정

`0.2.1`에서 `FS-07 check state`, `Gate PASS now result`, `PASS value state`처럼 내부 식별자와 일반 메타 어휘를 조합하면 기존 토큰 수·길이 문턱을 넘을 수 있었다. `0.2.2`는 구분자와 대소문자를 정규화하고 식별자 조각, 숫자, 상태·제어, 플레이스홀더, 일반 메타·행위 어휘를 명시적으로 분류한다. 설명 필드는 이들을 제외하고 운영 주체·객체 후보가 남아야 하며, 인터페이스 필드는 동일한 제외 규칙을 사용하되 하나의 실제 이름을 허용한다.

전체 87개 테스트 메서드는 helper 분류, 전체 조합형 fixture, 구분자 변형, Engine, 위조된 `PASS`의 내부 적합성, Renderer, 독립 Directive Validator와 통합 비방출을 검증한다. `Grafana`, `Terminal`, `RedisInsight`, `MySQL Workbench`, `Kafka UI`와 한국어·영어 혼합 운영 설명은 계속 허용한다. 이는 범용 자연어 판정이 아니라 알려진 비운영 어휘를 제거하는 최소 계약이므로, 새로운 프로젝트 용어는 allowlist 등록 없이 객체 후보로 남는다. Routing Schema와 프로필 버전은 각각 `1.1`, `0.2.0`으로 유지했다.

## 구조화된 사람 대상 운영 의미 집행 교정

`0.2.2`까지의 어휘 제거 방식은 `FS-07 review report`처럼 blacklist에 없는 동의어로 충분성을 만들 수 있었다. `0.3.0`은 자유 텍스트를 PASS 근거에서 제거하고 기존 Routing Request·Profile의 구조를 참조하는 positive binding을 요구한다. Routing Request·Result Schema는 `1.2`로 변경했으며 Framework Lab Profile은 내용이 변하지 않아 profile version `0.2.0`, profile schema `1.1`을 유지한다.

`structured_operational_semantics`는 action ID, `ACTION_TARGET`, 선택 surface에 귀속된 Interface, profile capability 집합, `ACTION_VERIFICATION_REQUIREMENT`, `REQUEST_VERIFICATION_CONTRACT`와 CLI fallback 상태를 별도 책임으로 표현한다. Engine은 참조를 실제 문맥과 대조하고, 내부 적합성 검사와 독립 Directive Validator도 재계산된 결과와 렌더링된 binding을 검증한다. `1.1` Human request처럼 binding이 없는 이전 형식은 `1.2` 요청 스키마에서 거부되며 지시문을 방출하지 않는다.

전체 93개 테스트 메서드는 세 exploit 계열, 자유 텍스트 동의어 불변성, binding 누락·변조, fingerprint를 다시 계산한 위조 `PASS`, Renderer와 독립 Validator 차단을 검증한다. 한국어 prefix 기반 제거를 없애고 exact control vocabulary만 심층 방어에 사용하므로 `작업자`, `실행기`, `상태머신`, `관측기`는 valid binding이 있으면 허용된다. `Grafana`, `Terminal`, `RedisInsight`, `MySQL Workbench`, `Kafka UI`, `IntelliJ IDEA`, `psql`, `redis-cli`도 제품 allowlist 없이 구조화된 named Interface로 허용한다. 이 교정은 정본 PCBW-R07의 의미를 변경하지 않는다.

## 신뢰 가능한 구조화 Human handoff 교정

`0.3.0`은 action·target·capability reference를 검증했지만 요청이 `NAMED_OPERATIONAL_INTERFACE`의 ID와 표시 이름을 직접 선언할 수 있었다. 따라서 `banana`를 모든 설명과 interface에 반복한 self-declaration도 통과했다. `0.4.0`은 이 신뢰 원천을 제거한다. Routing Request·Result Schema는 `1.3`, Project Routing Profile Schema는 `1.2`, Framework Lab Profile은 `0.3.0`으로 승격했다.

필수 Human 설명은 `actions[].human_handoff`에서, named interface는 `operational_interfaces`에서 해석한다. Request는 `SELECTED_EXECUTION_SURFACE` 또는 `PROFILE_OPERATIONAL_INTERFACE`의 ID만 참조하며 display name을 선언하지 않는다. Profile interface는 실제 선택 Human surface와 전체 action capability에 모두 호환되어야 한다. CLI fallback도 동일한 신뢰 reference를 사용한다. 기존 여섯 설명 필드는 Request 1.3에서 제거했고 임의 문맥은 `supplemental_note`로만 보존한다. Renderer와 독립 Validator는 신뢰 문맥에서 동일한 사람 책임을 재구성한다.

이전 Schema 1.1과 취약한 1.2 Human request는 자동 변환하지 않고 입력 경계에서 비방출한다. 전체 98개 테스트 메서드는 세 기존 exploit, `banana`, fallback mismatch, interface 소유권·surface·capability, 잘못된 action·target·verification binding, 위조 PASS, 한국어 기술 명사와 선택 surface/GUI/CLI 정상 경로를 검증한다. 이 Profile registry는 Collaboration Routing Engine의 프로젝트 데이터이며 새 PCBW 정본 요소가 아니다.

## 68A 재현 및 69 교정: 알려진 사람 필요성 부재와 Project 방출 회귀

시작 리비전 `cf32486bba42eeaeae6165538405d8ffd67d83f4`의 Request 1.3·Profile 0.3.0으로 관측 지시문을 충실히 투영하면 `ARTIFACT_WRITE`를 지원하지 않는 Human surface까지 함께 평가된다. 실제 결과는 `FAIL`, failure code `HEADER_BODY_MISMATCH`·`SURFACE_EFFECT_MISMATCH`, unresolved issue `HUMAN_NECESSITY_BASIS_MISSING`·`NO_FEASIBLE_SURFACE_AVAILABLE`·`REQUIRED_CAPABILITY_UNAVAILABLE`, `directive=null`의 복합 결과다. 이전의 `UNRESOLVED / HUMAN_NECESSITY_BASIS_MISSING` 단독 설명은 `ARTIFACT_WRITE`를 제외해 사람 필요성 상태만 격리한 최소 모델이며, 충실한 관측 fixture baseline이 아니다. 재실행한 baseline projection은 `tests/fixtures/pcbw-r07-observed-baseline-projection.json`에 고정한다.

교정 후 Routing Request·Result Schema는 `1.5`, Engine·Integration은 `0.6.0`이다. `human_necessity_basis=NOT_REQUIRED`를 알려진 사람 필요성 부재로 해석하고, `human_return_responsibility`를 추가했다. 인식되지 않은 basis는 Schema가 원문을 보존한 상태에서 Engine이 의미상 검증한다. 결정론적 행위를 사람에게 배정했는데 적합하고 권한 있는 AI 환경이 존재하고 사람 필요성이 `NOT_REQUIRED`·인식 불가이거나 반환 책임과 구조적으로 불일치하면 `FAIL / INVALID_HUMAN_DELEGATION`이다. `ACK_ONLY`와 `RAW_OUTPUT_ONLY`도 이 조건에서 동일하게 실패한다. basis가 실제로 누락 또는 `UNKNOWN`이고 다른 구조가 부재를 확정하지 않을 때만 `UNRESOLVED / HUMAN_NECESSITY_BASIS_MISSING`을 유지한다.

상태 의미는 다음과 같이 분리한다.

| 사람 필요성 입력 | 의미 | 결정론적 Human 배정과 적합·권한 있는 AI 후보가 있을 때 |
| --- | --- | --- |
| 필드 누락 | 아직 판정하지 못함 | `UNRESOLVED / HUMAN_NECESSITY_BASIS_MISSING` |
| `UNKNOWN` | 판정 결과를 알 수 없음 | `UNRESOLVED / HUMAN_NECESSITY_BASIS_MISSING` |
| `NOT_REQUIRED` | 사람 필요성이 없음을 확인함 | `FAIL / INVALID_HUMAN_DELEGATION` |
| 유효한 Human necessity | 반환 책임·운영 의미와 구조적으로 결합된 사람 고유 책임 | 나머지 권한·환경 계약이 유효하면 `PASS` 가능 |

`return_contract`는 더 이상 목적지 문장만 받지 않는다. 행위별 구조화 반환 종류를 `human_action_returns[]`로 선언하고 action의 반환 책임과 교차 검증한다. `HUMAN_EXECUTION_SIMPLER_OR_SAFER`라는 basis만으로는 충분하지 않으며, `DIRECT_ENGINEERING_RESULT`와 행위·대상·검증·운영 인터페이스에 결합된 실제 Human 책임이 있어야 한다. 준비된 명령·스크립트 실행 뒤 ACK, 원시 stdout, PASS/FAIL 출력 또는 Evidence 경로만 반환하는 경우는 사람의 결정 책임을 성립시키지 않는다.

`INVALID_HUMAN_DELEGATION`은 `TARGETED_RE_EVALUATION` 해결 유형으로 PCBW-R06에 연결된다. Routing Result의 `targeted_re_evaluation[]`은 영향을 받은 action, 원인, 거부된 Human surface와 적합한 AI 후보의 surface ID·표시 이름·역량·effect·권한 상태·모델·추론 추천을 반환한다. 후보에는 `selection_status=REEVALUATION_CANDIDATE`를 명시한다. 이는 선택이나 새 권한 부여가 아니다. Engine과 Integration은 후보를 새 선택으로 자동 적용하거나 사람 지시문을 고쳐 쓰지 않는다. 관측 fixture의 결과는 `Codex CLI` 후보, `directive=null`, `emission_outcome=BLOCKED`다.

회귀 fixture는 관측된 Bash 실행·hash 검증·정적 사전 점검·Docker inspect/logs/stats·Evidence 및 안정성 계획 파일 작성·완료 ACK 반환 책임을 한 action 계약으로 보존한다. 범용 회귀는 결정론적 사전 점검, Evidence 수집, 제한된 폴링, 준비된 스크립트와 완료 ACK, database·Kubernetes·test·log 수집을 포함한다. 대조 회귀는 유효한 사람 승인, 영향 범위 통제(Blast-radius Control), 사람 학습·직접 관측 목적, 적합한 AI 환경 부재와 기존 Human Direct Engineering을 보존한다.

통합 Adapter는 Engine의 `PASS` 결과도 원본 Request·Profile에서 독립 재계산하며, 독립 Directive Validator의 `PASS`가 Routing Result ID·의미 지문·지시문 지문에 결합되었을 때만 방출한다. 자유형 Project 지시문, 위조 Routing Result 또는 결과에 결합되지 않은 Validator `PASS`는 모두 `directive=null`, `emission_outcome=BLOCKED`다.

Project Routing Profile Schema `1.2`와 Framework Lab Profile `0.3.0`은 변경하지 않았다. 이번 교정은 action 요청·결과와 방출 관문의 의미를 명확히 하며 Profile의 action·surface·interface·가용성 선언을 바꾸지 않기 때문이다. PCBW-R07 정본 의미를 변경하거나 PCBW-R08을 만들지 않았다.

이 통합은 계속 운영자 매개 로컬 시험(Operator-mediated Local Trial)이다. 저장소 밖의 실제 ChatGPT Project 재사용 지시문 생성 경로가 이 Adapter를 반드시 호출하도록 만드는 플랫폼 설정 또는 ChatGPT-native interceptor는 이 저장소에 없다. 따라서 테스트 통과는 라이브 Project 집행을 증명하지 않는다. 라이브 강제 적용에는 Project Control Plane의 지시문 생성·방출 직전 지점에 Routing Request 구성, 이 Adapter 호출, `EMITTED` 외 결과의 방출 금지를 배포할 플랫폼 소유 권한이 필요하다.

저장소가 지원하는 가장 강한 Project 수준 계약은 `project-integration/framework-lab.reusable-directive-emission.v0.1.0.json`이다. 이 아티팩트는 모든 재사용 Routing/Handoff 지시문을 방출하기 전에 Required Action·Capability·Human Necessity를 평가하고, 결정론적 Human command relay를 거부하며, PCBW-R06 영향 부분 재평가 후 Routing Result와 Directive Validation이 모두 `PASS`일 때만 방출하도록 요구한다. `Human IDE / Terminal`을 missing-capability 기본 fallback으로 사용하는 것도 금지한다. 아티팩트 상태는 `CANDIDATE_FOR_EXTERNAL_PROJECT_SYNCHRONIZATION`이며 저장소 테스트는 내용과 로컬 Integration 동작의 일치만 검증한다. 실제 ChatGPT Project Instructions 반영과 그 독립 확인은 플랫폼/Project 설정 소유자가 수행해야 하므로 **EXTERNAL PROJECT SYNCHRONIZATION REQUIRED**다.

## 68C 교정: 통합 입력 결합과 신뢰 Human 책임

`0.6.0` Integration은 반환된 Routing Result 자체를 재검증했지만, 그 Result가 현재 `integrate(request, profile)` 호출에 전달된 입력에서 생성되었는지는 대조하지 않았다. 따라서 다른 유효 Request에서 생성된 self-validating `PASS` Result를 주입하면 현재 호출의 Renderer까지 진행해 지시문을 방출할 수 있었다. `0.7.0`은 Renderer 호출 전에 `result.source_request == request_snapshot`과 `result.source_profile == profile_snapshot`을 모두 확인한다. 하나라도 다르면 `INTEGRATION_BLOCKED / ROUTING_RESULT_INPUT_MISMATCH`, `directive=null`, `emission_outcome=BLOCKED`다.

Request가 `HUMAN_EXECUTION_SIMPLER_OR_SAFER`, `DIRECT_ENGINEERING_RESULT`와 임의 설명·source reference를 함께 선언하는 것만으로는 사람 필요성과 책임을 증명하지 못한다. Framework Lab Profile `0.4.0`은 `trusted_human_responsibilities[]`에서 basis, 반환 책임 종류, 적용 action kind와 Human role의 신뢰 가능한 조합을 소유한다. Engine은 Request의 `human_return_responsibility.source_references[]`가 선택된 Profile의 정확한 source ID와 결합되는지 검사한다. Request 문장은 주장과 부가 맥락으로 보존되지만 자신의 PASS 근거가 될 수 없다. 유효한 Human 승인, 위험·영향 범위 통제, 학습, 직접 관측, 실제 직접 엔지니어링과 재평가로 확인된 no-AI-surface 경로는 Profile source에 결합되어 계속 허용된다.

버전은 Routing Request Schema `1.5` 유지, Routing Result Schema `1.6`, Project Routing Profile Schema `1.3`, Framework Lab Profile `0.4.0`, Engine·Integration `0.7.0`이다. Profile의 `codex` surface label은 제품·저장소 식별자를 섞지 않은 `Codex CLI`로 정규화했다. 저장소 identity는 Request의 target과 branch/revision/environment 맥락에 남는다.

관측 fixture는 실제 파일 생성 책임을 반영해 action effect와 승인 경계에 `ARTIFACT_WRITE`를 추가했다. command-only R07 판정은 별도의 범용 fixture에서 계속 격리한다. 관측 fixture의 AI decision ownership과 ACK-only return contract를 유지한 채 basis·action 반환 종류·임의 source만 바꾸는 회귀와, top-level 반환 종류까지 같은 주장으로 바꾸는 회귀는 모두 `FAIL / INVALID_HUMAN_DELEGATION`이고 방출되지 않는다.

실제 ChatGPT Project 경계는 바뀌지 않았다. 공식 OpenAI 문서는 Project instructions가 Project의 chats에 적용되며 Codex CLI는 ChatGPT Projects view를 제공하지 않는다고 설명한다. 저장소에는 Project 응답을 자동 가로채는 플랫폼 interceptor가 없으므로, 로컬 Integration PASS는 실제 Project Instructions 동기화를 증명하지 않는다. `project-integration/framework-lab.reusable-directive-emission.v0.1.0.json`의 외부 동기화와 독립 확인이 계속 필요하다.

## 71 교정: action-instance Human 책임 소유권 결합

Profile `trusted_human_responsibilities[]`의 source ID는 허용된 basis·반환 종류·action kind·Human role의 카탈로그 항목일 뿐, 현재 action에 그 책임이 실제 배정됐다는 증거가 아니다. `0.7.0` 후보에서는 관측 command relay가 `framework-lab:direct-engineering` ID를 복사하고 basis와 반환 종류를 `HUMAN_EXECUTION_SIMPLER_OR_SAFER`·`DIRECT_ENGINEERING_RESULT`로 바꾸면, AI가 decision과 verification을 계속 소유해도 `PASS / EMITTED`가 되는 결함이 있었다.

Project Routing Profile Schema `1.4`는 각 신뢰 Human role에 `required_session_role`과 `required_request_owners[]`를 추가한다. 전자는 action instance의 session role을 Profile이 소유한 역할과 정확히 결합하고, 후자의 각 항목은 `responsibility.decision_owner` 또는 `responsibility.verification_owner`와 Profile이 소유한 정확한 책임자 identity를 결합한다. `DIRECT_ENGINEER`는 전용 session role과 두 책임자 모두를 요구하고, 승인·위험 통제·학습은 decision owner, 직접 관측은 verification owner를 요구한다. `EXECUTION_ONLY_WHEN_NO_AI_SURFACE`는 검증된 AI surface 부재 자체가 실행 책임 근거이므로 별도 decision/verification owner를 요구하지 않는다.

Engine은 action ID·kind·actor·선택 Human surface·basis·반환 종류·session role·target·effect·verification·action 반환 계약의 기존 교차 검증에 이 Profile 소유 owner binding을 추가한다. 따라서 관측 fixture가 AI decision/verification ownership과 command-relay topology를 유지한 채 정확한 `framework-lab:direct-engineering` ID를 복사해도 `FAIL / INVALID_HUMAN_DELEGATION`이다. 이 판정에는 자유 텍스트 keyword나 `done`·`완료` 같은 어휘를 사용하지 않는다.

현재 계약 버전은 Routing Request Schema `1.5`, Routing Result Schema `1.7`, Project Routing Profile Schema `1.4`, Framework Lab Profile 후보 `0.4.0`, Engine·Integration `0.8.0`이다. Profile `0.4.0`은 아직 커밋·게시된 기준선이 아닌 하나의 미커밋 후보이므로 같은 후보 파일 안에서 완성했다. PCBW-R07 정본 의미와 외부 Project synchronization 경계는 변경하지 않았다.
