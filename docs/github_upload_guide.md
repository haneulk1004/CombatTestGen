# GitHub 업로드 가이드

이미 로컬 저장소 초기화와 첫 번째 커밋(`Initial commit`)은 완료된 상태입니다.
아래 순서대로 진행하여 GitHub에 업로드하세요.

## 1. GitHub 저장소 생성
1. [GitHub](https://github.com/new)에 로그인하여 **New repository**를 클릭합니다.
2. **Repository name**에 `CombatTestGen` (또는 원하는 이름)을 입력합니다.
3. **Public** 또는 **Private**을 선택합니다.
4. **Initialize this repository with:** 섹션에서는 **아무것도 체크하지 마세요** (README, .gitignore 등).
5. **Create repository** 버튼을 클릭합니다.

## 2. 코드 푸시 (터미널 명령어)
GitHub 저장소가 생성되면, 화면에 나오는 명령어 중 **"…or push an existing repository from the command line"** 부분을 참고하거나 아래 명령어를 실행하세요.

터미널(CMD/PowerShell)을 열고 프로젝트 폴더(`f:\Vibe_coding\전투_테스트케이스`)에서 다음을 입력합니다:

```bash
# URL 부분을 본인의 GitHub 저장소 주소로 변경하세요
git remote add origin https://github.com/<사용자ID>/CombatTestGen.git

git branch -M main
git push -u origin main
```

## 3. 확인
GitHub 페이지를 새로고침하면 코드가 업로드된 것을 확인할 수 있습니다.
- `dist/` 폴더는 `.gitignore`에 의해 제외되었습니다. (실행 파일은 보통 릴리스(Releases) 탭에 별도로 올립니다)
