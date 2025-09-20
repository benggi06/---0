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

            # 힌트 기능
            if guess == '힌트':
                if self.hint_count > 0:
                    self.hint_count -= 1
                    # 아직 안 나온 글자 중 하나를 공개
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

            # 입력 유효성 검사
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

        # 게임 결과
        if '_' not in display_word:
            elapsed_time = time.time() - start_time
            print(f"\n🎉 축하합니다! 정답 '{self.target_word}'을(를) 맞추셨습니다!")
            print(f"걸린 시간: {elapsed_time:.2f}초")
            self.game_data.record_game(self.target_word, True, elapsed_time)
        else:
            print(f"\nGAME OVER. 정답은 '{self.target_word}'였습니다.")
            self.game_data.record_game(self.target_word, False)
            self.word_manager.add_to_my_wordbook(self.target_word)

    def start_game_by_level(self, level):
        """난이도별 게임 시작"""
        level_map = {'1': '초급', '2': '중급', '3': '고급'}
        if level in level_map:
            self.target_word = self.word_manager.get_word_by_level(level_map[level])
            self._play()
        else:
            print("⚠️ 잘못된 난이도 선택입니다.")

    def start_game_by_topic(self, topic):
        """주제별 게임 시작"""
        self.target_word = self.word_manager.get_word_by_topic(topic)
        self._play()

    def start_hint_mode(self):
        """힌트 모드 게임 시작 (글자 일부 미리 채우기)"""
        self.target_word = self.word_manager.get_random_word()
        if not self.target_word:
            print("\n⚠️ 플레이할 단어가 없습니다.")
            return

        display_word = ['_'] * len(self.target_word)
        # 단어 길이의 30% 만큼 힌트 제공
        hint_count = len(self.target_word) // 3
        hint_indices = random.sample(range(len(self.target_word)), hint_count)

        for i in hint_indices:
            display_word[i] = self.target_word[i]

        print("✨ [힌트 모드] 일부 글자가 미리 채워진 상태로 시작합니다!")
        # 기존 _play 로직을 수정하여 초기 상태를 전달하며 실행
        # 이 부분은 _play 함수를 수정하여 초기 display_word를 받을 수 있도록 확장해야 함
        self._play_with_initial_state(display_word)


    def start_challenge_mode(self):
        """챌린지 모드 게임 시작 (시간 제한)"""
        self.target_word = self.word_manager.get_random_word()
        print("⏱️ [챌린지 모드] 60초 안에 단어를 맞춰보세요!")
        self._play(challenge_mode=True, time_limit=60)

    def _play_with_initial_state(self, initial_display):
        """특정 상태에서 게임을 시작하는 내부 함수 (힌트 모드용)"""
        # _play 로직과 유사하지만, display_word 초기값을 받아옴
        if not self.target_word:
            print("\n⚠️ 플레이할 단어가 없습니다.")
            return

        self.guessed_letters = [c for c in initial_display if c != '_']
        self.attempts_left = self.max_attempts
        display_word = initial_display

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
            print(f"\n🎉 축하합니다! 정답 '{self.target_word}'을(를) 맞추셨습니다!")
            self.game_data.record_game(self.target_word, True)
        else:
            print(f"\nGAME OVER. 정답은 '{self.target_word}'였습니다.")
            self.game_data.record_game(self.target_word, False)
            self.word_manager.add_to_my_wordbook(self.target_word)