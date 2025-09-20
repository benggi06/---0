# main.py
import os
from game_logic import Game
from word_manager import WordManager
from ui import UI
from game_data import GameData

def main():
    """
    게임의 메인 루프를 실행합니다.
    사용자 메뉴를 표시하고 선택에 따라 해당 기능을 실행합니다.
    """
    # 초기 설정
    if not os.path.exists('word_lists'):
        os.makedirs('word_lists')
    if not os.path.exists('data'):
        os.makedirs('data')

    word_manager = WordManager()
    game_data = GameData()
    ui = UI()

    # 기본 게임 설정 값
    settings = {
        "max_attempts": 6,
        "hint_count": 2
    }

    while True:
        ui.display_main_menu()
        choice = input(">> 메뉴를 선택하세요: ")

        # 1. 게임 플레이 모드
        if choice == '1':
            game_mode_menu(word_manager, game_data, settings)
        # 2. 학습 효과 증진 메뉴
        elif choice == '2':
            learning_menu(word_manager)
        # 3. 게임 관리 및 설정
        elif choice == '3':
            management_menu(word_manager, game_data, settings)
        # 4. 게임 종료
        elif choice == '4':
            print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 1에서 4 사이의 숫자를 입력해주세요.")


def game_mode_menu(word_manager, game_data, settings):
    """게임 플레이 모드 메뉴를 처리합니다."""
    ui = UI()
    while True:
        ui.display_game_mode_menu()
        choice = input(">> 게임 모드를 선택하세요: ")
        game = Game(word_manager, game_data, settings)

        if choice == '1': # 난이도별 게임
            ui.display_difficulty_menu()
            level_choice = input(">> 난이도를 선택하세요: ")
            game.start_game_by_level(level_choice)
        elif choice == '2': # 주제별 단어장
            ui.display_topic_menu(word_manager.get_available_topics())
            topic_choice = input(">> 주제를 선택하세요: ")
            game.start_game_by_topic(topic_choice)
        elif choice == '3': # 힌트 모드
            game.start_hint_mode()
        elif choice == '4': # 챌린지 모드
            game.start_challenge_mode()
        elif choice == '5': # 메인 메뉴로 돌아가기
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 다시 선택해주세요.")

def learning_menu(word_manager):
    """학습 효과 증진 메뉴를 처리합니다."""
    ui = UI()
    while True:
        ui.display_learning_menu()
        choice = input(">> 학습 메뉴를 선택하세요: ")
        if choice == '1': # 단어 학습 (예시 기능)
            word = input(">> 뜻을 찾아볼 단어를 입력하세요: ")
            word_manager.show_word_meaning(word)
        elif choice == '2': # 나만의 단어장
            word_manager.manage_my_wordbook()
        elif choice == '3': # 메인 메뉴로 돌아가기
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 다시 선택해주세요.")

def management_menu(word_manager, game_data, settings):
    """게임 관리 및 설정 메뉴를 처리합니다."""
    ui = UI()
    while True:
        ui.display_management_menu()
        choice = input(">> 관리 메뉴를 선택하세요: ")
        if choice == '1': # 게임 방법
            ui.display_how_to_play()
        elif choice == '2': # 단어 관리
            word_manager.manage_words()
        elif choice == '3': # 게임 기록
            game_data.show_records()
        elif choice == '4': # 설정
            configure_settings(settings)
        elif choice == '5': # 메인 메뉴로 돌아가기
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 다시 선택해주세요.")

def configure_settings(settings):
    """게임 세부 규칙을 설정합니다."""
    print("\n[⚙️ 게임 설정]")
    try:
        max_attempts = int(input(f"최대 시도 횟수를 입력하세요 (현재: {settings['max_attempts']}): "))
        hint_count = int(input(f"힌트 사용 횟수를 입력하세요 (현재: {settings['hint_count']}): "))
        settings["max_attempts"] = max_attempts
        settings["hint_count"] = hint_count
        print("✨ 설정이 성공적으로 저장되었습니다.")
    except ValueError:
        print("⚠️ 숫자로만 입력해주세요.")


if __name__ == "__main__":
    main()