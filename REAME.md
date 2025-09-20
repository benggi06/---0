🐍 파이썬 교육용 행맨 게임 (Python Educational Hangman Game)
이 프로젝트는 파이썬(Python)으로 제작된 교육용 행맨 게임입니다. 사용자는 다양한 게임 모드와 학습 기능을 통해 재미있게 단어를 익힐 수 있습니다.

✨ 주요 기능
다양한 게임 모드

난이도별 게임: 초급, 중급, 고급 등 수준에 맞는 단어장으로 게임을 즐길 수 있습니다.

주제별 단어장: 동물, 음식, 직업 등 특정 주제의 단어들로 게임을 플레이합니다.

힌트 모드: 단어의 일부 글자가 미리 채워진 상태로 시작하여 난이도를 낮춥니다.

챌린지 모드: 시간 제한을 두어 긴장감과 몰입도를 높입니다.

학습 효과 증진

단어 학습: 게임에 나온 단어의 뜻과 예문을 확인할 수 있습니다.

나만의 단어장: 게임 중 틀렸던 단어들이 자동으로 저장되어 복습이 가능합니다.

게임 관리 및 설정

단어 관리: 사용자가 직접 원하는 단어를 주제별로 추가할 수 있습니다.

게임 기록: 총 플레이 횟수, 승률, 최고 기록 등 자신의 학습 성과를 확인할 수 있습니다.

개인 설정: 최대 시도 횟수나 힌트 개수 등 게임 규칙을 직접 변경할 수 있습니다.

🚀 실행 방법
사전 준비
Python 3가 설치되어 있어야 합니다. python.org에서 설치할 수 있습니다.

설치 및 실행 순서
프로젝트 파일 다운로드
모든 .py 파일을 하나의 폴더 안에 저장합니다.

main.py

game_logic.py

word_manager.py

game_data.py

ui.py

단어 목록 폴더 생성
.py 파일들이 있는 곳에 word_lists 라는 이름의 새 폴더를 만듭니다.

단어 목록 파일 생성
word_lists 폴더 안에 아래와 같이 텍스트 파일(.txt)을 만들고 원하는 단어를 한 줄에 하나씩 입력합니다. (파일 이름이 곧 게임 내 '주제'가 됩니다.)

animals.txt

Plaintext

lion
tiger
bear
...
foods.txt

Plaintext

pizza
pasta
sushi
...
professions.txt

Plaintext

doctor
nurse
teacher
...
게임 실행
터미널(Windows의 경우 CMD 또는 PowerShell, macOS의 경우 Terminal)을 열고, 프로젝트 파일이 저장된 폴더로 이동한 뒤 아래 명령어를 입력하여 게임을 실행합니다.

Bash

python main.py
🎮 게임 방법
게임을 실행하면 메인 메뉴가 나타납니다.

원하는 메뉴의 번호를 입력하여 선택합니다.

'게임 플레이 모드'를 선택하면 난이도, 주제 등을 고를 수 있습니다.

게임이 시작되면 알파벳 한 글자를 입력하여 단어를 추측합니다.

모든 글자를 맞히면 승리, 주어진 기회를 모두 사용하면 패배합니다.

📂 파일 구조
프로젝트는 아래와 같은 구조로 구성되어야 합니다.

your-project-folder/
├── 📄 main.py
├── 📄 game_logic.py
├── 📄 word_manager.py
├── 📄 game_data.py
├── 📄 ui.py
│
└── 📁 word_lists/
    ├── 📄 animals.txt
    ├── 📄 foods.txt
    └── 📄 professions.txt
(게임 실행 시 data 폴더는 자동으로 생성됩니다.)