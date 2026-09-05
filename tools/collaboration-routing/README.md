# Collaboration Routing Engine v0

Status: Project-level Local Trial Implementation

## 목적과 승인 경계

이 도구는 구조화된 필수 행위에서 필요한 역량과 실행 환경(Execution Surface)을 결정하고, 사람·AI 책임 및 실행 권한을 별도로 검증한다. 검증된 라우팅 결과(Routing Result)를 기계 소비용 계약으로 반환하며 `PASS`에서만 Markdown 지시문을 생성한다. 명령·Git 작업·런타임 조작을 실제 수행하지 않는다.

- 적용 프로젝트: `AI-Native Engineering Framework Lab`
- 승인 설계: `62 — AI-Native Collaboration Routing Engine v0 Design`
- 승인 근거: 사용자가 제공한 `63 Implementation Directive`의 `HG-62-01 — PASS` 및 후속 Resume의 `PASS / remains valid`
- 승인 범위: 프로젝트 수준의 로컬 시험 구현, 스키마·프로필·CLI·회귀 검증·최소 사용 문서
- 구현 브랜치: `feat/collaboration-routing-v0`
- 시작 리비전: `d934887ce0530ef0ad6b775b42092903fc022002`
- 반환 목적지: `00B — AI-Native Engineering Framework Control Plane`

적용 정본은 [AI Engineering Guidelines](../../governance/AI-ENGINEERING-GUIDELINES.md)와 [Project Collaboration Bootstrap Workflow](../../workflows/project-collaboration-bootstrap/PROJECT-COLLABORATION-BOOTSTRAP-WORKFLOW.md)다. 이 디렉터리의 코드·프로필·결과는 해당 문서를 대체하거나 Framework·Workflow 규칙을 변경하지 않는다. 한국어 문서는 [Technical Documentation Guidelines](../../governance/TECHNICAL-DOCUMENTATION-GUIDELINES.md)를 따른다.

## 실행 방법

Python 3.8 이상의 표준 라이브러리만 사용한다. 외부 패키지 설치와 서비스 연결이 없다. 아래 명령은 저장소 루트에서 실행한다.

```sh
python3 tools/collaboration-routing/src/cli.py route \
  --request tools/collaboration-routing/tests/fixtures/inspection.request.json \
  --profile tools/collaboration-routing/profiles/framework-lab.v0.1.0.json

python3 -m unittest discover -s tools/collaboration-routing/tests -v
```

CLI는 표준 출력에 JSON 객체 하나를 반환한다. 종료 코드는 `PASS=0`, `FAIL=1`, `UNRESOLVED=2`다. 잘못된 CLI 옵션은 argparse의 사용법 오류로 종료한다. 도구 자체는 출력 파일을 만들거나 원격 전송하지 않는다.

| 출력 필드 | 의미 |
| --- | --- |
| `routing_status` | 전체 검증 결과 |
| `failure_codes` | 확인된 계약 위반 |
| `unresolved_issues` | 확정할 수 없는 입력·가용성·권한·검증기 상태 |
| `resolution_action` | 입력 수정 또는 사람의 판단 후 재검증 안내 |
| `result` | 유효한 입력으로 구성한 구조화된 결과. 입력 형식 오류나 검증기 오류 시 `null` |
| `directive` | 검증된 `PASS` 지시문. 그 밖의 모든 경우 `null` |

`FAIL`·`UNRESOLVED`의 `result`에는 진단을 위한 실행 계획 후보가 남을 수 있다. 이 후보는 실행 가능한 지시문이 아니며 상태를 무시하고 소비해서는 안 된다.

예제는 **읽기 전용 요청 형식 예시**다. 대상 문자열·상태·검증 책임자·리비전을 실제 값으로 교체해야 한다. 테스트의 승인 참조는 가상 데이터이며 실제 실행 승인이 아니다.

## 구성과 책임 분리

```text
Structured Request → Schema Validation → Capability Resolution
 → Profile / Feasible Surface → Plan / Responsibility
 → Authority / Boundary → Internal Conformance → Status
 → PASS only → Renderer → Rendered Conformance
```

| 파일 | 책임 |
| --- | --- |
| `schemas/routing-request.schema.json` | 필수 행위와 명시적 입력 상태 |
| `schemas/project-routing-profile.schema.json` | 프로젝트의 행위·역량·환경 매핑 |
| `schemas/routing-result.schema.json` | 기계 소비용 결과 계약 |
| `profiles/framework-lab.v0.1.0.json` | Framework Lab의 버전 지정 매핑과 가용성 선언 |
| `src/schema_validation.py` | 번들 스키마에서 사용하는 JSON Schema 부분집합 검증 |
| `src/engine.py` | 라우팅, 책임 배분, 권한·경계 검증 및 내부 적합성 검사 |
| `src/directive.py` | 결정론적 표현과 지시문 적합성 검증 |
| `src/cli.py` | 로컬 입력 및 JSON 출력 |
| `tests/fixtures/` | 예제 요청과 고정 회귀 A–G |
| `tests/test_routing.py` | 정상·오류·변조·CLI 검증 |

요구사항 추출(Requirement Extraction)은 호출자의 책임이다. Engine은 자연어 목표나 본문에서 명령을 추출하지 않으며 `required_actions[]`만 행위 판정의 입력으로 사용한다. 목표·행위·대상 간 자연어 의미의 정확성은 요청 작성자와 검토자가 확인해야 한다.

`Routing Decision ≠ Authority`, `Routing Result ≠ Directive`, `Directive ≠ Execution`을 유지한다. 운반 어댑터(Execution Adapter)는 포함하지 않는다.

