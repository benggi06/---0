# ui.py

class UI:
    def display_main_menu(self):
        print("\n" + "="*30)
        print("    🐍 파이썬 행맨 게임 🐍")
        print("="*30)
        print("1. 게임 플레이 모드")
        print("2. 학습 효과 증진 메뉴")
        print("3. 게임 관리 및 설정")
        print("4. 게임 종료")
        print("="*30)

    def display_game_mode_menu(self):
        print("\n[🎮 게임 플레이 모드]")
        print("1. 난이도별 게임 (초급/중급/고급)")
        print("2. 주제별 단어장")
        print("3. 힌트 모드 (일부 글자 채우고 시작)")
        print("4. 챌린지 모드 (시간 제한)")
        print("5. 메인 메뉴로 돌아가기")

    def display_difficulty_menu(self):
        print("\n[📊 난이도 선택]")
        print("1. 초급 (동물)")
        print("2. 중급 (음식)")
        print("3. 고급 (직업)")

    def display_topic_menu(self, topics):
        print("\n[🎨 주제 선택]")
        if not topics:
            print("선택할 수 있는 주제가 없습니다. 단어를 먼저 추가해주세요.")
            return
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")

    def display_learning_menu(self):
        print("\n[🧠 학습 효과 증진 메뉴]")
        print("1. 단어 학습 (뜻/예문 보기)")
        print("2. 나만의 단어장 (틀린 단어 복습)")
        print("3. 메인 메뉴로 돌아가기")

    def display_management_menu(self):
        print("\n[🛠️ 게임 관리 및 설정]")
        print("1. 게임 방법 보기")
        print("2. 단어 관리 (추가/목록 보기)")
        print("3. 게임 기록 보기")
        print("4. 설정")
        print("5. 메인 메뉴로 돌아가기")

    def display_how_to_play(self):
        print("\n[📜 게임 방법]")
        print("1. 프로그램이 단어를 하나 선택합니다.")
        print("2. 단어의 길이만큼 빈칸('_')이 표시됩니다.")
        print("3. 알파벳을 하나씩 추측하여 입력합니다.")
        print("4. 추측한 알파벳이 단어에 포함되면 해당 칸이 채워집니다.")
        print("5. 포함되지 않으면 시도 횟수가 1회 차감됩니다.")
        print("6. 모든 글자를 맞추면 승리, 시도 횟수를 모두 소진하면 패배합니다.")