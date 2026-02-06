## TRD 개요
> **Version**: 1.0
> **Status**: Final
> **Last Updated**: 2026-02-06


CombatTestGen **Technical Requirements Document**(TRD)는 Python 기반 독립 실행 프로그램의 기술 구현 세부 사항을 정의합니다. PRD의 기능 요구사항을 충족하는 아키텍처, API 스펙, 데이터 모델, 성능 기준을 기술합니다.

## 시스템 아키텍처

`text┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Layer   │───▶│  Template Engine │───▶│  Output Layer   │
│ CLI/GUI/JSON    │    │   Jinja2         │    │ C#/Python/JSON  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Parameter      │    │   EdgeCase       │    │   FileSystem    │
│  Validator      │    │   Generator      │    │   Writer        │
└─────────────────┘    └──────────────────┘    └─────────────────┘`

## 기술 스택 상세

| **컴포넌트** | **기술** | **버전** | **역할** |
| --- | --- | --- | --- |
| CLI | Click/Typer | 8.1+ | 명령행 인터페이스 |
| GUI | CustomTkinter | 5.2+ | 크로스플랫폼 UI |
| 템플릿 | Jinja2 | 3.1+ | 테스트 코드 생성 |
| 데이터 | Pydantic | 2.5+ | 입력 검증 |
| 배포 | PyInstaller | 6.8+ | 독립 실행 파일 |

## 데이터 모델 (Pydantic)

`pythonfrom pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Scenario(str, Enum):
    NORMAL = "normal"
    CRITICAL = "critical"
    DODGE = "dodge"
    DEATH = "death"

class CombatParams(BaseModel):
    player_damage: int = Field(..., ge=0, le=9999)
    enemy_hp: int = Field(..., ge=1, le=999999)
    scenarios: List[Scenario] = Field(default=[Scenario.NORMAL])
    output_path: str = Field(default="./CombatTests.cs")
    language: str = Field(default="csharp", regex="^(csharp|python|json)$")`

## API 스펙 (CLI Commands)

`text# 기본 생성
combattestgen create --damage 50 --hp 100 --scenarios normal,critical

# JSON 입력
combattestgen create --config combat_params.json

# GUI 실행
combattestgen gui

# 배치 모드
combattestgen batch --scenarios-file scenarios.yaml --output-dir ./tests/`

## 핵심 알고리즘

## 1. 엣지 케이스 생성기

`text입력: player_damage=50, enemy_hp=100
출력 케이스:
1. Normal: 100 → 50
2. Critical: 100 → 0 (2배 데미지)
3. ZeroDamage: 100 → 100 (데미지 0)
4. Overkill: 100 → 0 (데미지 150)
5. DeathFlow: HP 0 → DropItem()`

## 2. 템플릿 렌더링

`text[Test, Description("{{ scenario.name }} - {{ player_damage }}dmg")]
public void Test{{ scenario.upper() }}_{{ player_damage }}dmg_{{ enemy_hp }}hp()
{
    // GIVEN
    EnemyHealth hp = new EnemyHealth({{ enemy_hp }});
    
    // WHEN
    Player attacks with {{ player_damage }} damage
    
    // THEN
    Assert.Equals({{ expected_hp }}, hp.Current);
}`

## 파일 I/O 스펙

| **입력 파일** | **형식** | **필수** | **예시** |
| --- | --- | --- | --- |
| config.json | JSON | 선택 | `{"damage":50, "hp":100}` |
| scenarios.yaml | YAML | 선택 | `normal: {multiplier:1.0}` |

| **출력 파일** | **형식** | **내용** |
| --- | --- | --- |
| CombatTests.cs | C# | Unity Test Framework |
| test_combat.py | Python | pytest/unittest |
| test_cases.json | JSON | CI/CD용 |

## 성능 요구사항

- **생성 속도**: 100 케이스 < 2초
- **메모리**: < 100MB
- **파일 크기**: 출력 파일 < 500KB
- **동시 실행**: 10+ 인스턴스 안정적

## 빌드 및 배포 스크립트

`bash# 개발
pip install -r requirements.txt
python src/main.py

# 빌드 (Windows)
pyinstaller build.spec --onefile --windowed --name CombatTestGen.exe

# 빌드 (macOS/Linux)
pyinstaller build.spec --onefile --name CombatTestGen`

## 테스트 전략

`text# 단위 테스트 (90% 커버리지 목표)
pytest tests/unit/ --cov=src/ --cov-report=html

# 통합 테스트
pytest tests/integration/  # 실제 C# 파일 생성 검증

# 성능 테스트
locust -f tests/load_test.py --users 50 --spawn-rate 5`

## 에러 핸들링

`text입력 오류: "데미지가 음수입니다. 0 이상 입력하세요."
템플릿 오류: "Jinja2 렌더링 실패: [상세 로그]"
파일 I/O 오류: "경로 접근 불가: [경로]. 대체 위치 [/tmp] 사용"`

## 로깅 및 모니터링

`textINFO: CombatTestGen v1.0.0 시작
DEBUG: 5개 시나리오 처리 중 (normal, critical...)
INFO: CombatTests.cs 생성 완료 (12KB, 8 tests)
ERROR: 출력 경로 쓰기 실패 → /tmp/CombatTests.cs 저장`