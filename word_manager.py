# word_manager.py
import os
import random
import json

class WordManager:
    def __init__(self):
        self.word_lists_path = "word_lists"
        self.my_wordbook_path = "data/my_wordbook.json"
        self.word_meaning_path = "data/word_meanings.json" # 단어 뜻 예시 데이터
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """필요한 파일 및 폴더가 없으면 생성합니다."""
        if not os.path.exists(self.word_lists_path):
            os.makedirs(self.word_lists_path)
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.my_wordbook_path):
            with open(self.my_wordbook_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        # 단어 뜻 예시 데이터 파일 생성
        if not os.path.exists(self.word_meaning_path):
            sample_meanings = {
                "apple": {"meaning": "사과", "example": "An apple a day keeps the doctor away."},
                "banana": {"meaning": "바나나", "example": "Monkeys love to eat bananas."},
                "developer": {"meaning": "개발자", "example": "A software developer writes code."}
            }
            with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
                json.dump(sample_meanings, f, ensure_ascii=False, indent=4)

    def get_word_list(self, filename):
        """지정된 파일에서 단어 목록을 읽어옵니다."""
        try:
            with open(os.path.join(self.word_lists_path, filename), 'r', encoding='utf-8') as f:
                words = [line.strip().lower() for line in f if line.strip()]
            return words
        except FileNotFoundError:
            return []

    def get_available_topics(self):
        """word_lists 폴더에 있는 모든 주제(파일 이름)를 가져옵니다."""
        try:
            files = [f.split('.')[0] for f in os.listdir(self.word_lists_path) if f.endswith('.txt')]
            return files
        except FileNotFoundError:
            return []

    def get_word_by_topic(self, topic):
        """주제에 맞는 단어를 랜덤하게 반환합니다."""
        words = self.get_word_list(f"{topic}.txt")
        return random.choice(words) if words else None

    def get_word_by_level(self, level):
        """난이도에 맞는 단어를 랜덤하게 반환합니다."""
        # 여기서는 주제별 단어장을 난이도별로 매핑하는 예시를 사용
        level_topic_map = {
            '초급': 'animals',
            '중급': 'foods',
            '고급': 'professions'
        }
        topic = level_topic_map.get(level)
        if topic:
            return self.get_word_by_topic(topic)
        return self.get_random_word() # 해당 레벨이 없으면 랜덤 단어 반환

    def get_random_word(self):
        """모든 단어 목록에서 랜덤하게 단어를 하나 선택합니다."""
        all_words = []
        topics = self.get_available_topics()
        if not topics:
            return None
        for topic in topics:
            all_words.extend(self.get_word_list(f"{topic}.txt"))
        return random.choice(all_words) if all_words else None

    def manage_words(self):
        """사용자가 단어를 추가하거나 목록을 보는 메뉴를 관리합니다."""
        while True:
            print("\n[📖 단어 관리]")
            print("1. 단어 추가하기")
            print("2. 전체 단어 목록 보기")
            print("3. 돌아가기")
            choice = input(">> 선택: ")

            if choice == '1':
                topic = input("추가할 단어의 주제(파일 이름)를 입력하세요 (예: animals): ")
                word = input("추가할 단어를 입력하세요: ").lower()
                self.add_word(topic, word)
            elif choice == '2':
                self.view_all_words()
            elif choice == '3':
                break
            else:
                print("⚠️ 잘못된 입력입니다.")

    def add_word(self, topic, word):
        """사용자가 입력한 단어를 파일에 추가합니다."""
        if not word.isalpha():
            print("⚠️ 알파벳으로만 구성된 단어를 입력해주세요.")
            return
        filepath = os.path.join(self.word_lists_path, f"{topic}.txt")
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n{word}")
        print(f"✅ 주제 '{topic}'에 단어 '{word}'이(가) 추가되었습니다.")

    def view_all_words(self):
        """모든 주제의 단어 목록을 출력합니다."""
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
        """단어의 뜻과 예문을 보여줍니다 (예시 데이터 기반)."""
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

    def add_to_my_wordbook(self, word):
        """틀린 단어를 '나만의 단어장'에 추가합니다."""
        with open(self.my_wordbook_path, 'r+', encoding='utf-8') as f:
            wordbook = json.load(f)
            if word not in wordbook:
                wordbook.append(word)
                f.seek(0)
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
        except FileNotFoundError:
            print("⚠️ 단어장 파일을 찾을 수 없습니다.")