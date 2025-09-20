# game_logic.py
import random
import time

class Game:
    def __init__(self, word_manager, game_data, settings):
        self.word_manager = word_manager
        self.game_data = game_data
        self.max_attempts = settings["max_attempts"]
        self.hint_count = settings["hint_count"]
        self.target_word = ""
        self.guessed_letters = []
        self.attempts_left = 0

    def _format_time(self, seconds):
        """초를 '분 초' 형태로 변환합니다."""
        if seconds < 60:
            return f"{seconds:.2f}초"
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}분 {remaining_seconds}초"

    def _play(self, challenge_mode=False, time_limit=60):
        """핵심 게임 플레이 로직을 수행합니다."""
        if not self.target_word:
            print("\n⚠️ 플레이할 단어가 없습니다. 단어를 먼저 추가해주세요.")
            return

        self.guessed_letters = []
        self.attempts_left = self.max_attempts
        display_word = ['_'] * len(self.target_word)
        start_time = time.time()

        print(f"\n✨ 새로운 게임을 시작합니다! 단어의 길이는 {len(self.target_word)}입니다.")

        while '_' in display_word and self.attempts_left > 0:
            if challenge_mode:
                remaining_time = time_limit - (time.time() - start_time)
                if remaining_time <= 0:
                    print("\n⏳ 시간 초과! 아쉽지만 실패입니다.")
                    self.game_data.record_game(self.target_word, False)
                    self.word_manager.add_to_my_wordbook(self.target_word)
                    return
                print(f"남은 시간: {int(remaining_time)}초")

            print(f"\n현재 단어: {' '.join(display_word)}")
            print(f"남은 시도: {self.attempts_left} | 추측한 알파벳: {', '.join(sorted(self.guessed_letters))}")
            guess = input(">> 알파벳을 추측하거나 '힌트'를 입력하세요: ").lower()

            if guess == '힌트':
                if self.hint_count > 0:
                    self.hint_count -= 1
                    unrevealed_letters = [i for i, char in enumerate(self.target_word) if display_word[i] == '_']
                    if unrevealed_letters:
                        hint_index = random.choice(unrevealed_letters)
                        display_word[hint_index] = self.target_word[hint_index]
                        print(f"💡 힌트! 정답에 '{self.target_word[hint_index]}'가 포함되어 있습니다.")
                    else:
                        print("모든 글자를 이미 찾았습니다!")
                else:
                    print("⚠️ 더 이상 힌트를 사용할 수 없습니다.")
                continue

            if len(guess) != 1 or not guess.isalpha():
                print("⚠️ 알파벳 한 글자만 입력해주세요.")
                continue
            if guess in self.guessed_letters:
                print("⚠️ 이미 추측한 알파벳입니다.")
                continue

            self.guessed_letters.append(guess)

            if guess in self.target_word:
                print(f"👍 '{guess}'가 단어에 포함되어 있습니다!")
                for i, char in enumerate(self.target_word):
                    if char == guess:
                        display_word[i] = char
            else:
                print(f"👎 아쉽네요! '{guess}'는 단어에 없습니다.")
                self.attempts_left -= 1

        if '_' not in display_word:
            elapsed_time = time.time() - start_time
            formatted_time = self._format_time(elapsed_time)
            print(f"\n🎉 축하합니다! 정답 '{self.target_word}'을(를) 맞추셨습니다!")
            print(f"걸린 시간: {formatted_time}")
            self.game_data.record_game(self.target_word, True, elapsed_time)
        else:
            print(f"\nGAME OVER. 정답은 '{self.target_word}'였습니다.")
            self.game_data.record_game(self.target_word, False)
            self.word_manager.add_to_my_wordbook(self.target_word)

    def start_game_by_level(self, level):
        level_map = {'1': '초급', '2': '중급', '3': '고급'}
        if level in level_map:
            self.target_word = self.word_manager.get_word_by_level(level_map[level])
            self._play()
        else:
            print("⚠️ 잘못된 난이도 선택입니다.")

    def start_game_by_topic(self, topic_choice):
        topics = self.word_manager.get_available_topics()
        try:
            index = int(topic_choice) - 1
            if 0 <= index < len(topics):
                chosen_topic = topics[index]
                self.target_word = self.word_manager.get_word_by_topic(chosen_topic)
                self._play()
            else:
                print("⚠️ 잘못된 번호입니다.")
        except (ValueError, IndexError):
            print("⚠️ 잘못된 입력입니다. 목록에 있는 번호를 입력해주세요.")


    def start_hint_mode(self, ui):
        """[수정] 힌트 모드 시작 전 주제를 선택받습니다."""
        topics = self.word_manager.get_available_topics()
        if not topics:
            print("\n⚠️ 플레이할 단어가 없습니다. 단어를 먼저 추가해주세요.")
            return

        ui.display_topic_menu(topics)
        topic_choice = input(">> 힌트 모드를 플레이할 주제를 선택하세요: ")

        try:
            index = int(topic_choice) - 1
            if 0 <= index < len(topics):
                chosen_topic = topics[index]
                self.target_word = self.word_manager.get_word_by_topic(chosen_topic)
            else:
                print("⚠️ 잘못된 번호입니다.")
                return
        except (ValueError, IndexError):
            print("⚠️ 잘못된 입력입니다. 목록에 있는 번호를 입력해주세요.")
            return

        if not self.target_word:
            print("\n⚠️ 단어를 불러오지 못했습니다.")
            return

        display_word = ['_'] * len(self.target_word)
        hint_count = len(self.target_word) // 3
        hint_indices = random.sample(range(len(self.target_word)), hint_count)

        for i in hint_indices:
            display_word[i] = self.target_word[i]

        print("✨ [힌트 모드] 일부 글자가 미리 채워진 상태로 시작합니다!")
        self._play_with_initial_state(display_word)


    def start_challenge_mode(self):
        self.target_word = self.word_manager.get_random_word()
        print("⏱️ [챌린지 모드] 60초 안에 단어를 맞춰보세요!")
        self._play(challenge_mode=True, time_limit=60)

    def _play_with_initial_state(self, initial_display):
        if not self.target_word:
            return

        self.guessed_letters = [c for c in initial_display if c != '_']
        self.attempts_left = self.max_attempts
        display_word = initial_display
        start_time = time.time()

        print(f"\n✨ 새로운 게임을 시작합니다! 단어의 길이는 {len(self.target_word)}입니다.")

        while '_' in display_word and self.attempts_left > 0:
            print(f"\n현재 단어: {' '.join(display_word)}")
            print(f"남은 시도: {self.attempts_left} | 추측한 알파벳: {', '.join(sorted(self.guessed_letters))}")
            guess = input(">> 알파벳을 추측하세요: ").lower()

            if len(guess) != 1 or not guess.isalpha():
                print("⚠️ 알파벳 한 글자만 입력해주세요.")
                continue
            if guess in self.guessed_letters:
                print("⚠️ 이미 추측한 알파벳입니다.")
                continue

            self.guessed_letters.append(guess)

            if guess in self.target_word:
                print(f"👍 '{guess}'가 단어에 포함되어 있습니다!")
                for i, char in enumerate(self.target_word):
                    if char == guess:
                        display_word[i] = char
            else:
                print(f"👎 아쉽네요! '{guess}'는 단어에 없습니다.")
                self.attempts_left -= 1
        
        if '_' not in display_word:
            elapsed_time = time.time() - start_time
            formatted_time = self._format_time(elapsed_time)
            print(f"\n🎉 축하합니다! 정답 '{self.target_word}'을(를) 맞추셨습니다!")
            print(f"걸린 시간: {formatted_time}")
            self.game_data.record_game(self.target_word, True, elapsed_time)
        else:
            print(f"\nGAME OVER. 정답은 '{self.target_word}'였습니다.")
            self.game_data.record_game(self.target_word, False)
            self.word_manager.add_to_my_wordbook(self.target_word)