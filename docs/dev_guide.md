# CombatTestGen 개발자 가이드

## 아키텍처 개요

CombatTestGen은 3계층 아키텍처를 따릅니다.

1. **Input Layer**: CLI (`src/cli`) 및 GUI (`src/gui`)
2. **Domain Layer**: 
    - `models.py`: Pydantic 데이터 모델
    - `edge_cases.py`: 테스트 케이스 생성 알고리즘
    - `template_renderer.py`: Jinja2 템플릿 엔진 래퍼
3. **Output Layer**: 파일 시스템 저장

## 프로젝트 구조

```text
src/
├── cli/           # Typer CLI 구현
├── gui/           # CustomTkinter GUI 구현
├── domain/        # 비즈니스 로직 (핵심)
│   ├── models.py
│   ├── edge_cases.py
│   └── template_renderer.py
└── templates/     # Jinja2 템플릿 (.j2)
    ├── combat_test_csharp.j2
    └── ...
```

## 개발 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
./venv/Scripts/activate

# 의존성 설치
pip install -r requirements.txt
```

## 테스트 실행

```bash
# 단위 테스트
pytest tests/unit

# 통합 테스트
pytest tests/integration

# 성능 테스트
python -m tests.performance_test
```

## 빌드 방법

PyInstaller를 사용하여 단일 실행 파일을 생성합니다.

```bash
# Windows
scripts/build_windows.bat

# macOS/Linux
scripts/build_unix.sh
```

결과물은 `dist/` 폴더에 생성됩니다.
