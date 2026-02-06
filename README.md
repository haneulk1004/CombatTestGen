# ⚔️ Combat Test Case Generator (전투 테스트 케이스 생성기)

**게임 전투 로직 검증을 위한 테스트 케이스 자동 생성 도구**

이 도구는 플레이어 데미지와 적 HP를 입력하면, 게임 개발에 필요한 다양한 전투 시나리오(정상, 치명타, 회피, 오버킬 등)를 자동으로 계산하여 테스트 케이스 파일로 만들어줍니다.

## ✨ 주요 기능
- **다양한 시나리오 지원**: 일반 공격, 치명타(2배), 회피(0 데미지), 사망 확인 등 필수 엣지 케이스 자동 생성.
- **대량 생성 (Random Variations)**: 입력값의 ±20% 범위에서 수십~수백 개의 무작위 테스트 케이스 추가 생성.
- **다국어 출력**:
  - 📊 **Excel**: 기획자/QA가 보기 편한 엑셀 보고서 형식
  - 🐍 **Python**: `unittest` 기반 코드
  - #️⃣ **C#**: Unity `NUnit` 기반 코드
  - 📄 **JSON**: CI/CD 파이프라인 연동용
- **쉬운 사용**: 설치가 필요 없는 실행 파일(`.exe`) 및 직관적인 GUI 제공.

## 🚀 사용/설치 방법

### 1. 실행 파일 사용 (Windows)
Python을 설치할 필요 없이 바로 사용할 수 있습니다.
1. [Releases](https://github.com/haneulk1004/CombatTestGen/releases) 페이지에서 최신 `CombatTestGen.exe` 다운로드
2. 파일 더블 클릭 → **GUI 모드** 실행
3. 수치 입력 후 **"Generate"** 클릭!

### 2. 소스 코드 실행 (개발자용)
Python 3.11 이상이 필요합니다.

```bash
# 1. 저장소 복제
git clone https://github.com/haneulk1004/CombatTestGen.git
cd CombatTestGen

# 2. 의존성 설치
pip install -r requirements.txt

# 3. GUI 실행
python -m src.cli.main gui

# 4. CLI 실행 예시
python -m src.cli.main create --damage 100 --hp 500 --random-count 20
```

## 📖 문서 (Documents)
- [사용자 가이드 (User Guide)](docs/user_guide.md): 자세한 프로그램 사용법
- [개발자 가이드 (Dev Guide)](docs/dev_guide.md): 프로젝트 구조 및 빌드 방법
- [기능 명세서 (PRD)](docs/PRD.md): 상세 기능 요구사항

## 🛠️ 기술 스택
- **Language**: Python 3.11+
- **GUI**: CustomTkinter
- **CLI**: Typer
- **Core**: Jinja2 (Templating), Pydantic (Validation), OpenPyXL (Excel)
- **Build**: PyInstaller

## 📄 라이선스
MIT License
