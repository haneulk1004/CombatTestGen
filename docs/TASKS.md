## 1. 기획·설계 단계 Tasks

## [x] T-001 PRD 최종 정리 및 공유

- 내용: 기존에 작성한 PRD(제품 목적, 타겟, KPI, 기능 목록)을 문서화하고 버전 관리 시스템(Confluence, Notion 등)에 게시.
- 산출물: `CombatTestGen_PRD_v1.0`
- 선행 작업: 없음
- 기간: 0.5일
- 참조: PRD – 목적과 목표, 타겟 사용자, 기능 요구사항 섹션

## [x] T-002 TRD 최종 정리 및 공유

- 내용: TRD(아키텍처, 데이터 모델, API, 성능 요구사항)를 정리해 팀과 공유.
- 산출물: `CombatTestGen_TRD_v1.0`
- 선행 작업: T-001
- 기간: 0.5일
- 참조: TRD – 시스템 아키텍처, 기술 스택, 데이터 모델, 성능 요구사항

## [x] T-003 WBS/일정 수립

- 내용: 이 Tasks 문서를 바탕으로 WBS 작성, 스프린트(또는 주차)별 배치.
- 산출물: Gantt / Sprint Backlog
- 선행 작업: T-001, T-002
- 기간: 0.5일
- 참조: PRD – 구현 로드맵, TRD – 빌드 및 배포 스크립트 개요

---

## 2. 인프라·프로젝트 뼈대

## [x] T-010 Python 프로젝트 초기화

- 내용: `src/`, `tests/`, `requirements.txt`, 기본 패키지 구조 생성.
- 산출물: Git 리포지토리, 기본 폴더 구조
- 선행 작업: T-003
- 기간: 0.5일
- 참조: TRD – 기술 스택 상세(언어, 라이브러리)

## [x] T-011 의존성 설정 및 가상환경 구성

- 내용: Python 3.11 가상환경, Typer/Click, Jinja2, Pydantic, PyInstaller 등 설치.
- 산출물: `requirements.txt`, 설치 스크립트
- 선행 작업: T-010
- 기간: 0.5일
- 참조: TRD – 기술 스택 상세

---

## 3. 도메인 모델·검증 로직

## [x] T-020 CombatParams 데이터 모델 구현

- 내용: PRD의 전투 파라미터 요구사항에 맞춘 `CombatParams` Pydantic 모델 구현.
- 산출물: `src/domain/models.py`
- 선행 작업: T-010, T-011
- 기간: 1일
- 참조: TRD – 데이터 모델 (CombatParams), PRD – 기능 요구사항(입력 인터페이스)

## [x] T-021 입력 검증·에러 메시지 정의

- 내용: 데미지 범위, HP 범위, 시나리오 필수 여부 검증 및 사용자 친화적 에러 메시지 정의.
- 산출물: 검증 모듈, 에러 메시지 스펙
- 선행 작업: T-020
- 기간: 0.5일
- 참조: TRD – 에러 핸들링, PRD – 타겟 사용자(비개발자도 사용 가능)

---

## 4. 엣지 케이스 생성 엔진

## [x] T-030 시나리오 Enum 및 기본 시나리오 정의

- 내용: NORMAL, CRITICAL, DODGE, DEATH 등 Enum 및 기본 시나리오 세트 정의.
- 산출물: `Scenario` Enum
- 선행 작업: T-020
- 기간: 0.5일
- 참조: TRD – Scenario Enum, PRD – 전투 시나리오 예시(기본 공격, 사망, 치명타)

## [x] T-031 엣지 케이스 생성 알고리즘 구현

- 내용: 입력(데미지, HP)을 기반으로 NORMAL, Critical, ZeroDamage, Overkill, DeathFlow 등 자동 생성.
- 산출물: `EdgeCaseGenerator` 모듈
- 선행 작업: T-030
- 기간: 1일
- 참조: TRD – 엣지 케이스 생성기, PRD – 엣지 케이스 자동 생성 기능

## [x] T-032 엣지 케이스 단위 테스트 작성

- 내용: 다양한 입력 조합에 대한 예상 HP/상태 검증 테스트.
- 산출물: `tests/unit/test_edge_cases.py`
- 선행 작업: T-031
- 기간: 0.5일
- 참조: TRD – 테스트 전략(단위 테스트 90% 목표)

---

## 5. 템플릿 엔진·출력 포맷

## [x] T-040 C# Unity Test 템플릿 설계

