# word_manager.py
import os
import random
import json

class WordManager:
    def __init__(self):
        self.word_lists_path = "word_lists"
        self.my_wordbook_path = "data/my_wordbook.json"
        self.word_meaning_path = "data/word_meanings.json"
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        if not os.path.exists(self.word_lists_path):
            os.makedirs(self.word_lists_path)
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.my_wordbook_path):
            with open(self.my_wordbook_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        if not os.path.exists(self.word_meaning_path):
            sample_meanings = {
                "apple": {"meaning": "사과", "example": "An apple a day keeps the doctor away."},
                "banana": {"meaning": "바나나", "example": "Monkeys love to eat bananas."},
                "developer": {"meaning": "개발자", "example": "A software developer writes code."}
            }
            with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
                json.dump(sample_meanings, f, ensure_ascii=False, indent=4)

    def get_word_list(self, filename):
        try:
            with open(os.path.join(self.word_lists_path, filename), 'r', encoding='utf-8') as f:
                words = [line.strip().lower() for line in f if line.strip()]
            return words
        except FileNotFoundError:
            return []

    def get_available_topics(self):
        try:
            files = [f.split('.')[0] for f in os.listdir(self.word_lists_path) if f.endswith('.txt')]
            return files
        except FileNotFoundError:
            return []

    def get_word_by_topic(self, topic):
        words = self.get_word_list(f"{topic}.txt")
        return random.choice(words) if words else None

    def get_word_by_level(self, level):
        level_topic_map = {
            '초급': 'animals',
            '중급': 'foods',
            '고급': 'professions'
        }
        topic = level_topic_map.get(level)
        if topic:
            return self.get_word_by_topic(topic)
        return self.get_random_word()

    def get_random_word(self):
        all_words = []
        topics = self.get_available_topics()
        if not topics:
            return None
        for topic in topics:
            all_words.extend(self.get_word_list(f"{topic}.txt"))
        return random.choice(all_words) if all_words else None

    def manage_words(self):
        while True:
            print("\n[📖 단어 관리]")
            print("1. 단어 추가하기")
            print("2. 단어 삭제하기")
            print("3. 전체 단어 목록 보기")
            print("4. 돌아가기")
            choice = input(">> 선택: ")

            if choice == '1':
                topic = input("추가할 단어의 주제(파일 이름)를 입력하세요 (예: animals): ").lower()
                word = input("추가할 단어를 입력하세요: ").lower()
                self.add_word(topic, word)
            elif choice == '2':
                topic = input("삭제할 단어의 주제(파일 이름)를 입력하세요: ").lower()
                word = input("삭제할 단어를 입력하세요: ").lower()
                self.delete_word(topic, word)
            elif choice == '3':
                self.view_all_words()
            elif choice == '4':
                break
            else:
                print("⚠️ 잘못된 입력입니다.")

    def add_word(self, topic, word):
        if not word.isalpha():
            print("⚠️ 알파벳으로만 구성된 단어를 입력해주세요.")
            return
        filepath = os.path.join(self.word_lists_path, f"{topic}.txt")
        existing_words = self.get_word_list(f"{topic}.txt")
        if word in existing_words:
            print(f"⚠️ 단어 '{word}'은(는) 이미 주제 '{topic}'에 존재합니다.")
            return

        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n{word}")
        print(f"✅ 주제 '{topic}'에 단어 '{word}'이(가) 추가되었습니다.")

    def delete_word(self, topic, word_to_delete):
        filepath = os.path.join(self.word_lists_path, f"{topic}.txt")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            
            if word_to_delete in words:
                words.remove(word_to_delete)
                with open(filepath, 'w', encoding='utf-8') as f:
                    for word in words:
                        f.write(f"{word}\n")
                print(f"✅ 주제 '{topic}'에서 단어 '{word_to_delete}'을(를) 삭제했습니다.")
            else:
                print(f"⚠️ 주제 '{topic}'에 '{word_to_delete}' 단어가 존재하지 않습니다.")
        except FileNotFoundError:
            print(f"⚠️ '{topic}'이라는 주제(파일)를 찾을 수 없습니다.")

    def view_all_words(self):
        topics = self.get_available_topics()
        if not topics:
            print("⚠️ 추가된 단어가 없습니다.")
            return
        
        for topic in topics:
            words = self.get_word_list(f"{topic}.txt")
            if words:
                print(f"\n--- 주제: {topic} ---")
                print(', '.join(words))

    # --- 학습 효과 증진 기능 ---
    def show_word_meaning(self, word):
        try:
            with open(self.word_meaning_path, 'r', encoding='utf-8') as f:
                meanings = json.load(f)
            info = meanings.get(word.lower())
            if info:
                print(f"\n--- '{word}' 단어 정보 ---")
                print(f"뜻: {info['meaning']}")
                print(f"예문: {info['example']}")
            else:
                print(f"⚠️ '{word}' 단어의 정보를 찾을 수 없습니다.")
        except FileNotFoundError:
            print("⚠️ 단어 정보 파일이 없습니다.")

    # 👇👇👇 이 함수의 들여쓰기가 올바른지 확인하세요! 👇👇👇
    def add_to_my_wordbook(self, word):
        """틀린 단어를 '나만의 단어장'에 추가합니다."""
        with open(self.my_wordbook_path, 'r+', encoding='utf-8') as f:
            try:
                wordbook = json.load(f)
            except json.JSONDecodeError: # 파일이 비어있을 경우 예외 처리
                wordbook = []
            
            if word not in wordbook:
                wordbook.append(word)
                f.seek(0)
                f.truncate() # 파일 내용을 모두 지움
                json.dump(wordbook, f, ensure_ascii=False, indent=4)
                print(f"✔️ '{word}'을(를) 나만의 단어장에 추가했습니다.")

    def manage_my_wordbook(self):
        """나만의 단어장을 보고 관리하는 메뉴입니다."""
        try:
            with open(self.my_wordbook_path, 'r', encoding='utf-8') as f:
                wordbook = json.load(f)
            
            if not wordbook:
                print("\n텅 비어있습니다. 게임에서 단어를 틀리면 자동으로 추가됩니다.")
                return

            print("\n[📚 나만의 단어장]")
            for i, word in enumerate(wordbook, 1):
                print(f"{i}. {word}")
            
            while True:
                choice = input("\n단어의 뜻을 보려면 번호를, 돌아가려면 'q'를 입력하세요: ")
                if choice.lower() == 'q':
                    break
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(wordbook):
                        self.show_word_meaning(wordbook[index])
                    else:
                        print("⚠️ 잘못된 번호입니다.")
                except ValueError:
                    print("⚠️ 숫자 또는 'q'를 입력해주세요.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ 단어장 파일을 찾을 수 없거나 파일이 비어있습니다.")