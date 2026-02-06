# CombatTestGen 사용자 가이드

> **Version**: v1.0
> **Date**: 2026-02-06

CombatTestGen은 게임 전투 시스템의 테스트 케이스를 자동으로 생성해주는 도구입니다.

## 1. 설치 방법

### Windows
1. 배포된 `CombatTestGen.exe` 파일을 다운로드합니다.
2. 원하는 폴더에 압축을 풉니다.
3. 바로 실행 가능합니다.

### Source Code 실행
```bash
git clone https://github.com/your-repo/combattestgen.git
cd combattestgen
pip install -r requirements.txt
python -m src.cli.main gui
```

## 2. GUI 사용법 (권장)

1. **프로그램 실행**: `CombatTestGen.exe`를 실행하면 메인 창이 열립니다.
2. **파라미터 입력**:
   - `플레이어 데미지`: 플레이어의 공격력 (0~9999)
   - `적 HP`: 적의 체력 (1~999999)
3. **시나리오 선택**:
   - `기본(Normal)`: 일반 공격 테스트
   - `치명타(Critical)`: 2배 데미지 테스트
   - `회피(Dodge)`: 데미지 0 처리 테스트
   - `사망(Death)`: HP가 0이 되는지 확인
4. **저장 설정**:
   - `저장 경로`: 생성될 파일의 위치를 선택 (예: `Assets/Tests/CombatTests.cs`)
   - `언어`: Unity C#, Python, JSON 중 선택
5. **생성**: `테스트 케이스 생성` 버튼 클릭

> **Tip**: 생성된 스크립트를 Unity 프로젝트의 `Assets/Tests` 폴더에 넣으면 Unity Test Runner에서 즉시 실행됩니다.

## 3. CLI 사용법 (자동화용)

터미널(CMD/PowerShell)에서 다음과 같이 실행합니다.

### 단일 파일 생성
```bash
combattestgen create --damage 50 --hp 100 --scenarios normal,critical --output ./MyTests.cs
```

### 배치 생성 (여러 설정 일괄 처리)
JSON 설정 파일들이 있는 폴더를 지정하여 한 번에 생성합니다.

```bash
combattestgen batch --config-dir ./inputs --output-dir ./outputs
```
