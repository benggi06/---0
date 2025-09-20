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
            return sorted(files)
        except FileNotFoundError:
            return []

    def get_word_by_topic(self, topic):
        words = self.get_word_list(f"{topic}.txt")
        return random.choice(words) if words else None

    # [수정] 글자 수로 난이도를 구분하는 로직으로 변경
    def get_word_by_level(self, level):
        """난이도(글자 수)에 맞는 단어를 랜덤하게 반환합니다."""
        level_lengths = {
            '초급': (3, 5),
            '중급': (6, 8),
            '고급': (9, 99) # 9글자 이상
        }
        
        if level not in level_lengths:
            return None

        min_len, max_len = level_lengths[level]
        
        all_words = self._get_all_words()
        if not all_words:
            return None
            
        # 조건에 맞는 단어들만 필터링
        eligible_words = [word for word in all_words if min_len <= len(word) <= max_len]
        
        return random.choice(eligible_words) if eligible_words else None

    def _get_all_words(self):
        """모든 주제의 단어를 하나의 리스트로 합쳐서 반환합니다."""
        all_words = []
        topics = self.get_available_topics()
        if not topics:
            return []
        for topic in topics:
            all_words.extend(self.get_word_list(f"{topic}.txt"))
        return list(set(all_words)) # 중복 제거

    def get_random_word(self):
        """모든 단어 목록에서 랜덤하게 단어를 하나 선택합니다."""
        all_words = self._get_all_words()
        return random.choice(all_words) if all_words else None

    def manage_words(self):
        while True:
            print("\n[📖 단어 관리]")
            print("1. 단어 추가하기 (뜻, 예문 포함)")
            print("2. 단어 삭제하기 🗑️")
            print("3. 전체 단어 목록 보기")
            print("4. 돌아가기")
            choice = input(">> 선택: ")

            if choice == '1':
                topic = input("추가할 단어의 주제(파일 이름)를 입력하세요: ").lower()
                word = input("추가할 단어를 입력하세요: ").lower()
                meaning = input(f"'{word}'의 뜻을 입력하세요: ")
                example = input(f"'{word}'이(가) 사용된 예문을 입력하세요: ")
                self.add_word(topic, word, meaning, example)
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

    def add_word(self, topic, word, meaning, example):
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
        
        try:
            with open(self.word_meaning_path, 'r', encoding='utf-8') as f:
                meanings_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            meanings_data = {}
        
        meanings_data[word] = {"meaning": meaning, "example": example}
        
        with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
            json.dump(meanings_data, f, ensure_ascii=False, indent=4)
        print(f"✅ '{word}'의 뜻과 예문 정보가 저장되었습니다.")

    def delete_word(self, topic, word_to_delete):
        filepath = os.path.join(self.word_lists_path, f"{topic}.txt")
        deleted_from_txt = False
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            
            if word_to_delete in words:
                words.remove(word_to_delete)
                with open(filepath, 'w', encoding='utf-8') as f:
                    for word in words:
                        f.write(f"{word}\n")
                print(f"✅ 주제 '{topic}'에서 단어 '{word_to_delete}'을(를) 삭제했습니다.")
                deleted_from_txt = True
            else:
                print(f"⚠️ 주제 '{topic}'에 '{word_to_delete}' 단어가 존재하지 않습니다.")
        
        except FileNotFoundError:
            print(f"⚠️ '{topic}'이라는 주제(파일)를 찾을 수 없습니다.")

        if deleted_from_txt:
            try:
                with open(self.word_meaning_path, 'r', encoding='utf-8') as f:
                    meanings_data = json.load(f)
                
                if word_to_delete in meanings_data:
                    del meanings_data[word_to_delete]
                    with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
                        json.dump(meanings_data, f, ensure_ascii=False, indent=4)
                    print(f"✅ '{word_to_delete}'의 뜻과 예문 정보가 삭제되었습니다.")
            except (FileNotFoundError, json.JSONDecodeError):
                pass

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
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ 단어 정보 파일이 없거나 손상되었습니다.")

    def add_to_my_wordbook(self, word):
        with open(self.my_wordbook_path, 'r+', encoding='utf-8') as f:
            try:
                wordbook = json.load(f)
            except json.JSONDecodeError:
                wordbook = []
            
            if word not in wordbook:
                wordbook.append(word)
                f.seek(0)
                f.truncate()
                json.dump(wordbook, f, ensure_ascii=False, indent=4)
                print(f"✔️ '{word}'을(를) 나만의 단어장에 추가했습니다.")

    def manage_my_wordbook(self):
        try:
            with open(self.my_wordbook_path, 'r', encoding='utf-8') as f:
                wordbook = json.load(f)
            
            if not wordbook:
                print("\n텅 비어있습니다. 게임에서 단어를 틀리면 자동으로 추가됩니다.")
                return

            print("\n[📚 나만의 단어장]")
            for i, word in enumerate(sorted(wordbook), 1):
                print(f"{i}. {word}")
            
            while True:
                choice = input("\n단어의 뜻을 보려면 번호를, 돌아가려면 'q'를 입력하세요: ")
                if choice.lower() == 'q':
                    break
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(sorted(wordbook)):
                        self.show_word_meaning(sorted(wordbook)[index])
                    else:
                        print("⚠️ 잘못된 번호입니다.")
                except ValueError:
                    print("⚠️ 숫자 또는 'q'를 입력해주세요.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ 단어장 파일을 찾을 수 없거나 파일이 비어있습니다.")