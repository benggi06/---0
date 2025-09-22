# main.py
import os
from game_logic import Game
from word_manager import WordManager
from ui import UI
from game_data import GameData

def main():
    if not os.path.exists('word_lists'):
        os.makedirs('word_lists')
    if not os.path.exists('data'):
        os.makedirs('data')

    word_manager = WordManager()
    game_data = GameData()
    ui = UI()

    settings = {
        "max_attempts": 6,
        "hint_count": 2
    }

    while True:
        ui.display_main_menu()
        choice = input(">> 메뉴를 선택하세요: ")

        if choice == '1':
            game_mode_menu(word_manager, game_data, settings, ui)
        elif choice == '2':
            learning_menu(word_manager)
        elif choice == '3':
            management_menu(word_manager, game_data, settings)
        elif choice == '4':
            print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 1에서 4 사이의 숫자를 입력해주세요.")


def game_mode_menu(word_manager, game_data, settings, ui):
    while True:
        ui.display_game_mode_menu()
        choice = input(">> 게임 모드를 선택하세요: ")
        game = Game(word_manager, game_data, settings)

        if choice == '1':
            ui.display_difficulty_menu()
            level_choice = input(">> 난이도를 선택하세요: ")
            game.start_game_by_level(level_choice)
        elif choice == '2':
            ui.display_topic_menu(word_manager.get_available_topics())
            topic_choice = input(">> 주제를 선택하세요: ")
            game.start_game_by_topic(topic_choice)
        elif choice == '3':
            game.start_hint_mode(ui)
        elif choice == '4':
            game.start_challenge_mode()
        elif choice == '5':
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 다시 선택해주세요.")

def learning_menu(word_manager):
    ui = UI()
    while True:
        ui.display_learning_menu()
        choice = input(">> 학습 메뉴를 선택하세요: ")
        if choice == '1':
            word = input(">> 뜻을 찾아볼 단어를 입력하세요: ")
            word_manager.show_word_meaning(word)
        elif choice == '2':
            word_manager.manage_my_wordbook()
        elif choice == '3':
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 다시 선택해주세요.")

def management_menu(word_manager, game_data, settings):
    ui = UI()
    while True:
        ui.display_management_menu()
        choice = input(">> 관리 메뉴를 선택하세요: ")
        if choice == '1':
            ui.display_how_to_play()
        elif choice == '2':
            word_manager.manage_words()
        elif choice == '3':
            game_data.show_records()
        elif choice == '4':
            configure_settings(settings)
        elif choice == '5':
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 다시 선택해주세요.")

def configure_settings(settings):
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