## 요청 계약과 명시적 상태

판정에 필요한 값은 다음 형태를 사용한다. `UNKNOWN`이나 `NOT_REQUIRED`에 `value`를 추가하면 스키마 위반이다. 누락·`null`·빈 문자열은 상태를 대신하지 않는다.

```json
{"state":"KNOWN","value":"confirmed value"}
{"state":"UNKNOWN"}
{"state":"NOT_REQUIRED"}
```

필수 맥락은 프로젝트, 제목, 목표, 세션 역할, 대상, 현재 상태·관문, 정본 참조, 실행 경계, 금지 행위 목록, 의사결정·검증 책임자, 검증 계약과 반환 계약이다. 이 필드의 `UNKNOWN`은 `UNRESOLVED`, `NOT_REQUIRED`는 계약 모순이다. 금지 행위가 없으면 `KNOWN`과 빈 배열로 명시한다.

중단 조건·근거 요구·브랜치/리비전/환경은 적용되지 않을 때 `NOT_REQUIRED`를 허용한다. 적용 여부를 아직 모르는 `UNKNOWN`은 보수적으로 `UNRESOLVED`다. `surface_selection=NOT_REQUIRED`는 명시적 선택 없이 프로필로 선택하라는 뜻이다. `KNOWN`이면 모든 action ID를 한 번씩 지정해야 한다.

각 필수 행위는 `id`, `kind`, `target`, `effects`, `source_references`, `actor`, `human_direct`, `session_role`, `verification_requirement`, `authority`, `approval_reference`를 가진다. 새 상태 필드도 `UNKNOWN`이면 미확정, `NOT_REQUIRED`이면 필수 계약 위반으로 처리한다. `human_direct`는 사람이 직접 수행하는지 명시하며 `actor`와 일치해야 한다. 행위별 대상은 승인 경계의 대상과 정확히 대조한다. 동일 행위 종류를 여러 번 사용하려면 서로 다른 ID를 사용한다. 행위 종류와 AI/HUMAN 책임은 프로필과 대조한다. 미등록 종류는 `REQUIRED_CAPABILITY_UNKNOWN`이다.

프로필 요청은 정확한 ID·버전으로 지정한다. 다른 버전이 제공되면 `PROFILE_VERSION_UNAVAILABLE`이며 암묵적으로 최신 버전으로 교체하지 않는다. 정본 충돌 상태는 `CLEAR / CONFLICT / UNKNOWN`으로 구분하며, 충돌 또는 미확정은 `CANONICAL_CONFLICT`로 반환한다.

## 프로필과 실행 계획

제품명은 프로필의 표시 이름에만 존재한다. Engine의 역량 모델에는 ChatGPT·Codex 제품명을 고정하지 않는다.

| 행위 종류 | 필요 역량 | 기본 실행 환경 |
| --- | --- | --- |
| `reason_context` | `context_reasoning` | ChatGPT 일반 Chat |
| `inspect_repository` | `repository_inspection` | ChatGPT Work mode |
| `edit_document` | `document_edit` | ChatGPT Work mode |
| `mutate_repository` | `repository_mutation` | Codex Project / Session |
| `git_branch` | `git_operation` | Codex Project / Session |
| `run_command`, `run_tests` | `command_execution` | Codex Project / Session |
| `observe_runtime` | `runtime_observation` | Human IDE / Terminal |
| `mutate_runtime` | `runtime_mutation` | Human IDE / Terminal |

프로필은 Local Trial에 제공된 개념적 환경 매핑과 가용성 선언이다. 실제 제품 접근·계정 권한·접속 상태를 탐지한 결과가 아니다. 호출자는 현재 환경의 가용성을 확인하고 변경한 프로필은 새 버전으로 관리해야 한다. 모델·추론 추천은 이 시험 프로필에서 `Surface-managed / N/A`로 두며 특정 모델 선택 알고리즘은 포함하지 않는다.

환경은 행위에 필요한 **모든** 역량과 effect, AI/HUMAN 책임 및 `KNOWN true` 가용성을 충족해야 후보가 된다. `required_capabilities ⊆ surface.capabilities`와 `required_effects ⊆ surface.supported_effects`는 독립적으로 검사한다. 둘 다 위반하면 두 진단을 보존한다. 권한이 `AUTHORIZED`라도 `SURFACE_EFFECT_MISMATCH`를 면제하지 않는다. 실효 effect는 프로필의 행위별 최소 effect와 요청의 명시적 effect를 합친 값이다. 요청이 최소 effect를 지우거나 추가 변경 effect의 권한 검사를 우회할 수 없다. 후보 중 명시적 선택이 있으면 이를 검증한다. 없으면 프로필의 `preferred_surfaces` 순서를 동률 해소 기준으로 사용한다. 선호 후보가 없을 때 유일한 적합 후보만 선택하며 여러 후보가 남으면 `AMBIGUOUS_SURFACE_SELECTION`이다. 필요한 역량을 갖추지 못한 환경으로의 하향 대체는 없다.

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
  --document tools/collaboration-routing/profiles/framework-lab.v0.1.0.json
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

Framework Governance, PCBW, Project Instructions는 변경하지 않는다. Skill·hook·ChatGPT 통합, 서버·큐·스케줄러, 자동 운반·실행·승인·orchestration 및 Scope Promotion은 포함하지 않는다. 이번 보정 결과는 `00B`로 반환하며 후속 통합 여부는 Control Plane에서 별도로 판단한다.

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