- 내용: Unity Test Framework 규칙에 맞는 C# 템플릿(Jinja2) 작성.
- 산출물: `templates/combat_test_csharp.j2`
- 선행 작업: T-020, T-031
- 기간: 1일
- 참조: TRD – 템플릿 예제(Jinja2), PRD – 출력 형식 표( Unity C# )

## [x] T-041 Python unittest/pytest 템플릿 설계

- 내용: Python 테스트 코드 템플릿(Jinja2) 작성.
- 산출물: `templates/combat_test_python.j2`
- 선행 작업: T-040
- 기간: 0.5일
- 참조: PRD – 출력 형식 표(Python unittest), TRD – 테스트 전략

## [x] T-042 JSON 테스트 케이스 스키마 정의 및 템플릿

- 내용: CI/CD용 JSON 스키마 설계 및 생성 로직.
- 산출물: JSON 스키마, 템플릿
- 선행 작업: T-031
- 기간: 0.5일
- 참조: PRD – JSON 출력, TRD – 파일 I/O 스펙

## [x] T-043 템플릿 렌더링 파사드 구현

- 내용: 언어 종류(csharp/python/json)에 따라 알맞은 템플릿을 선택해 렌더링하는 모듈 구현.
- 산출물: `TemplateRenderer` 클래스
- 선행 작업: T-040, T-041, T-042
- 기간: 1일
- 참조: TRD – 템플릿 렌더링 섹션

---

## 6. CLI 인터페이스

## [x] T-050 CLI 커맨드 설계 및 스켈레톤

- 내용: `combattestgen` 엔트리 포인트, `create`, `gui`, `batch` 커맨드 정의.
- 산출물: `src/cli/main.py`
- 선행 작업: T-010, T-020
- 기간: 0.5일
- 참조: TRD – API 스펙 (CLI Commands), PRD – 사용자 여정(명령 예시)

## [x] T-051 `create` 커맨드 구현

- 내용: 파라미터 입력, 검증, 엣지 케이스 생성, 템플릿 렌더링, 파일 저장 전체 플로우 구현.
- 산출물: 완성된 `create` 명령
- 선행 작업: T-043, T-021
- 기간: 1일
- 참조: PRD – 핵심 기능(테스트 케이스 생성), TRD – 파일 I/O 스펙

## [x] T-052 `batch` 커맨드 구현

- 내용: scenarios.yaml 또는 여러 config 파일을 받아 일괄 생성.
- 산출물: `batch` 명령
- 선행 작업: T-051
- 기간: 0.5일
- 참조: TRD – API 스펙 (batch), PRD – 고급 확장(CI/CD 연동)

---

## 7. GUI 인터페이스 (1.0 목표)

## [x] T-060 GUI 와이어프레임 구현

- 내용: PRD의 메인 입력 화면 구조대로 Tkinter/CustomTkinter UI 구현.
- 산출물: GUI 초기 화면
- 선행 작업: T-050
- 기간: 1일
- 참조: PRD – UI/UX 디자인 가이드, TRD – 기술 스택(GUI)

## [x] T-061 GUI ↔ 도메인 로직 연동

- 내용: GUI 입력을 CombatParams로 변환 후 엣지 케이스·템플릿 엔진 호출, 생성 경로 선택 기능 등.
- 산출물: `gui/main_window.py`
- 선행 작업: T-060, T-051
- 기간: 1일
- 참조: PRD – 타겟 사용자(비개발자용 GUI), TRD – 입력/출력 플로우

---

## 8. 빌드·배포

## [x] T-070 PyInstaller 설정 파일(spec) 작성

- 내용: CLI-only, GUI 버전 두 가지 spec 파일 작성.
- 산출물: `build_cli.spec`, `build_gui.spec`
- 선행 작업: T-051, T-061
- 기간: 0.5일
- 참조: TRD – 빌드 및 배포 스크립트, PRD – 플랫폼(Win/macOS/Linux)

## [x] T-071 플랫폼별 빌드 스크립트 작성

- 내용: Windows, macOS, Linux 빌드 스크립트/CI Job 정의.
- 산출물: `scripts/build_*.sh`, CI 설정
- 선행 작업: T-070
- 기간: 0.5일
- 참조: TRD – 빌드 및 배포 스크립트

---

## 9. 테스트·품질

## [x] T-080 단위 테스트 커버리지 확보

- 내용: 도메인, 엣지 케이스, 템플릿, CLI 로직에 대한 단위 테스트 작성, 90% 커버리지 목표.
- 산출물: `tests/unit/*`, 커버리지 리포트
- 선행 작업: T-032, T-043, T-051
- 기간: 2일
- 참조: TRD – 테스트 전략, PRD – KPI(버그 발견률 개선)

## [x] T-081 통합 테스트 (실제 파일 생성)

- 내용: 샘플 입력으로 C#/Python/JSON 파일 생성 후 포맷 및 내용 검증.
- 산출물: `tests/integration/*`
- 선행 작업: T-051, T-061
- 기간: 1일
- 참조: TRD – 통합 테스트, PRD – 사용자 여정(“Unity에서 바로 사용”)

## [x] T-082 성능 테스트(100 케이스 < 2초)

- 내용: 다양한 시나리오 수, 복잡도에서 생성 시간·메모리 측정.
- 산출물: 성능 리포트
- 선행 작업: T-051
- 기간: 0.5일
- 참조: TRD – 성능 요구사항

---

## 10. 문서·릴리즈

## [x] T-090 사용자 가이드 작성

- 내용: CLI 사용법, GUI 튜토리얼, Unity 통합 방법, FAQ 정리.
- 산출물: `docs/user_guide.md`
- 선행 작업: T-051, T-061
- 기간: 1일
- 참조: PRD – 사용자 여정·타겟 사용자, TRD – CLI/API 스펙

## [x] T-091 개발자용 기술 문서 정리

- 내용: 아키텍처 다이어그램, 모듈 설명, 확장 포인트 등 정리.
- 산출물: `docs/dev_guide.md`
- 선행 작업: 전 구간
- 기간: 1일
- 참조: TRD – 시스템 아키텍처, 기술 스택, 데이터 모델

## [x] T-092 v1.0 릴리즈 플랜 및 태깅

- 내용: 릴리즈 노트 작성, Git 태그, 배포 패키지 정리.
- 산출물: 릴리즈 노트, 바이너리
- 선행 작업: T-080~T-082, T-090
- 기간: 0.5일
- 참조: PRD – 구현 로드맵(v1.0 목표), TRD – 빌드·배포

## 11. 추가 요청사항

## [x] T-100 엑셀(.xlsx) 출력 지원

- 내용: 테스트 케이스를 엑셀 형식으로 저장. `openpyxl` 사용.
- 산출물: `TemplateRenderer` 엑셀 지원 업데이트, CLI/GUI 옵션 추가
- 선행 작업: T-043
- 기간: 0.5일